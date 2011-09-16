from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.forms import ModelForm
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from aspc.sagelist.models import BookSale
import string

class BookSaleForm(ModelForm):
    class Meta:
        model = BookSale
        exclude = ('buyer', 'seller', 'posted')

class CreateBookSaleView(CreateView):
    form_class = BookSaleForm
    model = BookSale
    
    def form_valid(self, form):
        sale = form.save(commit=False)
        sale.seller = self.request.user
        sale.save()
        sale.seller.email_user(
            u"Posted {0} on SageList".format(sale.title),
            render_to_string(
                'sagelist/new_listing.txt',
                {'seller': sale.seller, 'booksale': sale,},
                context_instance=RequestContext(self.request)
            )
        )
        messages.add_message(self.request, messages.SUCCESS, "Successfully listed {0} for sale".format(sale.title))
        return super(CreateBookSaleView, self).form_valid(form)


class BookSaleDetailView(DetailView):
    model = BookSale
    context_object_name = "book"
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.seller == request.user:
            return HttpResponseRedirect(reverse('sagelist_detail', kwargs={'pk': self.object.pk,}))
        self.object = self.get_object()
        self.object.buyer = request.user
        
        email_context = {
            'seller': self.object.seller,
            'buyer': self.object.buyer,
            'booksale': self.object,
        }
        
        self.object.buyer.email_user(
            u"Purchase of {0} from {1}".format(
                self.object.title,
                self.object.seller.get_full_name()
            ),
            render_to_string(
                'sagelist/purchase_complete_buyer.txt',
                email_context,
                context_instance=RequestContext(self.request)
            )
        )
        
        self.object.seller.email_user(
            u"Sale of {0} to {1}".format(
                self.object.title,
                self.object.buyer.get_full_name()
            ),
            render_to_string(
                'sagelist/purchase_complete_seller.txt',
                email_context,
                context_instance=RequestContext(self.request)
            )
        )
        
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, u"Purchased {0}. An email has been sent to you and the seller.".format(self.object.title))
        return self.get(request, *args, **kwargs)

class BookSaleDeleteView(DeleteView):
    model = BookSale
    context_object_name = "book"
    
    def get_success_url(self):
        return reverse('sagelist')
    
    def get_object(self, *args, **kwargs):
        object = super(BookSaleDeleteView, self).get_object(
            *args, **kwargs)
        if object.seller != self.request.user:
            raise Http403("Only the seller of a book or an administrator may"
                " delete a listing")
        return object
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.seller == request.user:
            self.object.delete()
            messages.add_message(request, messages.SUCCESS, u"Deleted listing for {0}".format(self.object.title))
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.get(request, *args, **kwargs)

class ListBookSalesView(ListView):
    model = BookSale
    context_object_name = "listings"
    
    def get_queryset(self):
        qs = super(ListBookSalesView, self).get_queryset()
        qs = qs.filter(buyer__isnull=True)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super(ListBookSalesView, self).get_context_data(*args, **kwargs)
        groups = {}
        for l in string.uppercase:
            groups[l] = []
        
        for b in self.object_list:
            groups[b.title[0].upper()].append(b)
        context['listings_grouped'] = groups.items()
        context['listings_grouped'].sort()
        return context
