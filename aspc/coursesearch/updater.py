import logging, re
from pprint import pprint
from datetime import time
import pyodbc
from django.template.defaultfilters import slugify
from aspc.coursesearch.models import (Course, Meeting, Department, 
    RequirementArea, CAMPUSES, CAMPUSES_LOOKUP)

FEE_REGEX = re.compile(r'[Ff]ee:\s+\$([\d\.]+)')
ROOM_REGEX = re.compile(r'[A-Z]+\s([^(]+)\s+')

logger = logging.getLogger(__name__)

def _is_requirement_area(deptcode):
    # By convention, dept codes of the form "letter, digit, letter" are
    # actually requirement areas (like Pomona Gen Eds)
    if deptcode[0] in [str(a) for a in range(1, len(CAMPUSES) + 1)]:
        return True
    else:
        return False

def refresh_departments(cursor):
    
    depts = cursor.execute("""
        SELECT Code, Description
        FROM pom.Departments;""").fetchall()
    
    total = created = 0
    
    for deptrow in depts:
        if _is_requirement_area(deptrow.Code):
            try:
                ra = RequirementArea.objects.get(code=deptrow.Code)
            except RequirementArea.DoesNotExist:
                ra = RequirementArea(code=deptrow.Code)
                created += 1
            
            ra.name = deptrow.Description
            ra.campus = CAMPUSES[int(deptrow.Code[0]) - 1][0] # CAMPUSES is 0-indexed
            ra.save()
        else:
            try:
                dept = Department.objects.get(code=deptrow.Code)
            except Department.DoesNotExist:
                dept = Department(code=deptrow.Code)
                created += 1
            
            dept.name = deptrow.Description
            dept.save()
        total += 1
    
    logger.info("Updated {0} departments and requirement areas, creating {1}"
                " new records".format(total, created))

