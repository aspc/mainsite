from django.forms import ModelForm, CheckboxSelectMultiple

from aspc.mentalhealth.models import MentalHealthReview


class MentalHealthReviewForm(ModelForm):
    class Meta:
        model = MentalHealthReview
        exclude = ["therapist","reviewer","created_ts","tags"]
        widgets = {
            'reasons': CheckboxSelectMultiple,
            'gender': CheckboxSelectMultiple,
            'sexual_orientation': CheckboxSelectMultiple,
            'ethnicity': CheckboxSelectMultiple,
            'identity': CheckboxSelectMultiple
        }
        labels = {
            'reasons': 'For what type of care did you visit this therapist? (required)',
            'duration': 'How long have you been with this therapist? (required)',
            'feeling': 'How do you feel your visit went? (required)',
            'gender': 'What is your gender? Check all that apply. (optional)',
            'sexual_orientation': 'What is your sexual orientation? Check all that apply. (optional)',
            'ethnicity': 'What is your ethnicity? Check all that apply. (optional)',
            'identity': 'Which of the following do you identify with? (optional)',
            'identity_related_comment': 'Do you feel that your identities affected your visit(s) with this therapist? (optional)',
            'therapist_recommendation': 'What did your therapist recommend? (e.g.prescriptions, referral to a psychiatrist, etc.) (optional)',
            'therapist_strategy': 'What ongoing strategies did you and your therapist use? (e.g.goal setting, journaling, visualization exercises, etc.) (optional)'
        }