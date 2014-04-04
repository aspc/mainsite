from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from aspc.courses.models import (Course, Meeting, CAMPUSES_LOOKUP, Term, Section, Department, Instructor, RequirementArea)
import simplejson, urllib, time, re

FEE_REGEX = re.compile(r'[Ff]ee:\s+\$([\d\.]+)')
ROOM_REGEX = re.compile(r'[A-Z]+\s([^(]+)\s+')
TIME_REGEX = re.compile(r'(\d+:\d+)(AM|PM)?-(\d+:\d+)(AM|PM).')
BR_TAGS = re.compile(r'<br\s?/?>')

ENROLLMENTS_URL = 'http://jicsweb.pomona.edu/api/courses/&s'
COURSES_URL = 'http://jicsweb.pomona.edu/api/courses/&s/&s'


def _sanitize(chardata):
    if not chardata:
        return u''
    else:
        return chardata.decode('utf8', 'replace')


class Command(BaseCommand):
    args = ''
    help = 'imports course data'


    def refresh_one_section(self, object, new_data):
        object.course.name = _sanitize(new_data['Name'])
        object.grading_style = _sanitize(new_data['GradingStyle'])
        object.description = _sanitize(new_data['Description'])
        object.note = BR_TAGS.sub('\n', _sanitize(new_data['Note'])).strip()
        object.credit = float(new_data['Credits'])
        object.requisites = new_data['Requisites'] == 'Y'

        object.save()

        for instructor in new_data['Instructors']:
            instructor_object, _ = Instructor.objects.get_or_create(name=instructor['Name'])
            object.instructors.add(instructor_object)

        # Check for fees or prerequisites
        match = FEE_REGEX.findall(unicode(object.description))
        if match:
            object.fee = True


        # refresh meetings
        # Clear old meetings
        object.meeting_set.all().delete()

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

                if mtg.Room and mtg['Building']:
                    room_number = ROOM_REGEX.findall(mtg['MeetTime'])[0]
                    location = "{0}, {1}".format(mtg['Building'], room_number)
                    # special case for Keck building / CU campus
                    if mtg['Building'] == u'Keck Science Center':
                        campus = CAMPUSES_LOOKUP['KS']
                else:
                    location = ''

                meeting = Meeting(
                    section=object,
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

        object.save()

        self.stdout.write('section "%s" added\n' % object.code)

        try:
            object.course.primary_department = Department.objects.get(code=new_data['Department'])
        except Department.DoesNotExist:
            self.stdout.write('unknown department for section "%s" - deleting...\n' % object.code)
            object.delete()
            return


    def refresh_enrollments(self):
        term = Term.objects.all().order_by('-pk').values_list('key', flatten=True)[0]
        courses = simplejson.load(urllib.urlopen(ENROLLMENTS_URL % term))

        for course in courses:
            code = course['CourseCode']
            object = Section.objects.get(code=code)

            object.perms = int(course['PermCount'])
            object.spots = int(course['SeatsTotal'])
            object.filled = int(course['SeatsFilled'])

            object.save()

            self.stdout.write('enrollments for section "%s" refreshed\n' % object.code)


    def handle(self, *args, **options):
        existing = set(Section.objects.values_list('code', flat=True))
        active = set()

        term = Term.objects.all().order_by('-pk').values_list('key', flatten=True)[0]
        departments = Department.objects.all().values_lsit('code', flatten=True)

        for department in departments:
            courses = simplejson.load(urllib.urlopen(ENROLLMENTS_URL % (term, department)))

            for course in courses:
                code = course['CourseCode']
                active.add(code)

                if code in existing:
                    # update section
                    object = Section.objects.get(code=code)
                    self.stdout.write('updating section "%s"\n' % code)
                    self.refresh_one_section(object, course)

                else:
                    # add new course and section
                    term = Term.objects.get(key=term)
                    code_slug = slugify(code).upper()
                    course_code = code[:-3]
                    course_code_slug = code_slug[:-3]
                    course_number = int(''.join([s for s in course_code if s.isdigit()]))

                    course_object, added= Course.objects.get_or_create(code=course_code, code_slug=course_code_slug,
                                                                    number=course_number)
                    if added: self.stdout.write('added course "&s"\n' % course_code)

                    try:
                        course_object.departments.add(Department.objects.get(code=department))
                    except Department.DoesNotExist:
                        break

                    object = Section(term=term, course=course, code=code, code_slug=code_slug)

                    self.stdout.write('adding section "%s"\n' % code)

                    self.refresh_one_section(object, course)

        areas = RequirementArea.objects.all().values_lsit('code', flatten=True)

        for area in areas:
            try:
                area_object = RequirementArea.objects.get(code=area)
                courses = simplejson.load(urllib.urlopen(ENROLLMENTS_URL % (term, area)))

                for course in courses:
                    code = course['CourseCode']
                    try:
                        object = Section.objects.get(code=code)
                        object.course.requirement_areas.add(area_object)
                    except Section.DoesNotExist:
                        break

            except RequirementArea.DoesNotExist:
                break

        # Remove courses that have been deleted from the catalog (or whose codes
        # have changed... can't tell the difference)
        stale = existing - active

        if stale:
            Course.objects.filter(code__in=stale).delete()


        self.refresh_entrollments()