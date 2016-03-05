from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db import IntegrityError
import simplejson, urllib, re
from datetime import time, datetime
import logging

from aspc.courses.models import Course, Meeting, CAMPUSES_LOOKUP, Term, Section, Department, Instructor, RequirementArea, RefreshHistory

COURSES_URL = settings.COURSE_API_URL + 'courses/{0}/{1}'
TERMS_URL = settings.COURSE_API_URL + 'terms'

FEE_REGEX = re.compile(r'[Ff]ee:\s+\$([\d\.]+)')
BR_TAGS_REGEX = re.compile(r'<br\s?/?>')
ROOM_REGEX = re.compile(r'[A-Z]+\s([^(]+)\s+')
TIME_REGEX = re.compile(r'(\d+:\d+)(AM|PM)?-(\d+:\d+)(AM|PM).')

logger = logging.getLogger(__name__)

def sanitize(chardata):
	if not chardata:
		return u''
	else:
		return unicode(chardata)

class TermEndpoint(object):
	def __init__(self):
		super(TermEndpoint, self).__init__()
		self.url = TERMS_URL

		try:
			self.terms = simplejson.load(urllib.urlopen(self.url))
		except simplejson.scanner.JSONDecodeError:
			self.terms = []
			logger.warning('could not access terms URL ' + self.url)

	def get_related_term_keys_for_term(self, term):
		return[t['Key'] for t in self.terms if term.key in t['Key']]

class DepartmentEndpoint(object):
	def __init__(self, department_code, term_key):
		super(DepartmentEndpoint, self).__init__()
		self.url = COURSES_URL.format(term_key, department_code)

		try:
			self.courses_this_term = simplejson.load(urllib.urlopen(self.url))
		except simplejson.scanner.JSONDecodeError:
			self.courses_this_term = []
			logger.warning('could not access department URL ' + self.url)

class RequirementAreaEndpoint(object):
	def __init__(self, area_code, term_key):
		super(RequirementAreaEndpoint, self).__init__()
		self.url = COURSES_URL.format(term_key, area_code)

		try:
			self.courses_in_area = simplejson.load(urllib.urlopen(self.url))
		except simplejson.scanner.JSONDecodeError:
			self.courses_in_area = []
			logger.warning('could not access requirement area URL ' + self.url)


