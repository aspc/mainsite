from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
import datetime

class BusinessManager(models.Manager):
    def off_campus(self):
        return self.get_query_set().exclude(
            type=Business.TYPES_LOOKUP['On-Campus Restaurant']
        )
    
    def restaurants(self):
        return self.get_query_set().filter(
            type=Business.TYPES_LOOKUP['Restaurant']
        )
    
    def businesses(self):
        return self.get_query_set().exclude(
            type__in=[
                Business.TYPES_LOOKUP['Restaurant'],
                Business.TYPES_LOOKUP['On-Campus Restaurant'],
            ]
        )
    
    def on_campus(self):
        return self.get_query_set().filter(
            type=Business.TYPES_LOOKUP['On-Campus Restaurant']
        )

class Business(models.Model):
    """A local/on-campus business"""
    TYPES = (
        (0, "On-Campus Restaurant"),
        (1, "Restaurant"),
        (2, "Snacks & Treats"),
        (3, "Beauty and Health"),
        (4, "Apparel"),
        (5, "Groceries"),
        (6, "Other"),
    )
    TYPES_LOOKUP = dict([(b,a) for a,b in TYPES])
    
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPES)
    address = models.TextField()
    phone = PhoneNumberField(null=True, blank=True)
    description = models.CharField(
        max_length=127,
        help_text="The brief description for this business")
    discount = models.TextField(null=True, blank=True)
    www = models.URLField(null=True, blank=True)
    
    objects = BusinessManager()
    
    class Meta:
        ordering = ['name']
        verbose_name, verbose_name_plural = "business", "businesses"

    def __unicode__(self):
        return u"{0}".format(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('business_detail', [self.id])
    
    @property
    def is_open(self):
        """
        Is the business open now (aka is the current time within
        the hour range(s) for this weekday)?
        """
        weekday = datetime.date.today().strftime("%A").lower()
        query = {
            weekday: True,
            'begin__lte': datetime.datetime.now().time(),
            'end__gte': datetime.datetime.now().time(),
        }
        if self.hours.filter(**query).count():
            return True
        else:
            return False
    
    def has_discount(self):
        """Does this business have student discount information?"""
        return bool(self.discount)
    has_discount.boolean = True
    
    def formatted_hours(self):
        """
        Return business hours information with early morning hours
        presented as people would expect (i.e. Mon 4pm-1am instead of
        Mon 4pm-11:59pm + Tues 12am-1am)
        """
        almost_midnight = datetime.time(23,59) # end of the day
        midnight = datetime.time(0,0) # beginning of the day
        
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday']
        combined = {}
        
        # First, gather 'normal' hour ranges (not beginning at midnight)
        
        for day in weekdays:
            q = {day: True, 'begin__gt': midnight,}
            if self.hours.filter(**q).count():
                dayranges = combined.get(day, []) # get list of ranges to
                                                  # append to
                
                raw_ranges = self.hours.filter(**q).values_list('begin', 'end')
                
                for b, e in raw_ranges:
                    if e >= almost_midnight: # Clean midnight for display
                        dayranges.append((b, midnight))
                    else:
                        dayranges.append((b,e))
                combined[day] = dayranges
        
        for day_idx, day in enumerate(weekdays):
            q = {day: True, 'begin': midnight,}
            
            # If there's no period starting at midnight for this day, skip it
            if not self.hours.filter(**q).count(): continue
            
            # Otherwise, take end of said period and replace midnight end time
            # of previous day (if it exists)
            
            midnight_period = self.hours.filter(**q)[0]
            old_pd = combined[weekdays[day_idx - 1]][-1] # Last pd yesterday
            if old_pd[1] == midnight:
                new_pd = (old_pd[0], midnight_period.end)
                print new_pd
                combined[weekdays[day_idx - 1]][-1] = new_pd # Swap in new pd
        
        as_list = [(a, combined[a]) for a in weekdays]
        
        return as_list

class Hours(models.Model):
    business = models.ForeignKey(Business, related_name="hours")
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    begin = models.TimeField()
    end = models.TimeField()
    
    class Meta:
        ordering = ['begin', 'end']
        verbose_name, verbose_name_plural = "hours", "hours"
    
    def gen_days(self):
        s = []
        if self.monday: s.append('M')
        if self.tuesday: s.append('T')
        if self.wednesday: s.append('W')
        if self.thursday: s.append('R')
        if self.friday: s.append('F')
        if self.saturday: s.append('Sa')
        if self.sunday: s.append('Su')
        return s

    def __unicode__(self):
        return u'[%s] Open %s, %s-%s' % (
            self.business.name,
            ''.join(self.gen_days()),
            self.begin.strftime('%I:%M %p'),
            self.end.strftime('%I:%M %p')
        )
