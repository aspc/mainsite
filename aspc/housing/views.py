#from django.views.generic.date_based import archive_index
#from django.views.generic.list_detail import object_list
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import Http404
from annoying.decorators import render_to
from aspc.college.models import Building, Floor
from aspc.housing.models import Review, Room
from aspc.housing.forms import ReviewRoomForm, NewReviewForm, SearchForm, RefineForm

class Home(ArchiveIndexView):
    date_field = "create_ts"
    allow_empty = True
    queryset = Review.objects.all()

@render_to('housing/search.html')
def search(request):
    context = {'search_active': True,}
    if len(request.GET.keys()) > 0:
        form = RefineForm(request.GET)
        if form.is_valid():
            matching_rooms = Room.objects.all()
            if form.cleaned_data['buildings']:
                matching_rooms = matching_rooms.filter(floor__building__in=form.cleaned_data['buildings'])
            if form.cleaned_data['occupancy']:
                matching_rooms = matching_rooms.filter(occupancy__in=form.cleaned_data['occupancy'])
            if form.cleaned_data['size']:
                matching_rooms = matching_rooms.filter(size__gt=form.cleaned_data['size'])
            if form.cleaned_data['suite']:
                matching_rooms = matching_rooms.filter(suite__isnull=False, suite__occupancy__in=form.cleaned_data['suite'])
            context.update({'result_view': True, 'rooms': matching_rooms[:25],})
        else:
            context.update({'result_view': False,})
    else:
        form = SearchForm()
    context.update({'form': form,})
    return context

class BrowseBuildings(ListView):
    template_name = "housing/building_list.html"
    model = Building
    context_object_name = "buildings"
    
    def get_context_data(self, **kwargs):
        context = super(BrowseBuildings, self).get_context_data(**kwargs)
        context.update({'browse_active': True,})
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(type=Building.TYPES_LOOKUP['Dormitory'])

class BrowseBuildingFloor(ListView):
    model = Room
    context_object_name = "rooms"
    
    def get_queryset(self):
        building_shortname, floor_id = self.kwargs.get('building'), self.kwargs.get('floor')
        
        try:
            self.building = Building.objects.get(shortname=building_shortname)
        except ObjectDoesNotExist:
            raise Http404(u"There is no building called {0}".format(building_shortname))
        
        if floor_id is None:
            self.floor = self.building.floor_set.get(number=1)
        else:
            try:
                self.floor = Floor.objects.get(building=self.building, number=int(floor_id))
            except ObjectDoesNotExist:
                raise Http404(u"{0} has no floor #{1}".format(self.building))
        
        return self.model.objects.select_related().filter(floor=self.floor)
    
    def get_context_data(self, **kwargs):
        context = super(BrowseBuildingFloor, self).get_context_data(**kwargs)
        context.update({
            'floor': self.floor,
            'all_floors': self.building.floor_set.all(),
            'browse_active': True,
        })
        return context

class RoomDetail(DetailView):
    model = Room
    context_object_name = "room"
    
    def get_object(self, queryset=None):
        housing_set = queryset if queryset else self.get_queryset()
        building_shortname, floor, room_number = self.kwargs.get('building'), int(self.kwargs.get('floor', False)), self.kwargs.get('room', False)
        
        room = housing_set.filter(floor__number=floor, floor__building__shortname=building_shortname, number=room_number)
        try:
            obj = room.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name})
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(RoomDetail, self).get_context_data(**kwargs)
        context.update({'browse_active': True,})
        return context

class ReviewRoomWithChoice(CreateView):
    template_name = "housing/review_room_with_choice.html"
    model = Review
    form_class = NewReviewForm
    
    def get_context_data(self, **kwargs):
        context_data = super(ReviewRoomWithChoice, self).get_context_data(**kwargs)
        context_data.update({
            'review_active': True,
        })
        return context_data

class ReviewRoom(CreateView):
    form_class = ReviewRoomForm
    template_name = "housing/review_room.html"
    
    def get_context_data(self, **kwargs):
        context_data = super(ReviewRoom, self).get_context_data(**kwargs)
        context_data.update({
            'room': self.room,
            'review_active': True,
        })
        return context_data
    
    def get_form_kwargs(self):
        
        building_shortname, floor_id, room_number = self.kwargs.get('building'), int(self.kwargs.get('floor', False)), self.kwargs.get('room', False)
        
        try:
            self.building = Building.objects.get(shortname=building_shortname)
        except ObjectDoesNotExist:
            raise Http404(u"There is no building called {0}".format(building_shortname))
        
        try:
            self.floor = Floor.objects.get(building=self.building, number=int(floor_id))
        except:
            raise Http404(u"{0} has no floor #{1}".format(self.building))
        
        
        try:
            self.room = Room.objects.get(floor=self.floor, number=room_number)
        except ObjectDoesNotExist:
            raise Http404(u"{0} {1} has no room #{2}".format(self.building, self.floor, room_number))
        
        kwargs = super(ReviewRoom, self).get_form_kwargs()
        new_review = Review(room=self.room)
        kwargs.update({'instance': new_review,})
        print 'wat'
        #kwargs.update({'room_instance': self.room,})
        return kwargs