class Command(BaseCommand):
	args = ''
	help = 'imports course data'

	def __init__(self):
		super(Command, self).__init__()
		self.current_term = Term.objects.all()[0]
		self.current_term_keys = TermEndpoint().get_related_term_keys_for_term(term=self.current_term) # E.g. ['2016;SP', '2016;SP;P1']
		self.department_codes = Department.objects.all().values_list('code', flat=True) # E.g. ['RLST', 'MATH']
		self.area_codes = RequirementArea.objects.all().values_list('code', flat=True) # E.g. ['1A5', '5NAT']

	### HANDLER ###
	def handle(self, *args, **options):
		for term_key in self.current_term_keys:
			# Load the course and section data by department for the current term
			for department_code in self.department_codes:
				self._load_courses_in_department(department_code=department_code, term_key=term_key)

			# Set the area requirement data for those courses that were just added
			for area_code in self.area_codes:
				self._set_area_requirement_data_for_courses(area_code=area_code, term_key=term_key)

		# Keep a record of when the last import time was
		self._set_last_updated_time()

	def _load_courses_in_department(self, department_code, term_key):
		department = DepartmentEndpoint(department_code=department_code, term_key=term_key)
		if department.courses_this_term:
			for section_data in department.courses_this_term:
				if section_data['CourseCode']:
					logger.info('currently importing course: ' + section_data['CourseCode'])

					# Get or create the Course object for this course
					course_object = self._create_or_update_course(course_data=section_data, department_code=department_code)

					# Get or create the Section object for this specific section of that course
					if course_object:
						self._create_or_update_section(section_data=section_data, course_object=course_object)

	def _create_or_update_course(self, course_data, department_code):
		course_code = course_data['CourseCode'][:-3].strip() # E.g. 'ANTH088' instead of 'ANTH088 PZ-01'

		# First, create the skeleton Course object, or get it if it already exists
		try:
			course_object, was_created = Course.objects.get_or_create(
				code=course_code,
				code_slug=slugify(course_code).upper()
			)
		except IntegrityError as e:
			# The get_or_create call should prevent this from happening most of the time, but it's still possible
			logger.error('{0} duplicate course: {1}\n'.format(e.message, course_code))
			return None

		# Set the data for all the Course properties
		try:
			course_object.name = sanitize(course_data['Name'])
			course_object.number = int(''.join([s for s in course_code if s.isdigit()]))
			course_object.departments.add(Department.objects.get(code=department_code))
		except Exception as e:
			logger.error('{0} corrupted data for course {1}: {2}\n'.format(e.message, course_code, course_data))

		# Set the data for the Course.primary_department property (a little tricky to calculate)
		primary_department_code = course_code[:4].strip() # Department codes are 3 or 4 characters long
		try:
			course_object.primary_department = Department.objects.get(code=primary_department_code)
		except Department.DoesNotExist:
			logger.error('primary department {0} does not exist for course {1}'.format(primary_department_code, course_code))
			course_object.primary_department = course_object.departments.all()[0] # Just set the primary department to the course's first department instead

		# Save the fully-formed Course
		course_object.save()

		if was_created:
			logger.info('ADDED: course ' + course_code)
		else:
			logger.info('UPDATED: course ' + course_code)

		return course_object

	def _create_or_update_section(self, section_data, course_object):
		section_code = section_data['CourseCode'] # E.g. 'ANTH088 PZ-01' not 'ANTH088'

		# First, create the skeleton Section object, or get it if it already exists
		try:
			section_object, was_created = Section.objects.get_or_create(
				term=self.current_term,
				course=course_object,
				code=section_code,
				code_slug=slugify(section_code).upper()
			)
		except IntegrityError as e:
			# The get_or_create call should prevent this from happening most of the time, but it's still possible
			logger.error('{0} duplicate section: {1}\n'.format(e.message, section_code))
			return

		# Set the data for all the Section properties
		try:
			section_object.description = sanitize(section_data['Description'])
			section_object.note = BR_TAGS_REGEX.sub('\n', sanitize(section_data['Note'])).strip()
			section_object.credit = float(section_data['Credits'])
			section_object.requisites = section_data['Requisites'] == 'Y'
			section_object.fee = FEE_REGEX.findall(unicode(section_data['Description']))
			section_object.grading_style = sanitize(section_data['GradingStyle'])
		except Exception as e:
			logger.error('{0} corrupted data for section {1}: {2}\n'.format(e.message, section_code, section_data))

		# Link the Section with its Instructor
		if section_data['Instructors']:
			for instructor in section_data['Instructors']:
				instructor_object, _ = Instructor.objects.get_or_create(name=instructor['Name'])
				section_object.instructors.add(instructor_object)

		# Save the fully-formed Section
		section_object.save()

		# Create the Meeting objects for this Section
		if section_data['Schedules']:
			section_object.meeting_set.all().delete() # Delete all the old Meeting records for this Section first
			for meeting_data in section_data['Schedules']:
				if meeting_data['Weekdays'] != '':
					parsed_meeting_data = self._parse_meeting_data(meeting_data=meeting_data)
					if parsed_meeting_data:
						meeting_object = Meeting(
							section=section_object,
							monday=parsed_meeting_data['monday'],
							tuesday=parsed_meeting_data['tuesday'],
							wednesday=parsed_meeting_data['wednesday'],
							thursday=parsed_meeting_data['thursday'],
							friday=parsed_meeting_data['friday'],
							begin=parsed_meeting_data['begin'],
							end=parsed_meeting_data['end'],
							campus=parsed_meeting_data['campus'],
							location=parsed_meeting_data['location']
						)
						meeting_object.save()

		if was_created:
			logger.info('ADDED: section ' + section_code)
		else:
			logger.info('UPDATED: section ' + section_code)

	def _set_area_requirement_data_for_courses(self, area_code, term_key):
		area_object = RequirementArea.objects.get(code=area_code)
		courses_in_area = RequirementAreaEndpoint(area_code=area_code, term_key=term_key).courses_in_area

		# For each course that is cataloged in that area...
		for course in courses_in_area:
			logger.info('currently loading data for area requirement: ' + area_code)

			# Set that course's requirement area data
			try:
				course_object = Course.objects.get(code=course['CourseCode'])
				course_object.requirement_areas.add(area_object)
			except Course.DoesNotExist:
				# It's possible but unlikely that this course will have a hitherto unseen course_code at this point,
				# and its corresponding course_object does not exist yet
				# This would only happen if the course is not listed under a department, but only under an area requirement
				# If this is the case, don't worry about it or bother to import it at this point - just continue the loop
				continue

	def _parse_meeting_data(self, meeting_data):
		# Parse weekdays
		weekdays = meeting_data['Weekdays']
		monday = True if weekdays.find('M') != -1 else False
		tuesday = True if weekdays.find('T') != -1 else False
		wednesday = True if weekdays.find('W') != -1 else False
		thursday = True if weekdays.find('R') != -1 else False
		friday = True if weekdays.find('F') != -1 else False

		# Parse times
		try:
			start, start_pm, end, end_pm = TIME_REGEX.findall(meeting_data['MeetTime'])[0]
		except IndexError:
			return None

		# Set end_pm
		if end_pm == 'PM':
			end_pm = True
		else:
			end_pm = False

		# Set start_pm
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
			campus_code = meeting_data['Campus'].split(' ')[0]
			campus = CAMPUSES_LOOKUP[campus_code]
		except Exception:
			campus = CAMPUSES_LOOKUP['?']

		# Get location
		if meeting_data['Room'] and meeting_data['Building']:
			room_number = ROOM_REGEX.findall(meeting_data['MeetTime']) # Returns a list
			room_number = room_number[0] if room_number else ''
			location = "{0}, {1}".format(meeting_data['Building'], room_number)
			# special case for Keck building / CU campus
			if meeting_data['Building'] == u'Keck Science Center':
				campus = CAMPUSES_LOOKUP['KS']
		else:
			location = ''

		return {
			'monday': monday,
			'tuesday': tuesday,
			'wednesday': wednesday,
			'thursday': thursday,
			'friday': friday,
			'begin': begin,
			'end': end,
			'campus': campus,
			'location': location
		}

	def _set_last_updated_time(self):
		new_history = RefreshHistory(
			last_refresh_date=datetime.now(),
			term=self.current_term,
			type=RefreshHistory.FULL
		)
		new_history.save()