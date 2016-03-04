from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.defaultfilters import slugify
import simplejson, urllib, re
from datetime import time
import logging

from aspc.courses.models import Course, Meeting, CAMPUSES_LOOKUP, Term, Section, Department, Instructor, RequirementArea, RefreshHistory

COURSES_URL = settings.COURSE_API_URL + 'courses/{0}/{1}'
TERMS_URL = settings.COURSE_API_URL + 'terms'

FEE_REGEX = re.compile(r'[Ff]ee:\s+\$([\d\.]+)')
BR_TAGS_REGEX = re.compile(r'<br\s?/?>')
ROOM_REGEX = re.compile(r'[A-Z]+\s([^(]+)\s+')
TIME_REGEX = re.compile(r'(\d+:\d+)(AM|PM)?-(\d+:\d+)(AM|PM).')

logger = logging.getLogger(__name__)

def log_error(message):
	logger.error('**ERROR**: {0}'.format(message))

def log_added(message):
	logger.info('ADDED: {0}'.format(message))

def log_updated(message):
	logger.info('UPDATED: {0}'.format(message))

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
			log_error('could not access terms URL ' + self.url)

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
			log_error('could not access department URL ' + self.url)

class RequirementAreaEndpoint(object):
	def __init__(self, area_code, term_key):
		super(RequirementAreaEndpoint, self).__init__()
		self.url = COURSES_URL.format(term_key, area_code)

		try:
			self.courses_in_area = simplejson.load(urllib.urlopen(self.url))
		except simplejson.scanner.JSONDecodeError:
			self.courses_in_area = []
			log_error('could not access requirement area URL ' + self.url)


class Command(BaseCommand):
	args = ''
	help = 'imports course data'

	def __init__(self):
		super(Command, self).__init__()
		self.current_term = Term.objects.all()[0]
		self.current_term_keys = TermEndpoint().get_related_term_keys_for_term(term=self.current_term) # E.g. ['2016;SP', '2016;SP;P1']
		self.department_codes = Department.objects.all().values_list('code', flat=True) # E.g. ['RLST', 'MATH']
		self.area_codes = RequirementArea.objects.all().values_list('code', flat=True) # E.g. ['1A5', '5NAT']

	def handle(self, *args, **options):
		for term_key in self.current_term_keys:
			# Load the course and section data by department for the current term
			for department_code in self.department_codes:
				self._load_courses_in_department(department_code=department_code, term_key=term_key)

			# Set the area requirement data for those sections that were just added
			for area_code in self.area_codes:
				self._load_area_requirements_for_sections(area_code=area_code, term_key=term_key)

	def _load_courses_in_department(self, department_code, term_key):
		department = DepartmentEndpoint(department_code=department_code, term_key=term_key)
		if department.courses_this_term:
			for section_data in department.courses_this_term:
				section_code = section_data['CourseCode'] # This parameter is poorly named
				course_code = section_code[:-3]
				logger.info('currently importing course: ' + section_code)

				if course_code:
					# Get or create the Course object for this course
					course_object, was_created = Course.objects.get_or_create(
						code=course_code,
						code_slug=slugify(course_code).upper()
					)
					course_object.number = int(''.join([s for s in course_code if s.isdigit()]))
					course_object.departments.add(Department.objects.get(code=department_code))

					primary_department_code = course_code[:4].strip() # Department codes are 3 or 4 characters long
					try:
						course_object.primary_department = Department.objects.get(code=primary_department_code)
					except Department.DoesNotExist:
						log_error('primary department {0} does not exist for course {1}'.format(primary_department_code, course_code))
						course_object.primary_department = course_object.departments.all()[0] # Just set the primary department to the course's first department instead

					course_object.save()

					if was_created:
						log_added('course ' + course_code)
					else:
						log_updated('course ' + course_code)

					# Get or create the Section object for this section
					section_object, was_created = Section.objects.get_or_create(
						term=self.current_term,
						course=course_object,
						code=section_code,
						code_slug=slugify(section_code).upper()
					)
					section_object.description = sanitize(section_data['Description'])
					section_object.note = BR_TAGS_REGEX.sub('\n', sanitize(section_data['Note'])).strip()
					section_object.credit = float(section_data['Credits'])
					section_object.requisites = section_data['Requisites'] == 'Y'
					section_object.fee = FEE_REGEX.findall(unicode(section_data['Description']))
					section_object.grading_style = sanitize(section_data['GradingStyle'])

					if section_data['Instructors']:
						for instructor in section_data['Instructors']:
							instructor_object, _ = Instructor.objects.get_or_create(name=instructor['Name'])
							section_object.instructors.add(instructor_object)

					if section_data['Schedules']:
						for meeting in section_data['Schedules']:
							if meeting['Weekdays'] != '':
								parsed_meeting_data = self._parse_meeting_data(meeting)
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

					section_object.save()

					if was_created:
						log_added('section ' + section_code)
					else:
						log_updated('section ' + section_code)

	def _load_area_requirements_for_sections(self, area_code, term_key):
		logger.info('currently loading data for area requirement: ' + area_code)

		area_object = RequirementArea.objects.get(code=area_code)
		courses_in_area = RequirementAreaEndpoint(area_code=area_code, term_key=term_key).courses_in_area

		# For each course that is cataloged in that area...
		for course in courses_in_area:
			# It's possible but unlikely that this course will have a hitherto unseen course_code at this point
			# This would only happen if the course is not listed under a department, but only under an area requirement
			# If this is the case, don't bother to import it at this point
			course_code = course['CourseCode']
			section_objects = Section.objects.filter(code=course_code, term=self.current_term)

			# For each Section of that course...
			for section_object in section_objects:
				# Append the relevant AreaRequirement object to that Section
				section_object.course.requirement_areas.add(area_object)

	def _parse_meeting_data(self, meeting):
		# Parse weekdays
		weekdays = meeting['Weekdays']
		monday = True if weekdays.find('M') != -1 else False
		tuesday = True if weekdays.find('T') != -1 else False
		wednesday = True if weekdays.find('W') != -1 else False
		thursday = True if weekdays.find('R') != -1 else False
		friday = True if weekdays.find('F') != -1 else False

		# Parse times
		try:
			start, start_pm, end, end_pm = TIME_REGEX.findall(meeting['MeetTime'])[0]
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
			campus_code = meeting['Campus'].split(' ')[0]
			campus = CAMPUSES_LOOKUP[campus_code]
		except Exception:
			campus = CAMPUSES_LOOKUP['?']

		# Get location
		if meeting['Room'] and meeting['Building']:
			room_number = ROOM_REGEX.findall(meeting['MeetTime']) # Returns a list
			room_number = room_number[0] if room_number else ''
			location = "{0}, {1}".format(meeting['Building'], room_number)
			# special case for Keck building / CU campus
			if meeting['Building'] == u'Keck Science Center':
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