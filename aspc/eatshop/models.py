from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
import datetime

class BusinessManager(models.Manager):
    def off_campus(self):
        return self.get_query_set().exclude(type=Business.TYPES_LOOKUP['On-Campus Restaurant'])
    
    def on_campus(self):
        return self.get_query_set().filter(type=Business.TYPES_LOOKUP['On-Campus Restaurant'])

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
    address = models.TextField()
    phone = PhoneNumberField(null=True, blank=True)
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
        weekday = datetime.date.today().strftime("%A").lower()
        query = {
            weekday: True,
            'open__lt': datetime.datetime.now().time(),
            'close__gt': datetime.datetime.now().time(),
        }
        if self.hours.filter(**query).count():
            return True
        else:
            return False
    
    def has_discount(self):
        return bool(self.discount)

class Hours(models.Model):
    business = models.ForeignKey(Business, related_name="hours")
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    begin = models.TimeField()
    end = models.TimeField()

    def gen_days(self):
        s = []
        if self.monday: s.append('M')
        if self.tuesday: s.append('T')
        if self.wednesday: s.append('W')
        if self.thursday: s.append('R')
        if self.friday: s.append('F')
        return s

    def __unicode__(self):
        return u'[%s] Open %s, %s-%s' % (
            self.business.name,
            ''.join(self.gen_days()),
            self.begin.strftime('%I:%M %p'),
            self.end.strftime('%I:%M %p')
        )
