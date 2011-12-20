import django_filters
from django import forms
from aspc.eatshop.models import Business

class OpenNowFilter(django_filters.Filter):
    field_class = forms.BooleanField
    
    def filter(self, qs, value):
        if not value:
            return qs
        else:
            # Query for currently open businesses lives
            # in manager class BusinessManager
            return Business.objects.open_now(qs) 

class OptionalChoiceFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        wildcard_label = kwargs.get('wildcard_label', u"All")
        try:
            choices = ((u"all", wildcard_label),) + kwargs['choices']
        except KeyError:
            raise RuntimeError("No choices provided for choice field!")
        kwargs['choices'] = choices
        super(OptionalChoiceFilter, self).__init__(*args, **kwargs)
    
    def filter(self, qs, value):
        if value is not None and value != u"all":
            return super(OptionalChoiceFilter, self).filter(qs, value)
        else:
            return qs

class StudentDiscountFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        if value is not None:
            q = {"{0}__iexact".format(self.name): u''}
            return qs.exclude(**q)
        else:
            return qs

class OnCampusFilterSet(django_filters.FilterSet):
    open_now = OpenNowFilter()
    claremont_cash = django_filters.BooleanFilter(label="ClaremontCash")
    
    class Meta:
        model = Business
        fields = ['claremont_cash', 'flex']

class RestaurantsFilterSet(django_filters.FilterSet):
    open_now = OpenNowFilter()
    claremont_cash = django_filters.BooleanFilter(label="ClaremontCash")
    discount = StudentDiscountFilter(label="Student discounts")
    
    class Meta:
        model = Business
        fields = ['discount', 'claremont_cash', 'flex']

class AllBusinessesFilterSet(django_filters.FilterSet):
    open_now = OpenNowFilter()
    claremont_cash = django_filters.BooleanFilter(label="ClaremontCash")
    discount = StudentDiscountFilter(label="Student discounts")
    type = OptionalChoiceFilter(choices=Business.TYPES)
    
    class Meta:
        model = Business
        fields = ['type', 'discount', 'claremont_cash', 'flex',]
