from django.core.management.base import BaseCommand
from django.conf import settings

from aspc.activityfeed.models import Activity, TwitterActivity


class Command(BaseCommand):
    help = 'clears recent tweets (for testing)'

    def handle(self, *args, **options):
        self.stdout.write("Deleting all Twitter SocialMediaActivity objects\n")
        self.stdout.flush()
        tweets = TwitterActivity.objects.all()
        activities = Activity.objects.filter(category="twitter")
        self.stdout.write("Deleting %i tweets, %i activity instances.\n" % (len(tweets), len(activities)))
        self.stdout.flush()
        tweets.delete()
        activities.delete()
