from django.shortcuts import render
# Need to import

# Create your views here.
class ReviewView(view):
	@method_decorator(login_required)
    def get(self, request, therapist_id):
        if therapist_id:
          therapist = get_object_or_404(Therapist, id=therapist_id)
          review = get_object_or_404(TherapistReview, therapist=therapist) # 
          form = ReviewForm(therapist_id, review)
        else:
          form = ReviewForm(therapist_id)
        return render(request, 'reviews/review_new.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, therapist_id):
        form = ReviewForm(therapist_id, None, request.POST)
        if form.is_valid():
            #instructor = form.cleaned_data["professor"]
            therapist = form.cleaned_data["therapist"]
            reasons = form.cleaned_data["reasons"]
            duration = form.cleaned_data["duration"]

            feeling = form.cleaned_data["feeling"]
            gender = form.cleaned_data["gender"]
            sexual_orientation = form.cleaned_data["sexual_orientation"]
            ethnicity = form.cleaned_data["ethnicity"]
            identity = form.cleaned_data["identity"]
            identity_related_comment = form.cleaned_data["identity_related_comment"]
            therapist_recommendation = form.cleaned_data["therapist_recommendation"]
            therapist_strategy = form.cleaned_data["therapist_strategy"]
            tags = form.cleaned_data["tags"]


            review, created = CourseReview.objects.get_or_create(author=request.user, therapist=therapist)
            review.therapist = therapist
            review.reasons = reasons

            review.feeling = feeling
            review.gender = gender
            review.sexual_orientation = sexual_orientation
            review.ethnicity = ethnicity
            review.identity = identity
            review.identity_related_comment = identity_related_comment
            review.therapist_recommendation = therapist_recommendation
            review.therapist_strategy = therapist_strategy
            review.tags = tags
            review.save()
            # Likely to change 'section_detail'
            return redirect(reverse('section_detail', kwargs={"therapist_id": therapist_id}))
        else:
            return render(request, 'reviews/review_new.html', {'form': form})

