from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import widgets
from aspc.college.models import Building
from aspc.housing.models import Review, Room, Suite
from aspc.housing.forms.fields import RoomField
from aspc.housing.forms.widgets import ColumnCheckboxSelectMultiple, RatingRadioFieldRenderer
from django.utils.safestring import mark_safe

rating_widgets = {
            'quiet': widgets.RadioSelect(renderer=RatingRadioFieldRenderer),
            'spacious': widgets.RadioSelect(renderer=RatingRadioFieldRenderer),
            'temperate': widgets.RadioSelect(renderer=RatingRadioFieldRenderer),
            'maintained': widgets.RadioSelect(renderer=RatingRadioFieldRenderer),
            'cellphone': widgets.RadioSelect(renderer=RatingRadioFieldRenderer),
            'best': widgets.Textarea(attrs={'rows':5, 'cols':60,}),
            'worst': widgets.Textarea(attrs={'rows':5, 'cols':60,}),
            'comments': widgets.Textarea(attrs={'rows':5, 'cols':60,}),
        }

class CustomImageField(forms.ImageField):
    def clean(self, data, initial):
        f = super(CustomImageField, self).clean(data)
        if f:
            (w, h) = get_image_dimensions(f)
            if w > 500 or h > 500:
                raise forms.ValidationError((u'Image is too large. The height and width must be no greater than 500px.' ))
        return f


class ReviewRoomForm(forms.ModelForm):
    photo1 = CustomImageField(required=False)
    photo2 = CustomImageField(required=False)
    photo3 = CustomImageField(required=False)

    class Meta:
        model = Review
        exclude = ('create_ts', 'room')
        widgets = rating_widgets


class NewReviewForm(ReviewRoomForm):
    room = RoomField()


SEARCH_ORDERING = (
    (('average_rating',), "highest rated"),
    (('size', 'average_rating_spacious'), "largest"),
    (('average_rating_quiet',), "quietest"),
    (('average_rating_temperate',), "most temperate"),
    (('average_rating_maintained',), "best condition"),
    (('average_rating_cellphone',), "best cell reception"),
)

ORDERING_CHOICES = tuple(enumerate((a[1] for a in SEARCH_ORDERING)))

class SearchForm(forms.Form):
    prefer = forms.TypedChoiceField(choices=ORDERING_CHOICES, coerce=int, empty_value=(), help_text="rooms first")
    buildings = forms.ModelMultipleChoiceField(
        queryset=Building.objects.filter(type=Building.TYPES_LOOKUP['Dormitory']),
        required=False,
        widget=ColumnCheckboxSelectMultiple(columns=3, css_class="col buildings"),
    )
    size = forms.FloatField(required=False, help_text="square feet or larger")
    occupancy = forms.TypedMultipleChoiceField(
        choices=Room.OCCUPANCY_TYPES,
        required=False,
        widget=ColumnCheckboxSelectMultiple(columns=2, css_class="col"),
        coerce=int,
        empty_value=(),
    )


class RefineForm(forms.Form):
    prefer = forms.TypedChoiceField(choices=ORDERING_CHOICES, coerce=int, empty_value=(), help_text="rooms first")
    buildings = forms.ModelMultipleChoiceField(
        queryset=Building.objects.filter(type=Building.TYPES_LOOKUP['Dormitory']),
        required=False,
        widget=ColumnCheckboxSelectMultiple(columns=2, css_class="col buildings"),
    )
    size = forms.FloatField(required=False, help_text=mark_safe("ft<sup>2</sup> or larger"))
    occupancy = forms.TypedMultipleChoiceField(
        choices=Room.OCCUPANCY_TYPES,
        required=False,
        widget=ColumnCheckboxSelectMultiple(columns=2, css_class="col"),
        coerce=int,
        empty_value=(),
    )

class RaffleForm(forms.Form):
    start_date = forms.DateField(widget=widgets.DateInput(attrs={
        'placeholder': 'YYYY-MM-DD',
    }))
    end_date = forms.DateField(widget=widgets.DateInput(attrs={
        'placeholder': 'YYYY-MM-DD',
    }))
    num_winners = forms.IntegerField(initial=1, min_value=1)