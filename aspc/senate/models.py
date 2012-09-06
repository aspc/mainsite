from django.db import models
from django.contrib.auth.models import User, Group
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
    groups = models.ManyToManyField(
        Group,
        help_text="Groups that people holding this position should be added "
                  "to for permissions reasons"
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
    login_id = models.CharField(max_length=20, blank=True, null=True)
    
    user = models.ForeignKey(User, blank=True, null=True)
    
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

# Watch for user logins to make sure they have the permissions their position
# requires

from django.contrib.auth.signals import user_logged_in

def sync_permissions(sender, user, request, **kwargs):
    try:
        # Does the user have an active appointment?
        appt = Appointment.objects.get(
            login_id=user.username,
            start__lte=datetime.date.today(),
            end__gte=datetime.date.today(),
        )
        appt.user = user
        
        # One side effect of this is that users will not be removed from a 
        # group just because their position has been removed from a group
        user.groups.add(list(appt.position.groups.all()))
        
        appt.save()
    except Appointment.DoesNotExist:
        # No current appointment for this user
        pass
    
    try:
        # Does the user have an expired appointment?
        appt = Appointment.objects.get(
            user=user,
            end__lte=datetime.date.today(),
        )
    except Appointment.DoesNotExist:
        
    

user_logged_in.connect(sync_permissions)