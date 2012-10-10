from django.db import models
from django.contrib.auth.models import User, Group
import datetime

class Position(models.Model):
    """A position in ASPC (elected, appointed, or hired)"""
    
    title = models.CharField(
        max_length=80,
        help_text="The official title of the position")
    email = models.EmailField(blank=True, null=True)
        
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
    groups = models.ManyToManyField(
        Group,
        help_text="Groups that people holding this position should be added "
                  "to assign the correct permissions.",
        blank=True,
    )
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
        if self.sort_order is None:
            positions = Position.objects.order_by('-sort_order')
            if not positions.count():
                self.sort_order = 1
            else:
                self.sort_order = positions[0].sort_order + 1
        super(Position, self).save(*args, **kwargs)

class Appointment(models.Model):
    """Information on the start and end dates of a particular ASPC position"""
    
    position = models.ForeignKey(Position)
    name = models.CharField(max_length=40, help_text="The name to display "
        "on the Senate Positions page")
    login_id = models.CharField(max_length=20, blank=True, null=True)
    
    user = models.ForeignKey(User, blank=True, null=True)
    
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['start', 'position']

    def __unicode__(self):
        return u"{0}: {1} from {2} to {3}".format(
            self.position.title,
            self.name,
            self.start,
            self.end)
    
    def save(self, *args, **kwargs):
        if self.user:
            self.login_id = self.user.username
        return super(Appointment, self).save(*args, **kwargs)

# Watch for user logins to make sure they have the permissions their position
# requires

from django.contrib.auth.signals import user_logged_in

def sync_permissions(sender, user, request, **kwargs):
    # First clear expired permissions, then (re)add active permissions
    
    # Does the user have one or more expired appointments?
    expired_appts = Appointment.objects.filter(
        user=user,
        end__lte=datetime.date.today(),
    )
    
    for appt in expired_appts:
        user.groups.remove(*tuple(appt.position.groups.all()))
    user.is_staff = False
    
    # Does the user have one or more current appointments?
    appts = Appointment.objects.filter(
        start__lte=datetime.date.today(),
        end__gte=datetime.date.today(),
    )
    
    # note: some appointments have no end date (i.e. staff advisors)
    appts |= Appointment.objects.filter(
        start__lte=datetime.date.today(),
        end__isnull=True
    )
    
    appts_active = appts.filter(login_id=user.username)
    appts_active |= appts.filter(user__username=user.username)
    
    for appt in appts_active:
        print appt, 'is active'
        appt.user = user
        appt.save()
        
        # One side effect of this is that users will not be removed from a 
        # group just because their position has been removed from a group
        user.groups.add(*tuple(appt.position.groups.all()))
    
    if appts_active:
        user.is_staff = True
    
    user.save()

user_logged_in.connect(sync_permissions)

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
