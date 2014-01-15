from django.db import models
from django.contrib.humanize.templatetags.humanize import ordinal
from django.contrib.auth.models import User
from stdimage import StdImageField
from aspc.college.models import Term, Location, Building, Floor, RoomLocation
from aspc.activityfeed.signals import new_activity, delete_activity

class Suite(models.Model):
    OCCUPANCY_TYPES = (
        (3, 'three person'),
        (4, 'four person'),
        (5, 'five person'),
        (6, 'six person'),
    )
    
    OCCUPANCY_LOOKUP = dict([(a[1], a[0]) for a in OCCUPANCY_TYPES])
    
    occupancy = models.IntegerField(choices=OCCUPANCY_TYPES, null=False, blank=False)

class RoomManager(models.Manager):
    def suite_from_rooms(self, rooms, occupancy_type):
        new_suite = Suite(occupancy=occupancy_type)
        new_suite.save()
        
        for room in rooms:
            room.suite = new_suite
            room.save()

class Room(RoomLocation):
    OCCUPANCY_TYPES = (
        (1, 'single'),
        (2, 'double'),
        (3, 'two room double'),
        (4, 'two room triple'),
    )
    
    BATHROOM_TYPES = (
        (0, 'shared (hall)'),
        (1, 'shared (2 person)'),
        (2, 'private'),
    )
    
    CLOSET_TYPES = (
        (0, 'free-standing'),
        (1, 'walk-in'),
        (2, 'bump out'),
    )
    
    RESERVATION_GROUPS = (
        (0, 'freshman housing'),
        (1, 'RHS'),
    )
    
    OCCUPANCY_LOOKUP = dict([(a[1], a[0]) for a in OCCUPANCY_TYPES])
    RESERVATION_LOOKUP = dict([(a[1], a[0]) for a in RESERVATION_GROUPS])
    
    size = models.FloatField(help_text="size in square feet", null=True, blank=True)
    occupancy = models.PositiveSmallIntegerField(choices=OCCUPANCY_TYPES, null=True, blank=True) # single, double, etc
    reserved = models.PositiveSmallIntegerField(choices=RESERVATION_GROUPS, null=True, blank=True)
    suite = models.ForeignKey(Suite, null=True, on_delete=models.SET_NULL, blank=True)
    #bathroom = models.PositiveSmallIntegerField(choices=BATHROOM_TYPES, default=BATHROOM_TYPES[0][0])
    #storage = models.PositiveSmallIntegerField(choices=CLOSET_TYPES, default=CLOSET_TYPES[1][0])
    #info = models.TextField(help_text="extra info from the housing office")
    objects = RoomManager()
    average_rating = models.FloatField(editable=False, null=True, blank=True)
    average_rating_quiet = models.FloatField(editable=False, null=True, blank=True)
    average_rating_spacious = models.FloatField(editable=False, null=True, blank=True)
    average_rating_temperate = models.FloatField(editable=False, null=True, blank=True)
    average_rating_maintained = models.FloatField(editable=False, null=True, blank=True)
    average_rating_cellphone = models.FloatField(editable=False, null=True, blank=True)
    
    
    def is_reserved(self):
        reservation = self.reserved.filter(term__end__gte=datetime.date.today())
        if reservation.count() != 1:
            return False
        else:
            return reservation[0].get_group_display()
    
    def get_suite_display(self):
        if not self.suite:
            return False
        else:
            return "{0} room suite".format(Room.objects.filter(suite=self.suite).count())
    
    def get_size_display(self):
        if self.size:
            return unicode(self.size)
        else:
            return u'?'
    
    def get_classes(self):
        classes = []
        
        if self.is_in_suite():
            classes.append(u'suite')
        res_type = self.is_reserved()
        if res_type:
            classes.append(u'reserved_{0}'.format(res_type))
        
        return ' '.join(classes)
    
    def get_name(self):
        return u'{0} {1}'.format(self.floor.building.name, self.number)
    get_name.short_description = 'number'
    
    def get_building(self):
        return self.floor.building.name
    get_building.admin_order_field = 'building'
    get_building.short_description = 'building'
    
    def update_average_rating(self):
        reviews = self.review_set.all()
        review_count = float(reviews.count())
        self.average_rating = sum(reviews.values_list('overall', flat=True)) / review_count
        self.average_rating_quiet = sum(reviews.values_list('quiet', flat=True)) / review_count
        self.average_rating_spacious = sum(reviews.values_list('spacious', flat=True)) / review_count
        self.average_rating_temperate = sum(reviews.values_list('temperate', flat=True)) / review_count
        self.average_rating_maintained = sum(reviews.values_list('maintained', flat=True)) / review_count
        self.average_rating_cellphone = sum(reviews.values_list('cellphone', flat=True)) / review_count
    
    __unicode__ = get_name
    
    @models.permalink
    def get_absolute_url(self):
        return ('housing_browse_room', [], {'building': self.floor.building.shortname, 'floor': self.floor.number, 'room': self.number})
    
    def get_data(self):
        return {
            'occupancy': self.get_occupancy_display(),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'number': self.number,
        }
    
    class Meta:
        ordering = ('number',)


