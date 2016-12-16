from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver
from .signals import new_activity, delete_activity


CATEGORY_CHOICES = (
    ('housing', 'Housing Reviews'),
    ('course', 'Course Reviews'),
    ('sagelist', 'SageBooks'),
    ('twitter', 'Twitter'),
)


class SocialMediaActivity(models.Model):
    date = models.DateTimeField()
    url = models.URLField()
    message = models.TextField()

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return self.url


class TwitterActivity(SocialMediaActivity):
    author = models.CharField(max_length=20)
    tweet_id = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(TwitterActivity, self).save(*args, **kwargs)
        if created:
            new_activity.send(sender=self, category="twitter", date=self.date)

    class Meta:
        ordering = ['-tweet_id']


class Activity(models.Model):
    date = models.DateTimeField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object = GenericForeignKey()

    class Meta:
        ordering = ['-date']


@receiver(new_activity)
def create_activity(sender, **kwargs):
    a = Activity(date=kwargs.get('date'), category=kwargs.get('category'), object=sender)
    a.save()


@receiver(delete_activity)
def delete_activity(sender, **kwargs):
    a = Activity.objects.filter(object_id=sender.pk)
    a.delete()