from django.db import models
from django.contrib.auth.models import User
import datetime

class Position(models.Model):
    """A position in ASPC (elected, appointed, or hired)"""
    
    title = models.CharField(
        max_length=80,
        help_text="The official title of the position")
    description = models.TextField(
        blank=True,
        help_text="(optional) Description of the position")
    appointments = models.ManyToManyField(
        User,
        through="Appointment",
        help_text="Current and past appointees to this position")
    active = models.BooleanField(
        default=True,
        help_text="Whether or not a position is still active (for display "
                  "in the list of Senate positions)")
    sort_order = models.PositiveSmallIntegerField(
        blank=True,
        help_text="Sort ordering")
    
    class Meta:
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title
    
    def current_appointee(self):
        appts = self.appointments.filter(start__lte=datetime.date.today())
        appts = (
            appts.filter(end__isnull=True) | 
            appts.filter(end__gte=datetime.date.today())
        )
        if appts.count():
            return appts[0]
        else:
            return none
    
    def save(self, *args, **kwargs):
        if not self.sort_order:
            positions = Position.objects.order_by('-sort_order')
            if not positions.count():
                self.sort_order = 1
            else:
                self.sort_order = positions[0].sort_order + 1
        super(Position, self).save(*args, **kwargs)

class Appointment(models.Model):
    """Information on the start and end dates of a particular ASPC position"""
    
    position = models.ForeignKey(Position)
    user = models.ForeignKey(User)
    
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['start', 'position']

    def __unicode__(self):
        return u"{0}: {1} from {2} to {3}".format(
            self.position.title,
            self.user.get_full_name(),
            self.start,
            self.end)

class Document(models.Model):
    """A publication of the Senate, such as a report"""
    
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey('auth.User')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    authors = models.TextField(blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='senate/documents/%Y/%m/%d/')
    
    class Meta:
        ordering = ['uploaded_at', 'title']
    
    def get_absolute_url(self):
        return self.file.url
    
    def __unicode__(self):
        return '{filename} uploaded by {user} on {datetime}'.format(
            filename=self.file.name,
            user=self.uploaded_by.username,
            datetime=self.uploaded_at,
        )
