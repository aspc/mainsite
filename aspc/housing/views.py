#from django.views.generic.date_based import archive_index
#from django.views.generic.list_detail import object_list
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.utils import simplejson as json
from django.conf import settings
import time
from itertools import groupby
from aspc.college.models import Building, Floor, Map
from aspc.housing.models import Review, Room
from aspc.housing.forms import ReviewRoomForm, NewReviewForm, SearchForm, RefineForm, SEARCH_ORDERING

class Home(ArchiveIndexView):
    template_name = "housing/home.html"
    date_field = "create_ts"
    allow_empty = True
    queryset = Review.objects.all()
    paginate_by = 15

def format_data(rooms):
    sorted_rooms = sorted(rooms, key=lambda r: r.floor.id)
    grouped_rooms = groupby(sorted_rooms, lambda room: room.floor)
    floors = []
    for floor, f_rooms in grouped_rooms:
        try:
            room_data = [r.get_data() for r in f_rooms]
        except AttributeError:
            room_data = [r.room.get_data() for r in f_rooms]
        floor_data = {
            'floor': floor.get_data(),
            'rooms': room_data,
        }
        floors.append(floor_data)
    return floors

def most_rooms(room_set):
    floors = {}
    for r in room_set:
        number = r.floor.get_number_display()
        if number in floors.keys():
            floors[number] += 1
        else:
            floors[number] = 1
    sortable = [(a[1], a[0]) for a in floors.items()]
    sortable.sort()
    sortable.reverse()
    return sortable[0][1]


def calculate_map(matching_rooms):
    lats = []
    longs = []
    for a in matching_rooms:
        if a.latitude and a.longitude:
            lats.append(a.latitude)
            longs.append(a.longitude)
    if len(lats) == 0: # empty results, or no map locations
        center_latitude = 34.096987 # geocoded location for Pomona College
        center_longitude = -117.711575
        zoom_level = 14 # use largest map
        initial_json = mark_safe(json.dumps({}))
    else:
        center_latitude = sum(lats) / len(lats)
        center_longitude = sum(longs) / len(longs)
        spread_latitude = max(lats) - min(lats)
        spread_longitude = max(longs) - min(longs)

        # determine zoom
        spread_factor = ((spread_latitude + spread_longitude) / 2.0) * 10000.0
        
        if spread_factor > 30.0:
            zoom_level = 14
        elif spread_factor > 20.0:
            zoom_level = 16
        elif spread_factor > 10.0:
            zoom_level = 18
        else:
            zoom_level = 19
        
        initial_json = mark_safe(json.dumps(most_rooms(matching_rooms)))
    
    # serialize map data

    results_data = format_data(matching_rooms)
    results_data_json = mark_safe(json.dumps(results_data))
    
    return {
        'results_data': results_data_json,
        'initial': initial_json,
        'center_latitude': center_latitude,
        'center_longitude': center_longitude,
        'zoom_level': zoom_level,
    }

def search(request):
    context = {'search_active': True,}
    if len(request.GET.keys()) > 0:
        form = RefineForm(request.GET)
        if form.is_valid():
            
            matching_rooms = Room.objects.all()
            matching_rooms = matching_rooms.select_related('floor', 'floor__building', 'roomlocation')
            
            # build ordering clause
            on_fields = SEARCH_ORDERING[form.cleaned_data['prefer']][0]
            print on_fields
            ordering = []
            select_nulls = {}
            
            for f in on_fields:
                ordering.extend(['{0}_null'.format(f), '-{0}'.format(f)])
                select_nulls['{0}_null'.format(f)] = '{0} is NULL'.format(f)
            print ordering
            print select_nulls
            matching_rooms = matching_rooms.extra(select=select_nulls, order_by=ordering)
            
            if form.cleaned_data['buildings']:
                matching_rooms = matching_rooms.filter(floor__building__in=form.cleaned_data['buildings'])
            if form.cleaned_data['occupancy']:
                matching_rooms = matching_rooms.filter(occupancy__in=form.cleaned_data['occupancy'])
            if form.cleaned_data['size']:
                matching_rooms = matching_rooms.filter(size__gt=form.cleaned_data['size'])
            # if form.cleaned_data['suite']:
            #     matching_rooms = matching_rooms.filter(suite__isnull=False, suite__occupancy__in=form.cleaned_data['suite'])
            
            print str(matching_rooms.query)
            
            paginator = Paginator(matching_rooms, per_page=50, orphans=10)
            GET_data = request.GET.copy()
            
            try:
                page = int(request.GET.get('page', '1'))
                if GET_data.get('page', False):
                    del GET_data['page']
            except ValueError:
                page = 1
            
            try:
                results = paginator.page(page)
            except (EmptyPage, InvalidPage):
                results = paginator.page(paginator.num_pages)
            
            context.update(calculate_map(results.object_list))
            context.update({
                'result_view': True,
                'results': results,
                'rooms': results.object_list,
                'path': ''.join([request.path, '?', GET_data.urlencode()]),
            })
        else:
            context.update({'result_view': False,})
    else:
        form = SearchForm()
    context.update({'form': form,})
    return render(request, 'housing/search.html', context)

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
        
        context.update(calculate_map(self.get_queryset().select_related('room', 'floor')))
        
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
            raise Http404(u"No %(verbose_name)s found matching the query" %
                {'verbose_name': housing_set.model._meta.verbose_name})
        return obj
    
    def get_context_data(self, **kwargs):
        map_data = self.object.floor.map.get_data()
        room_data = self.object.get_data()
        room_data.update({'map': map_data})
        room_data_json = mark_safe(simplejson.dumps(room_data))
        context = super(RoomDetail, self).get_context_data(**kwargs)
        context.update({'browse_active': True, 'id': self.object.id, 'room_json': room_data_json})
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
