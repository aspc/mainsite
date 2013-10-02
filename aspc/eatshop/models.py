from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
import datetime
from aspc.eatshop.config import COOP_FOUNTAIN_ID
import hashlib
from django.utils.http import urlquote
from django.core.cache import cache

class BusinessManager(models.Manager):
    def off_campus(self, qs=None):
        """Off campus businesses of all types"""
        qs = qs or self.get_query_set()
        return qs.exclude(
            type=Business.TYPES_LOOKUP['On-Campus Restaurant']
        )

    def restaurants(self, qs=None):
        """Off-campus restaurants only"""
        qs = qs or self.get_query_set()
        return qs.filter(
            type=Business.TYPES_LOOKUP['Restaurant']
        )

    def non_food(self, qs=None):
        """Only businesses that aren't restaurants"""
        qs = qs or self.get_query_set()
        return qs.exclude(
            type__in=[
                Business.TYPES_LOOKUP['Restaurant'],
                Business.TYPES_LOOKUP['On-Campus Restaurant'],
            ]
        )

    def on_campus(self, qs=None):
        """Only on-campus restaurants"""
        qs = qs or self.get_query_set()
        return qs.filter(
            type=Business.TYPES_LOOKUP['On-Campus Restaurant']
        )

    def open_now(self, qs=None):
        """
        All businesses open now (aka is the current time within
        the hour range(s) for this weekday)?
        """
        qs = qs or self.get_query_set()
        weekday = datetime.date.today().strftime("%A").lower()
        query = {
            'hours__{0}'.format(weekday): True,
            'hours__begin__lte': datetime.datetime.now().time(),
            'hours__end__gte': datetime.datetime.now().time(),
        }
        return qs.filter(**query)

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
    description = models.TextField(help_text="Brief description for this business")
    claremont_cash = models.BooleanField()
    flex = models.BooleanField()
    discount = models.TextField(null=True, blank=True, verbose_name="student discount")
    www = models.URLField(null=True, blank=True)

    objects = BusinessManager()

    class Meta:
        ordering = ['name']
        verbose_name, verbose_name_plural = "business", "businesses"

    def __unicode__(self):
        return u"{0}".format(self.name)

    @models.permalink
    def get_absolute_url(self):
        if self.id == COOP_FOUNTAIN_ID:
            return ('coop_fountain', [])
        elif self.type == Business.TYPES_LOOKUP['On-Campus Restaurant']:
            return ('on_campus')
        elif self.type == Business.TYPES_LOOKUP['Restaurant']:
            return ('restaurants', [self.id])
        else:
            return ('businesses', [self.id])

    @property
    def is_open(self):
        if self.objects.open_now().filter(pk=self.pk).count():
            return True
        else:
            return False

    def has_discount(self):
        """Does this business have student discount information?"""
        return bool(self.discount)
    has_discount.boolean = True


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

    # Override this method to invalidate cached business template for the business that is being updated (saved)
    def save(self, *args, **kwargs):
        # Code extracted from django version 1.6: https://github.com/django/django/blob/master/django/core/cache/utils.py
        # When we upgrade to that version we can simply do "from django.core.cache import cache" and invoke this method

        TEMPLATE_FRAGMENT_KEY_TEMPLATE = 'template.cache.%s.%s'
        def make_template_fragment_key(fragment_name, vary_on=None):
            if vary_on is None:
                vary_on = ()
            key = ':'.join(urlquote(var) for var in vary_on)
            args = hashlib.md5(key)
            return TEMPLATE_FRAGMENT_KEY_TEMPLATE % (fragment_name, args.hexdigest())

        # Generates the appropriate key (a md5 hash, not just a string) and deletes it from the cache
        key = make_template_fragment_key('business_info_fragment', [self.business])
        cache.delete(key)

        super(Hours, self).save(*args, **kwargs)