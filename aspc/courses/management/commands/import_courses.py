from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.conf import settings
from aspc.courses.models import (Course, Meeting, CAMPUSES_LOOKUP, Term, Section, Department, Instructor, RequirementArea, RefreshHistory)
import simplejson, urllib, re
from datetime import time, datetime
from django.core.exceptions import MultipleObjectsReturned

FEE_REGEX = re.compile(r'[Ff]ee:\s+\$([\d\.]+)')
ROOM_REGEX = re.compile(r'[A-Z]+\s([^(]+)\s+')
TIME_REGEX = re.compile(r'(\d+:\d+)(AM|PM)?-(\d+:\d+)(AM|PM).')
BR_TAGS = re.compile(r'<br\s?/?>')

COURSES_URL = settings.COURSE_API_URL + 'courses/%s/%s'
TERMS_URL = settings.COURSE_API_URL + 'terms'


def _sanitize(chardata):
    if not chardata:
        return u''
    else:
        return unicode(chardata)


def get_all_terms(term):
    terms = [t['Key'] for t in simplejson.load(urllib.urlopen(TERMS_URL)) if term in t['Key']]
    return terms


class Command(BaseCommand):
    args = ''
    help = 'imports course data'


    def refresh_one_section(self, section, new_data):
        section.grading_style = _sanitize(new_data['GradingStyle'])
        section.description = _sanitize(new_data['Description'])
        section.note = BR_TAGS.sub('\n', _sanitize(new_data['Note'])).strip()
        section.credit = float(new_data['Credits'])
        section.requisites = new_data['Requisites'] == 'Y'

        # Check for fees or prerequisites
        section.fee = FEE_REGEX.findall(unicode(section.description))

        section.save()

        section.course.name = _sanitize(new_data['Name'])

        if new_data['Instructors']:
            for instructor in new_data['Instructors']:
                instructor_object, _ = Instructor.objects.get_or_create(name=instructor['Name'])
                section.instructors.add(instructor_object)

        # refresh meetings
        # Clear old meetings
        section.meeting_set.all().delete()

        if new_data['Schedules']:
            for mtg in new_data['Schedules']:
                if mtg['Weekdays'] != '':
                    # Parse weekdays

                    weekdays = mtg['Weekdays']
                    monday = True if weekdays.find('M') != -1 else False
                    tuesday = True if weekdays.find('T') != -1 else False
                    wednesday = True if weekdays.find('W') != -1 else False
                    thursday = True if weekdays.find('R') != -1 else False
                    friday = True if weekdays.find('F') != -1 else False

                    # Parse times
                    try:
                        start, start_pm, end, end_pm = TIME_REGEX.findall(mtg['MeetTime'])[0]
                    except IndexError:
                        continue

                    if end_pm == 'PM':
                        end_pm = True
                    else:
                        end_pm = False

                    if start_pm in ('AM', 'PM'):
                        start_pm = True if start_pm == 'PM' else False
                    else:
                        start_pm = end_pm

                    start_h, start_m = [int(a) for a in start.split(':')]
                    end_h, end_m = [int(a) for a in end.split(':')]

                    # Correct times to 24hr form

                    if end_pm and end_h != 12:
                        end_h += 12
                    if start_pm and start_h != 12:
                        start_h += 12
                    begin = time(start_h, start_m)
                    end = time(end_h, end_m)

                    # Get campus
                    try:
                        campus_code = mtg['Campus'].split(' ')[0]
                        campus = CAMPUSES_LOOKUP[campus_code]
                    except Exception:
                        campus = CAMPUSES_LOOKUP['?']

                    # Get location

                    if mtg['Room'] and mtg['Building']:
                        room_number = ROOM_REGEX.findall(mtg['MeetTime'])[0]
                        location = "{0}, {1}".format(mtg['Building'], room_number)
                        # special case for Keck building / CU campus
                        if mtg['Building'] == u'Keck Science Center':
                            campus = CAMPUSES_LOOKUP['KS']
                    else:
                        location = ''

                    meeting = Meeting(
                        section=section,
                        monday=monday,
                        tuesday=tuesday,
                        wednesday=wednesday,
                        thursday=thursday,
                        friday=friday,
                        begin=begin,
                        end=end,
                        campus=campus,
                        location=location
                    )
                    meeting.save()

        dcode = ''
        for x in section.course.code:
            if x.isalpha():
                dcode += x
            else:
                break
        try:
            section.course.primary_department = Department.objects.get(code=dcode)
            section.course.save()
        except Department.DoesNotExist:
            self.stdout.write(
                'unknown department "%s" for section "%s" - deleting...\n' % (dcode, section.code))
            section.delete()
            return

        section.save()

        self.stdout.write('section "%s" added\n' % section.code)


    def handle(self, *args, **options):
        term = Term.objects.all()[0]
        terms = get_all_terms(term.key)
        departments = Department.objects.all().values_list('code', flat=True)
        existing = set(Section.objects.filter(term=term).values_list('code', flat=True))
        active = set()

        for t in terms:
            for department in departments:

                try:
                    sections = simplejson.load(urllib.urlopen(COURSES_URL % (t, department)))
                    if sections:
                        for section in sections:
                            try:
                                section_code = section['CourseCode']
                            except TypeError:
                                # Sometimes `section` holds the string "Message" for some reason
                                continue
                            active.add(section_code)

                            if section_code in existing:
                                # update section
                                try:
                                    section_object = Section.objects.get(code=section_code, term=term)
                                except MultipleObjectsReturned:
                                    self.stdout.write('multiple sections of "%s" for term "%s"' % (section_code, term))
                                    continue

                                self.stdout.write('updating section "%s"\n' % section_code)
                                try:
                                    section_object.course.departments.add(Department.objects.get(code=department))
                                except Department.DoesNotExist:
                                    continue
                                self.refresh_one_section(section_object, section)

                            else:
                                # add new section and possible course
                                section_code_slug = slugify(section_code).upper()
                                course_code = section_code[:-3]
                                course_code_slug = section_code_slug[:-3]

                                course_number = ''.join([s for s in course_code if s.isdigit()])
                                if not course_number:
                                    self.stdout.write('unknown number for course "%s" - deleting...\n' % course_code)
                                    continue
                                else:
                                    course_number = int(course_number)

                                course_object, added = Course.objects.get_or_create(code=course_code,
                                                                                    code_slug=course_code_slug,
                                                                                    number=course_number)
                                if added: self.stdout.write('added course "%s"\n' % course_code)

                                try:
                                    course_object.departments.add(Department.objects.get(code=department))
                                except Department.DoesNotExist:
                                    continue

                                section_object = Section(term=term, code=section_code, code_slug=section_code_slug)
                                section_object.course = course_object

                                self.stdout.write('adding section "%s"\n' % section_code)
                                self.refresh_one_section(section_object, section)
                except simplejson.scanner.JSONDecodeError:
                    self.stdout.write('error accessing "%s"' % (COURSES_URL % (t, department)))

            areas = RequirementArea.objects.all().values_list('code', flat=True)

            for area in areas:
                try:
                    area_object = RequirementArea.objects.get(code=area)
                    if urllib.urlopen(COURSES_URL % (t, area)).read():
                        sections = simplejson.load(urllib.urlopen(COURSES_URL % (t, area)))
                        for section in sections:
                            try:
                                code = section['CourseCode']
                            except TypeError:
                                # Sometimes section holds the string "Message" for some reason
                                continue
                            try:
                                section_object = Section.objects.get(code=code, term=term)
                                section_object.course.requirement_areas.add(area_object)
                            except MultipleObjectsReturned:
                                self.stdout.write('multiple sections of "%s" for term "%s"' % (section_code, term))
                                continue

                            except Section.DoesNotExist:
                                self.stdout.write('unknown section "%s"' % code)
                                continue

                except RequirementArea.DoesNotExist:
                    continue

        # Remove courses that have been deleted from the catalog (or whose codes
        # have changed... can't tell the difference)
        stale = existing - active

        if stale:
            Section.objects.filter(code__in=stale).delete()

        # Add a timestamp of refresh time (i.e. a new RefreshHistory record)
        new_history = RefreshHistory(
            last_refresh_date=datetime.now(),
            term=term,
            type=RefreshHistory.FULL
        )
        new_history.save()