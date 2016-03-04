from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.defaultfilters import slugify
import simplejson, urllib, re
import logging

from aspc.courses.models import Course, Meeting, CAMPUSES_LOOKUP, Term, Section, Department, Instructor, RequirementArea, RefreshHistory

COURSES_URL = settings.COURSE_API_URL + 'courses/{0}/{1}'
TERMS_URL = settings.COURSE_API_URL + 'terms'

FEE_REGEX = re.compile(r'[Ff]ee:\s+\$([\d\.]+)')
BR_TAGS_REGEX = re.compile(r'<br\s?/?>')

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