def refresh_meetings(cursor, course):
    # Create Meeting objects for the course's meetings
    meetings = cursor.execute("""SELECT Weekdays, MeetTime, Campus, Building, Room
        FROM pom.Courses AS pc
        JOIN pom.Meetings AS pm
        ON (pc.CourseCode = pm.CourseCode)
        WHERE pm.CourseCode = ?
        AND Weekdays IS NOT NULL 
        AND MeetTime NOT LIKE '%00:00-00:00AM. %';""",
        course.cx_code.encode('utf8')).fetchall()
    
    # Query explanation: Null weekdays can't be displayed on the schedule, so
    # they don't make any sense to store (or try to parse). Non-existent 
    # meeting times likewise shouldn't be parsed.
    
    # Clear old meetings
    course.meetings.all().delete()
    
    for mtg in meetings:
        # Parse weekdays
        
        weekdays = mtg.Weekdays
        monday = True if weekdays.find('M') != -1 else False
        tuesday = True if weekdays.find('T') != -1 else False
        wednesday = True if weekdays.find('W') != -1 else False
        thursday = True if weekdays.find('R') != -1 else False
        friday = True if weekdays.find('F') != -1 else False
        
        # Parse times
        
        start, end = mtg.MeetTime.split('. ')[0].split('-')
        end, end_pm = end[:-2], True if end[-2:] == 'PM' else False

        if start[-2:] in ('AM', 'PM'):
            start, start_pm = start[:-2], True if start[-2:] == 'PM' else False
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
        
        campus_code = mtg.Campus.split(' ')[0]
        campus = CAMPUSES_LOOKUP[campus_code]
        
        # Get location
        room_number = ROOM_REGEX.findall(mtg.MeetTime)[0]
        
        if mtg.Room and mtg.Building:
            location = "{0}, {1}".format(mtg.Building, room_number)
        else:
            location = ''
        
        meeting = Meeting(
            course=course,
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

def _sanitize(chardata):
    if not chardata:
        return u''
    else:
        return chardata.decode('utf8', 'replace')

def refresh_one_course(cursor, course):
    course_row = cursor.execute("""SELECT * 
        FROM pom.Courses 
        WHERE CourseCode = ?""", course.cx_code.encode('utf8')).fetchone()
    
    logger.info("Populating information for [{0}] {1}".format(
        course.cx_code, course_row.Name))
    
    course.name = _sanitize(course_row.Name)
    course.grading_style = _sanitize(course_row.GradingStyle)
    course.description = _sanitize(course_row.Description)
    course.note = _sanitize(course_row.Note)
    course.credit = float(course_row.Credits)
    course.spots = int(course_row.SeatsTotal)
    course.filled = int(course_row.SeatsFilled)
    
    course.save()
    
    # Get the instructors for the course
    instructors = cursor.execute("""SELECT pi.Name, pc.CourseCode, pi.InstructorID
        FROM pom.Instructors AS pi 
        JOIN pom.Courses AS pc 
        ON (pc.CourseCode = pi.CourseCode) 
        WHERE pi.CourseCode = ?
        ORDER BY pi.InstructorID;""", course.cx_code.encode('utf8')).fetchall()
    
    inames = []
    for instructor in instructors:
        inames.append(instructor.Name)
    
    course.instructor = "; ".join(inames)
    
    # TODO: Normalize instructors into their own table
    
    # Check for fees or prerequisites
    match = FEE_REGEX.findall(unicode(course.description))
    if match:
        course.fee = True
    
    # TODO: add a prerequisites booleanfield
    # if course_row.Requisites == "Y":
    #     course.prerequisites = True
    
    # Populate meeting times and locations
    
    refresh_meetings(cursor, course)
    
    # Populate departments and requirement areas
    
    try:
        course.primary_department = Department.objects.get(code=course_row.Department)
    except Department.DoesNotExist:
        logger.warning("Tried to create a course record for {0} in the {1}"
            "department, but {1} did not exist. Skipping.".format(
                course.cx_code, course_row.Department))
        course.delete()
        return
    
    # Clear secondary department/RA associations in case they've changed
    course.departments.clear()
    course.requirement_areas.clear()
    
    dept_rows = cursor.execute("""SELECT CallingDepartment 
        FROM pom.Courses
        WHERE CourseCode = ?;""", course.cx_code.encode('utf8')).fetchall()
    
    for dept in dept_rows:
        if _is_requirement_area(dept.CallingDepartment):
            course.requirement_areas.add(
                RequirementArea.objects.get(code=dept.CallingDepartment)
            )
        else:
            course.departments.add(
                Department.objects.get(code=dept.CallingDepartment)
            )
    
    course.save()


def refresh_courses(cursor):
    existing = set(Course.objects.values_list('cx_code', flat=True))
    cx_existing = set()
    
    cx_course_codes = cursor.execute("""SELECT CourseCode FROM pom.Courses
        WHERE CourseCode NOT LIKE '%;GRAD;';""").fetchall()
    
    for row in cx_course_codes:
        cx_existing.add(row.CourseCode)
    
    # Remove courses that have been deleted from the catalog (or whose codes
    # have changed... can't tell the difference)
    stale = existing - cx_existing
    
    logger.info("Removing {0} courses whose corresponding codes are no longer"
                " in the JICSWS database...".format(len(stale)))
    Course.objects.filter(cx_code__in=stale).delete()
    logger.info("Removed all of the following: {0}".format(pprint(stale)))
    
    # Things in CX that we don't have yet:
    new = cx_existing - existing
    
    logger.info("Creating new course records for {0} "
                "new courses".format(len(new)))
    for cx_code in new:
        # turning CHEM110ALPO;02 into CHEM110ALPO-02, etc:
        code = '-'.join(cx_code.split(';')[2:4])
        
        new_course = Course(
            cx_code=cx_code,
            code=code,
            code_slug=slugify(code).upper())
        refresh_one_course(cursor, new_course)
        logger.info("Created [{0}] {1}".format(
            new_course.code, 
            new_course.name
        ))
    
    # Existing stuff to refresh:
    to_refresh = existing & cx_existing
    
    logger.info("Refreshing the course information for {0} "
                "existing course records".format(len(to_refresh)))
    
    for cx_code in to_refresh:
        course = Course.objects.get(cx_code=cx_code)
        refresh_one_course(cursor, course)
        logger.info("Refreshed [{0}] {1}".format(
            course.code, 
            course.name
        ))
    