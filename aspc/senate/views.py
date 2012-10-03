from django.views.generic import ListView
from aspc.senate.models import Document, Appointment
import datetime

class DocumentList(ListView):
    model = Document
    context_object_name = 'documents'
    paginate_by = 20

class AppointmentList(ListView):
    model = Appointment
    context_object_name = 'appointments'
    
    def get_queryset(self, *args, **kwargs):
        qs = super(AppointmentList, self).get_queryset(*args, **kwargs)
        qs.filter(end__isnull=True)
        qs |= qs.filter(end__gte=datetime.datetime.now())
        qs = qs.order_by('position__sort_order')
        return qs
    