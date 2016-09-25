from django.views.generic import ListView
from aspc.senate.models import Document, Appointment, Position
from aspc.senate.models import COMMITTEE_CHOICES
from django.db.models import Q
import datetime

class DocumentList(ListView):
    model = Document
    context_object_name = 'documents'
    paginate_by = 20

class AppointmentList(ListView):
    model = Appointment
    context_object_name = 'appointments'

    def get_context_data(self, **kwargs):
        context = super(AppointmentList, self).get_context_data(**kwargs)
        context['committee'] = dict(COMMITTEE_CHOICES).get(self.kwargs['committee'])
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AppointmentList, self).get_queryset(*args, **kwargs)
        return qs\
            .filter(position__committee=self.kwargs['committee'])\
            .filter(Q(end__isnull=True) | Q(end__gte=datetime.datetime.now()))

class PositionList(ListView):
    model = Position
    context_object_name = 'positions'

    def get_queryset(self, *args, **kwargs):
        all_qs = super(PositionList, self).get_queryset(*args, **kwargs)
        qs = all_qs.filter(active=True)
        return qs
