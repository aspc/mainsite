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
from functools import wraps
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
            u"Posted {0} on SageBooks".format(sale.title),
            render_to_string(
                'sagelist/new_listing.txt',
                {'seller': sale.seller, 'booksale': sale,},
                context_instance=RequestContext(self.request)
            )
        )
        messages.add_message(self.request, messages.SUCCESS, u"Successfully listed {0} for sale".format(sale.title))
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
    
    class AccessDenied(Exception):
        pass
    
    def get_success_url(self):
        return reverse('sagelist')
    
    def user_can_delete(self):
        return (self.get_object().seller == self.request.user or
                self.request.user.has_perm('sagelist.delete_booksale'))
    
    def dispatch(self, *args, **kwargs):
        try:
            return super(BookSaleDeleteView, self).dispatch(*args, **kwargs)
        except BookSaleDeleteView.AccessDenied:
            return HttpResponseForbidden("Only the seller or an administrator may delete this listing")
    
    def get_object(self):
        obj = super(BookSaleDeleteView, self).get_object()
        if not (obj.seller == self.request.user or
                self.request.user.has_perm('sagelist.delete_booksale')):
            raise BookSaleDeleteView.AccessDenied
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, u"Deleted listing for {0}".format(self.object.title))
        return HttpResponseRedirect(self.get_success_url())


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
        for l in string.uppercase + '#':
            groups[l] = []
        
        for b in self.object_list:
            if b.title[0].upper() in groups.keys():
              groups[b.title[0].upper()].append(b)
            else:
              groups['#'].append(b)
        context['listings_grouped'] = groups.items()
        context['listings_grouped'].sort()
        context['total_for_sale'] = self.get_queryset().count()
        context['total_sold'] = self.model.objects.filter(buyer__isnull=False).count()
        context['total'] = self.model.objects.count()
        return context
