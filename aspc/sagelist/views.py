from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django import forms
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from aspc.sagelist.models import BookSale
from aspc.courses.models import Course
import string

class BookSaleForm(forms.ModelForm):
    class Meta:
        model = BookSale
        exclude = ('buyer', 'seller', 'posted', 'is_recoop', 'recoop_id')

class BookSearchForm(forms.Form):
    search = forms.CharField(initial="search")

class CreateBookSaleView(CreateView):
    form_class = BookSaleForm
    model = BookSale

    def form_valid(self, form):
        sale = form.save(commit=False)
        sale.title = sale.title.strip()
        sale.authors = sale.authors.strip()
        sale.seller = self.request.user
        sale.save()
        try:
            sale.update_amazon_info()
        except:
            pass
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

        if self.object.is_recoop:
            buyer_email_template = 'sagelist/recoop_purchase_complete_buyer.txt'
            seller_email_template = 'sagelist/recoop_purchase_complete_seller.txt'
        else:
            buyer_email_template = 'sagelist/purchase_complete_buyer.txt'
            seller_email_template = 'sagelist/purchase_complete_seller.txt'

        self.object.buyer.email_user(
            u"Purchase of {0} from {1}".format(
                self.object.title,
                self.object.seller.get_full_name()
            ),
            render_to_string(
                buyer_email_template,
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
                seller_email_template,
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


class ListUserBookSalesView(ListView):
    model = BookSale
    context_object_name = "listings"
    template_name = "sagelist/booksale_list_user.html"
    _user = None

    def get_context_data(self, *args, **kwargs):
        context = super(ListUserBookSalesView, self).get_context_data(*args, **kwargs)
        context.update({
            'listings_by': self._get_user(),
        })
        return context

    def _get_user(self):
        if not self._user:
            self._user = get_object_or_404(User, email__iexact=self.kwargs['email'])
        return self._user

    def get_queryset(self):
        qs = super(ListUserBookSalesView, self).get_queryset()
        qs = qs.filter(seller=self._get_user())
        return qs

class ListCourseBookSalesView(ListView):
    model = BookSale
    context_object_name = "listings"
    template_name = "sagelist/booksale_list_course.html"
    _course = None

    def get(self, request, *args, **kwargs):
        self._course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return super(ListCourseBookSalesView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ListCourseBookSalesView, self).get_context_data(*args, **kwargs)
        context.update({
            'course': self._course,
        })
        return context

    def get_queryset(self):
        qs = super(ListCourseBookSalesView, self).get_queryset()
        qs = qs.filter(course=self._course, buyer__isnull=True).order_by('title')
        return qs

class ListBookSalesView(ListView):
    model = BookSale
    context_object_name = "listings"
    paginate_by = 100

    def get_queryset(self):
        form = BookSearchForm(self.request.GET)

        qs = super(ListBookSalesView, self).get_queryset()
        qs = qs.filter(buyer__isnull=True).order_by('title')

        if form.is_valid():
            query = Q(title__icontains=form.cleaned_data['search'])
            query |= Q(authors__icontains=form.cleaned_data['search'])
            query |= Q(edition__icontains=form.cleaned_data['search'])
            query |= Q(isbn__icontains=form.cleaned_data['search'])
            qs = qs.filter(query)

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ListBookSalesView, self).get_context_data(*args, **kwargs)

        form = BookSearchForm(self.request.GET)
        if form.is_valid:
            context['form'] = form
            context['search'] = True
        else:
            context['form'] = BookSearchForm()
            context['search'] = False

        context['total_for_sale'] = self.model.objects.filter(buyer__isnull=True).count()
        context['total_sold'] = self.model.objects.filter(buyer__isnull=False).count()
        context['total'] = self.model.objects.count()
        return context
