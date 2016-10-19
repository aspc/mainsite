from django.core.management.base import BaseCommand
from aspc.courses.models import Schedule
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from aspc.settings import EMAIL_HOST_USER

# Assume we send the emails at the end of the semester, we
# should only consider schedules that are at least 3 months old
MIN_DAYS = 90
MAX_DAYS = 300
EMAIL_TITLE = "Have you taken these classes?"

class Command(BaseCommand):
    args = ''
    help = 'imports terms'

    def handle(self, *args, **options):
        plaintext = get_template('email/solicit_reviews.txt')
        htmly     = get_template('email/solicit_reviews.html')
        schedules = Schedule.objects.filter(create_ts__lte=datetime.now()-timedelta(days=MIN_DAYS),
                                            create_ts__gte=datetime.now()-timedelta(days=MAX_DAYS))
        emails_sent = 0
        for schedule in schedules:
            try:
                context = Context({'user': schedule.user, 'courses': schedule.sections.all()})
                text_content = plaintext.render(context)
                html_content = htmly.render(context)
                user_data = schedule.user.user.all()
                if user_data and user_data[0].subscribed_email:
                    msg = EmailMultiAlternatives(EMAIL_TITLE, text_content, EMAIL_HOST_USER, [schedule.user.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    emails_sent += 1
            except Exception as e:
                self.stdout.write('Error: %s\n' % e)
        self.stdout.write('Successfully send %s emails\n' % emails_sent)