class Review(models.Model):
    """A review of a room."""
    NOISY_QUIET = (
        (0, u"noisy"),
        (1, u"some noise"),
        (2, u"average"),
        (3, u"quieter than average"),
        (4, u"quiet"),
    )
    SMALL_SPACIOUS = (
        (0, u"cramped"),
        (1, u"small"),
        (2, u"adequate"),
        (3, u"roomy"),
        (4, u"spacious"),
    )
    HOT_COLD_TEMPERATE = (
        (0, u"too hot/cold"),
        (1, u"slightly uncomfortable"),
        (2, u"tolerable"),
        (3, u"comfortable"),
        (4, u"perfect"),
    )
    RUNDOWN_MAINTAINED = (
        (0, u"run-down"),
        (1, u"tatty"),
        (2, u"average"),
        (3, u"presentable"),
        (4, u"well maintained"),
    )
    PHONE_SERVICE = (
        (0, u"no cell service"),
        (1, u"some cell service"),
        (2, u"average  cell service"),
        (3, u"good cell service"),
        (4, u"excellent cell service"),
    )

    create_ts = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='posted at')
    room = models.ForeignKey(Room)
    author = models.ForeignKey(User, null=True, blank=True)
    overall = models.FloatField(editable=False)
    quiet = models.IntegerField(choices=NOISY_QUIET, blank=False, default=NOISY_QUIET[2][0])
    spacious = models.IntegerField(choices=SMALL_SPACIOUS, blank=False, default=SMALL_SPACIOUS[2][0])
    temperate = models.IntegerField(choices=HOT_COLD_TEMPERATE, blank=False, default=HOT_COLD_TEMPERATE[2][0])
    maintained = models.IntegerField(choices=RUNDOWN_MAINTAINED, blank=False, default=RUNDOWN_MAINTAINED[2][0])
    cellphone = models.IntegerField(choices=PHONE_SERVICE, blank=False, default=PHONE_SERVICE[2][0])
    best = models.TextField()
    worst = models.TextField()
    comments = models.TextField(blank=True)
    photo1 = StdImageField(blank=True, null=True, upload_to='housing/reviews/%Y/%m/%d/', size=(1000,700), thumbnail_size=(100,100))
    photo2 = StdImageField(blank=True, null=True, upload_to='housing/reviews/%Y/%m/%d/', size=(1000,700), thumbnail_size=(100,100))
    photo3 = StdImageField(blank=True, null=True, upload_to='housing/reviews/%Y/%m/%d/', size=(1000,700), thumbnail_size=(100,100))

    class Meta:
        ordering = ['-create_ts']


    def __unicode__(self):
        return u"Review of {0}".format(unicode(self.room))

    def get_overall_rating(self):
        return (self.quiet + self.spacious + self.temperate + self.maintained + self.cellphone) / 5.0

    def get_timestamp(self):
        return self.create_ts.strftime("%Y%m%d%H%M%S")

    def get_room(self):
        return self.room.get_name()
    get_room.short_description = "room"

    def update_overall(self):
        self.overall = float(self.quiet + self.spacious + self.temperate + self.maintained + self.cellphone) / 5.0

    def save(self, *args, **kwargs):
        created = self.pk is None
        self.update_overall()
        super(Review, self).save(*args, **kwargs)
        self.room.update_average_rating()
        self.room.save()
        if created:
            new_activity.send(sender=self, category="housing", date=self.create_ts)

    def delete(self, *args, **kwargs):
        delete_activity.send(sender=self)
        super(Review, self).delete(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('housing_browse_room', [], {'building': self.room.floor.building.shortname, 'floor': self.room.floor.number, 'room': self.room.number})

