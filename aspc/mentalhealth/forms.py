from django.forms import ModelForm

from aspc.mentalhealth.models import MentalHealthReview


class MentalHealthReviewForm(ModelForm):
    class Meta:
        model = MentalHealthReview
        fields = "__all__"
