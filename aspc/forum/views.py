from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from aspc.mentalhealth.forms import MentalHealthReviewForm
from aspc.mentalhealth.models import Therapist, MentalHealthReview

class PostView(View):
    @method_decorator(login_required)
    def get(self, request):
        return
    @method_decorator(login_required)
    def post(self, request, therapist_id=None):
        #this is for editing
        #try:
        #    review = MentalHealthReview.objects.get(therapist=therapist_id, reviewer=self.request.user)
        #except MentalHealthReview.DoesNotExist:
        #    review = None
        # check valid?
        form = PostForm(request.POST)#, instance=review)
        if form.is_valid():
    		post = form.save(commit=False)
    		post.author = self.request.user
    		post.save()
            form.save_m2m()
            return redirect(reverse('showAllPosts'))
		else:
            return render(request, 'posts/new_post.html', {'form' : form})
        

class QuestionView(View):
	@method_decorator(login_required)
    def get(self, request, therapist_id=None):
        return
    @method_decorator(login_required)
    def post(self, request, therapist_id=None):
        form = QuestionForm(request.POST)
        if form.is_valid():  
            question = form.save(commit=False)
            question.author = self.request.user
            question.save()
            form.save_m2m()
        return redirect(reverse('showAllQuestions'))

# class QuestionDetailView(View):
#     model = Question
#     template_name = "qna/question.html"

#     def get_object(self):
#         question = Question.objects.filter(id__exact=self.kwargs['id'])
#         if not question:
#             raise Http404
#         return question

#     def get_context_data(self, **kwargs):
#         context = super(QuestionDetailView, self).get_context_data(**kwargs)
#         question_object = get_object_or_404(Instructor, id=self.kwargs['id'])
#         answers = Answer.objects.filter(question_id=question_object.id)
#         context['answers'] = answers
#         return context    

def showAllPosts(request):
    return render(request, 'posts/posts.html')

def showAllQuestions(request):
    return render(request, 'qna/questions.html')

def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'qna/question.html', {'q': question})

@login_required
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post.html', {'p': post})


def home(request):
    return render(request, 'general/forum_home.html')

