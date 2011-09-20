from django.db import models
from django.contrib.humanize.templatetags.humanize import ordinal
from datetime import date

class Term(models.Model):
    """Representing a term"""
    
    TERM_TYPES = (
        "fall",
        "spring",
        "summer",
    )
    
    start = models.DateField()
    end = models.DateField()
    
    def is_in_term(self, test_date):
        if self.start < test_date < self.end:
            return True
        else:
            return False
    
    def get_type(self):
        term_year = self.end.year
        if self.is_in_term(date(term_year, 10, 1)): # if in november
            return self.TERM_TYPES[0] # fall term
        if self.is_in_term(date(term_year, 2, 1)): # if in february
            return self.TERM_TYPES[1] # spring term
        if self.is_in_term(date(term_year, 7, 1)): # if in july
            return self.TERM_TYPES[2] # summer term
    
    class Meta:
        ordering = ['-end']

    def __unicode__(self):
        return u"{0} {1}".format(self.get_type(), self.end.year)

class Location(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

class Building(Location):
    TYPES = (
        (0, 'Dormitory'),
        (1, 'Academic'),
        (2, 'Dining Hall'),
    )
    
    TYPES_LOOKUP = dict([(a[1], a[0]) for a in TYPES])
    
    name = models.CharField(max_length=32)
    shortname = models.SlugField(max_length=32)
    type = models.IntegerField(choices=TYPES)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Floor(models.Model):
    building = models.ForeignKey(Building)
    number = models.PositiveSmallIntegerField()

    def building_name(self):
        return self.building.name

    def get_number_display(self):
        if self.number == 0:
            return u'basement'
        else:
            return ordinal(self.number) + u' floor'

    __unicode__ = get_number_display

    class Meta:
        ordering = ('number',)

class RoomLocation(Location):
    floor = models.ForeignKey(Floor)
    number = models.CharField(max_length=8, help_text="room number in building numbering scheme")