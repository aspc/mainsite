from django.db import models
from django.conf import settings
from datetime import date, time, datetime, timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder

CAMPUSES = ((1, u'PO'), (2, u'SC'), (3, u'CMC'), (4, u'HM'), (5, u'PZ'), (6, u'CGU'), (7, u'CU'), (-1, u'?'))
CAMPUSES_FULL_NAMES = {1: 'Pomona', 2: 'Scripps', 3: 'Claremont-McKenna', 4: 'Harvey Mudd', 5: 'Pitzer'}
CAMPUSES_LOOKUP = dict([(a[1], a[0]) for a in CAMPUSES])
CAMPUSES_LOOKUP['CM'] = CAMPUSES_LOOKUP['CMC']
START_DATE = date(2013, 1, 23)
END_DATE = date(2012, 5, 8)

class RefreshHistory(models.Model):
    FULL = 0
    REGISTRATION = 1
    
    run_date = models.DateTimeField(default=datetime.now)
    last_refresh_date = models.DateTimeField()
    term = models.CharField(max_length=7)
    type = models.IntegerField(choices=(
        (FULL, 'Full'),
        (REGISTRATION, 'Registration'),
    ))
    
    def __unicode__(self):
        return u"{0} refresh at {1}".format(self.get_type_display(), self.last_refresh_date.isoformat())
    
    class Meta:
        verbose_name_plural = 'refresh histories'

class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    
    def course_count(self):
        return len(self.primary_course_set.all())
    
    def non_breaking_name(self):
        return self.name.replace(' ','&nbsp;')
    
    def __unicode__(self):
        return u'[%s] %s' % (self.code, self.name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('department_detail', (), {'slug': self.code,})

class RequirementArea(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    campus = models.PositiveSmallIntegerField(choices=CAMPUSES)

    def course_count(self):
        return len(self.course_set.all())

    def non_breaking_name(self):
        return self.name.replace(' ','&nbsp;')

    def __unicode__(self):
        return u'[%s] %s' % (self.code, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('requirement_area_detail', (), {'slug': self.code,})

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    code_slug = models.CharField(max_length=20, unique=True, db_index=True)
    cx_code = models.CharField(max_length=34, unique=True,
                               db_index=True, editable=False)
    number = models.IntegerField(default=0)
    
    name = models.CharField(max_length=256)
    instructor = models.CharField(max_length=256)
    grading_style = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    credit = models.FloatField()
    
    fee = models.BooleanField()
    spots = models.IntegerField()
    filled = models.IntegerField(blank=True, null=True)
    
    primary_department = models.ForeignKey(Department, related_name='primary_course_set', null=True)
    departments = models.ManyToManyField(Department, related_name='course_set')
    requirement_areas = models.ManyToManyField(RequirementArea, related_name='course_set')
    
    def __unicode__(self):
        return u'[%s] %s (%s)' % (self.code, self.name, self.instructor)
    
    def get_campuses(self):
        campuses = []
        for mtg in self.meeting_set.all():
            campuses.append(mtg.get_campus())
        return campuses
    
    def get_campus(self):
        campii = self.get_campuses()
        if len(campii) > 0:
            return self.get_campuses()[0]
        else:
            return 'UU'
    
    def json(self):
        event_list = []
        for mtg in self.meeting_set.all():
            for begin, end in mtg.to_datetime_ranges():
                event_list.append({
                    'id': '%s-%s-%s' % (self.code, mtg.id, begin.strftime('%w')),
                    'start': begin,
                    'end': end,
                    'title': self.code,
                })
        
        return {'events': event_list, 'info': {'course_code': self.code, 'course_code_slug': self.code_slug, 'detail_url': self.get_absolute_url(), 'campus_code': self.get_campus(),}}
        
    
    @models.permalink
    def get_absolute_url(self):
        return ('course_detail', (), {'course_code': self.code_slug, 'dept': self.primary_department.code,})
    
    class Meta:
        ordering = ('code',)

class Meeting(models.Model):
    course = models.ForeignKey(Course)
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    begin = models.TimeField()
    end = models.TimeField()
    campus = models.PositiveSmallIntegerField(choices=CAMPUSES)
    location = models.CharField(max_length=100)
    
    def gen_days(self):
        s = []
        if self.monday: s.append('M')
        if self.tuesday: s.append('T')
        if self.wednesday: s.append('W')
        if self.thursday: s.append('R')
        if self.friday: s.append('F')
        return s
    
    def to_datetime_ranges(self):
        ranges = []
        combine_dates = []
        
        if self.monday:
            combine_dates.append(START_DATE)
        if self.tuesday:
            combine_dates.append(START_DATE + timedelta(days=1))
        if self.wednesday:                                     
            combine_dates.append(START_DATE + timedelta(days=2))
        if self.thursday:                                      
            combine_dates.append(START_DATE + timedelta(days=3))
        if self.friday:                                        
            combine_dates.append(START_DATE + timedelta(days=4))
        
        for basedate in combine_dates:
            begin = datetime.combine(basedate, self.begin)
            end = datetime.combine(basedate, self.end)
            if end > begin: # Sanity check for malformed meetings in CX
                ranges.append((begin, end))
        
        return ranges
    
    def get_campus(self):
        return CAMPUSES[self.campus - 1][1] # CAMPUSES is now 1-based
    
    def __unicode__(self):
        return u'[%s] Meeting every %s, %s-%s' % (self.course.code, ''.join(self.gen_days()), self.begin.strftime('%I:%M %p'), self.end.strftime('%I:%M %p'))


class Schedule(models.Model):
    courses = models.ManyToManyField(Course)
    create_ts = models.DateTimeField(default=datetime.now)
    
    def json(self):
        all_courses = []
        for course in self.courses.all():
            all_courses.append(course.json())
        return all_courses
    
    def json_encoded(self):
        return json.dumps(self.json(), cls=DjangoJSONEncoder)
    
    @models.permalink
    def get_absolute_url(self):
        return ('aspc.coursesearch.views.view_schedule', (self.id,))
    
    def outside_url(self):
        return u''.join([settings.OUTSIDE_URL_BASE, self.get_absolute_url()])
    
    def __unicode__(self):
        return u'Schedule %i' % (self.id,)