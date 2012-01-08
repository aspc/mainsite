from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.template.defaultfilters import slugify
from aspc.coursesearch.models import Department, Course, Meeting, CAMPUSES_LOOKUP
import re

from datetime import datetime, date, time, timedelta

keyword_regex = re.compile(r'(\w+)')

def parse_meeting(mtg):
    daytime, timeloc, loc = mtg
    day_bits = daytime.split(' ')
    if len(day_bits) != 2:
        return None
    weekdays, times = day_bits
    monday = True if weekdays.find('M') != -1 else False
    tuesday = True if weekdays.find('T') != -1 else False
    wednesday = True if weekdays.find('W') != -1 else False
    thursday = True if weekdays.find('R') != -1 else False
    friday = True if weekdays.find('F') != -1 else False
    
    start, end = times.split('-')
    #print start, end
    end, end_pm = end[:-2], True if end[-2:] == 'PM' else False
    
    if start[-2:] in ('AM', 'PM'):
        start, start_pm = start[:-2], True if start[-2:] == 'PM' else False
    else:
        start_pm = end_pm
    
    start_h, start_m = [int(a) for a in start.split(':')]
    end_h, end_m = [int(a) for a in end.split(':')]
    
    if end_pm and end_h != 12:
        end_h += 12
    if start_pm and start_h != 12:
        start_h += 12
    begin = time(start_h, start_m)
    end = time(end_h, end_m)
    
    return monday, tuesday, wednesday, thursday, friday, begin, end, loc

class Command(BaseCommand):
    args = ''
    help = 'imports data from data/scraped_courses.py'
    deptrx = re.compile(r'([A-Z]+)')

    def handle(self, *args, **options):
        Course.objects.all().delete() # do NOT want this any more, we should merge gracefully.
        from aspc.data.scraped_courses import courses
        for k, scraped_course in courses.items():
            code_slug = slugify(scraped_course['code']).upper()
            dept_code = self.deptrx.match(code_slug).groups()[0]
            
            try:
                course = Course.objects.get(code_slug=code_slug)
                self.stdout.write('found existing for code: "%s", dept_code: "%s"\n' % (course.code, dept_code))
            except Course.DoesNotExist:
                course = Course(code=scraped_course['code'], code_slug=code_slug)
                self.stdout.write('adding new for code: "%s", dept_code: "%s"\n' % (course.code, dept_code))
            
            course.name = scraped_course['name']
            course.instructor = scraped_course['instructor']
            course.grading_style = scraped_course['grading_style']
            course.description = scraped_course['description']
            course.note = scraped_course['note']
            course.credit = float(scraped_course['credit'])
            course.spots = int(scraped_course['slots'])
            
            try:
                course.primary_department = Department.objects.get(code=dept_code)
            except Department.DoesNotExist:
                course.primary_department = None
            
            course.save() # Save first then run m2m
            
            course.departments.clear() # On the off chance that a course has been 
                # removed from one subject area / dept between imports
                # we don't want to keep stale dept relationships around
            
            for dcode in scraped_course['depts']:
                course.departments.add(Department.objects.get(code=dcode))
            
            if not course.primary_department:
                if course.departments.count() == 0:
                    course.delete()
                    self.stdout.write('Failed to add %s because it wasn\'t in a department' % course.code)
                else:
                    smallest_dept = course.departments.annotate(num_courses=Count('primary_course_set')).distinct().order_by('-num_courses')[0]
                    course.primary_department = smallest_dept
            
            course.save()
            
            course.meeting_set.all().delete() # don't want to keep stale meetings, can safely re-create all because schedule m2ms to course
            
            for mtg in scraped_course['mtgs']:
                meeting_breakout = parse_meeting(mtg)
                if not meeting_breakout:
                    continue
                m, t, w, r, f, begin, end, loc = meeting_breakout
                new_meeting = Meeting(course=course)
                new_meeting.monday = m
                new_meeting.tuesday = t
                new_meeting.wednesday = w
                new_meeting.thursday = r
                new_meeting.friday = f
                
                new_meeting.begin = begin
                new_meeting.end = end
                
                campus_code = keyword_regex.findall(loc)[0]
                if campus_code not in CAMPUSES_LOOKUP.keys():
                    continue
                new_meeting.campus = CAMPUSES_LOOKUP[campus_code]
                
                new_meeting.location = loc[11:]
                
                new_meeting.save()
            self.stdout.write('Successfully added course "%s"\n' % course.name.encode('utf-8'))
