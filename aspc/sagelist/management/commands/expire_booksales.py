from django.core.management.base import BaseCommand
from optparse import make_option
from django.template.loader import render_to_string

from aspc.sagelist.models import BookSale
from datetime import datetime, timedelta

class Command(BaseCommand):
    args = '[max age in days, default: 6*30]'
    help = 'expires booksales'
    option_list = BaseCommand.option_list + (
                    make_option('--silent',
                        action='store_true',
                        dest='silent',
                        default=False,
                        help='Do not email users when their booksale expires'),
                    make_option('--fake',
                        action='store_true',
                        dest='fake',
                        default=False,
                        help='Do not actually delete booksales or send emails'),
                  )

    def handle(self, *args, **options):
        if len(args) > 0:
            max_age_in_days = int(args[0])
        else:
            max_age_in_days = 6 * 30

        self.stdout.write('Running with: silent = {0}, fake = {1}, max_age_in_days = {2}'.format(
            options['silent'], options['fake'], max_age_in_days))

        dtnow = datetime.now()
        cutoff_oldest_posted = dtnow - timedelta(days=max_age_in_days)
        old_booksales = BookSale.objects.filter(posted__lt=cutoff_oldest_posted)
        self.stdout.write('Found {0} old booksales.'.format(len(old_booksales)))

        for booksale in old_booksales:
            age = (dtnow - booksale.posted).days
            self.stdout.write('[{0} days old] {1} from {2}'.format(
                age, booksale.title.encode('ascii', 'replace'), booksale.seller.username
            ))
            
                
            if not options['silent']:
                email_subject = u"SageBooks listing expired: {0}".format(booksale.title)
                email_content = render_to_string(
                                    'sagelist/listing_expired.txt',
                                    {
                                        'title': booksale.title.encode('utf8'),
                                        'seller': booksale.seller.get_full_name().encode('utf8')
                                    },
                                )
                self.stdout.write("Preparing an email to {0} [{1}]".format(booksale.seller, booksale.seller.email))
                self.stdout.write("--> subject: {0}".format(email_subject))
                self.stdout.write("--> content: {0}".format(email_content))
                if not options['fake']:
                    booksale.seller.email_user(email_subject, email_content)
                    self.stdout.write("Email sent.")
            
            if not options['fake']:
                booksale.delete()
                self.stdout.write("BookSale deleted.")
            
            self.stdout.write('\n')

