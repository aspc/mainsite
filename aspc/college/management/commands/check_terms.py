from django.core.management.base import BaseCommand, CommandError
from aspc.college.models import Term

class Command(BaseCommand):
    args = ''
    help = 'ensures that the site has pre-populated the current ' \
           'and next academic terms'
    
    def handle(self, *args, **options):
        cur = Term.objects.current_term()
        next = Term.objects.next_term()
        all = list(Term.objects.order_by('end'))
        
        self.stdout.write("Current term: {0}\n".format(cur))
        self.stdout.write("Next term: {0}\n".format(next))
        self.stdout.write("Total: {0} terms from {1} to {2}\n".format(
            len(all),
            all[0],
            all[-1]
        ))