from django.views.generic import ListView
from aspc.senate.models import Document

class DocumentList(ListView):
    model = Document
    context_object_name = 'documents'
    paginate_by = 20
