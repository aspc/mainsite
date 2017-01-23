from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from aspc.mentalhealth.forms import MentalHealthReviewForm
from aspc.mentalhealth.models import Therapist, MentalHealthReview

class ReviewView(View):
    def get(self, request, therapist_id=None):
        try:
            review = MentalHealthReview.objects.get(therapist=therapist_id, reviewer=self.request.user)
        except MentalHealthReview.DoesNotExist:
            review = None
        form = MentalHealthReviewForm(instance=review)
        therapist = Therapist.objects.get(id=therapist_id).name
        return render(request, 'mentalhealth_reviews/review_new.html', {'therapist_name': therapist, 'form': form})

    def post(self, request, therapist_id=None):
        try:
            review = MentalHealthReview.objects.get(therapist=therapist_id, reviewer=self.request.user)
        except MentalHealthReview.DoesNotExist:
            review = None
        form = MentalHealthReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = self.request.user
            review.therapist = Therapist.objects.get(id=therapist_id)
            form.save_m2m()
            review.save()
            return redirect(reverse('therapist', kwargs={"therapist_id": review.therapist.id}))
        else:
            return render(request, 'mentalhealth_reviews/review_new.html', {'form': form})

def home(request):
    q = request.GET.get("q")
    if q:
        therapists = Therapist.objects.filter(
            Q(name__contains=q) |
            Q(phone__contains=q) |
            Q(email__contains=q) |
            Q(address__contains=q) |
            Q(website__contains=q) |
            Q(insurances__name__contains=q) |
            Q(specialties__name__contains=q) |
            Q(qualifications__name__contains=q)
        )
    else:
        therapists = Therapist.objects.all()
    return render(request, 'mentalhealth_home.html', {'therapists': therapists})

def therapist(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    return render(request, 'therapists/therapist.html', {'t': therapist})
