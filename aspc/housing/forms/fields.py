from django import forms
from aspc.college.models import Building
from aspc.housing.models import Room
from django.forms.fields import MultiValueField
from aspc.housing.forms.widgets import RoomSelectionWidget
from django.core.exceptions import ValidationError

class RoomField(MultiValueField):
    def __init__(self, *args, **kwargs):
        self.buildings = tuple(Building.objects.filter(type=Building.TYPES_LOOKUP['Dormitory']).order_by('name').values_list('shortname', 'name'))
        unsorted_room_numbers = Room.objects.order_by('number').values_list('number', flat=True).distinct()
        # So rooms aren't sorted by number, since they are strings, leading to unintuitive behavior
        # Re-sort them by their nearest integer values
        temp_room_numbers = []
        for a in unsorted_room_numbers:
            clean = filter(unicode.isdigit, a)
            if clean:
                int_out = int(clean)
            else:
                int_out = 0
            temp_room_numbers.append((int_out, a))
        temp_room_numbers.sort()
        self.room_numbers = [a[1] for a in temp_room_numbers]
        building_field = forms.ChoiceField(choices=self.buildings)
        room_number_field = forms.CharField()#choices=enumerate(self.room_numbers))
        kwargs.update({'fields': (building_field, room_number_field,),})
        if not 'widget' in kwargs.keys():
            kwargs.update({
                'widget': RoomSelectionWidget(buildings=self.buildings),
            })
        super(RoomField, self).__init__(*args, **kwargs)
    
    def compress(self, data_list):
        building_name, room_number = data_list
        print data_list
        try:
            room = Room.objects.get(floor__building__shortname=building_name, number=room_number)
        except:
            raise ValidationError(u'Room does not exist')
        return room