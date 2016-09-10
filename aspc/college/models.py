from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import ordinal
from django.core.urlresolvers import reverse
from datetime import date
from geoposition.fields import GeopositionField

def _gen_termspecs(config=settings.ACADEMIC_TERM_DEFAULTS):
    """
    Returns a list of dates suitable for start/end of terms based on
    a dictionary of "name": (begin month, day), (end month, day) pairs.
    If one is not passed in, it uses settings.ACADEMIC_TERM_DEFAULTS
    """
    term_year = date.today().year
    termspecs = []
    
    # so really we only need one termspec added on either end, but we don't
    # know which until we've done the comparisons in the caller... just return
    # a few extras on either end
    for year in [term_year - 1, term_year, term_year + 1]:
        for name, (start_day, end_day) in config.items():
            ts = (date(year, *start_day), date(year, *end_day), name)
            termspecs.append(ts)
    
    if not len(termspecs):
        raise ImproperlyConfigured("At least one academic term must be "
            "defined under ACADEMIC_TERM_DEFAULTS in settings.py")
    
    termspecs.sort()
    return termspecs

class TermManager(models.Manager):
    def current_term(self):
        """
        Retrieve (or create if missing) the current academic term (n.b. this 
        could be the most recently concluded term based on the way terms are
        matched)
        """
        
        termspecs = _gen_termspecs()
        termspecs.reverse() # we want the furthest future dates first
        
        today = date.today()
        
        for begin, end, name in termspecs:
            if begin <= today:
                current_begin, current_end = begin, end
                break
        
        try:
            current_term = self.get_query_set().get(
                start__gte=current_begin,
                end__lte=current_end
            )
        except self.model.DoesNotExist:
            current_term = self.model(start=current_begin, end=current_end)
            current_term.save()
        
        return current_term
    
    def next_term(self):
        """ Retrieve (or create if missing) the next academic term """
        
        current = self.current_term()
        future = self.get_query_set()\
                     .order_by('start')\
                     .filter(start__gte=current.end)
        
        if future.count():
            # Next term exists, hooray
            return future[0]
        
        # No next term, must generate it
        termspecs = _gen_termspecs()
        
        for begin, end, name in termspecs:
            if begin >= current.end:
                next_begin, next_end = begin, end
                break
        
        # Create a new term with the begin/end we got
        
        next_term = self.model(start=next_begin, end=next_end)
        next_term.save()
        
        return next_term

class Term(models.Model):
    """Representing an academic term (e.g. Fall 2012)"""
    
    TERM_TYPES = (
        "fall",
        "spring",
        "summer",
    )
    
    start = models.DateField()
    end = models.DateField()
    
    objects = TermManager()
    
    def is_in_term(self, test_date):
        if self.start < test_date < self.end:
            return True
        else:
            return False
    
    def get_type(self):
        term_types = settings.ACADEMIC_TERM_DEFAULTS.items()
        term_year = self.end.year
        for name, (start_day, end_day) in term_types:
            start, end = (date(term_year, *start_day), date(term_year, *end_day))
            if start <= self.start and end >= self.end:
                return name
        return "N/A"
    
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
    type = models.IntegerField(choices=TYPES, db_index=True)
    position = GeopositionField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
    
    def get_map_info(self):
        data = {}
        data['shortname'] = self.shortname
        data['floors'] = []
        for floor in self.floor_set.all():
            for map in floor.map_set.all():
                data['floors'].append((unicode(floor.number), map.image.url))
        data['bounds'] = {
            'ne': (self.floor_set.all()[0].map_set.all()[0].n, self.floor_set.all()[0].map_set.all()[0].e),
            'sw': (self.floor_set.all()[0].map_set.all()[0].s, self.floor_set.all()[0].map_set.all()[0].w),
        }
        return data

    def map_object(self):
        if not self.position:
            return {}
        return {
            'name': self.name,
            'position': {'lat':float(self.position.latitude), 'lng': float(self.position.longitude or 0)},
            'review_url': reverse('housing_browse_building_floor_first', kwargs={'building': self.shortname})
        }

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
    
    def get_data(self):
        data = {
            'number': self.number,
            'number_display': self.get_number_display(),
#            'map': self.map.get_data(),
        }
        return data

    class Meta:
        ordering = ('number',)


class Map(models.Model):
    image = models.FileField(upload_to='maps/')
    n = models.FloatField()
    e = models.FloatField()
    s = models.FloatField()
    w = models.FloatField()
    floor = models.OneToOneField(Floor)
    
    def get_building(self):
        return self.floor.building.name
    
    def get_data(self):
        return {
            'url': self.image.url,
            'n': self.n,
            'e': self.e,
            's': self.s,
            'w': self.w,
        }
    
    def __unicode__(self):
        return "Map for {0}".format(self.get_building())

class RoomLocation(Location):
    floor = models.ForeignKey(Floor)
    number = models.CharField(max_length=8, help_text="room number in building numbering scheme")
