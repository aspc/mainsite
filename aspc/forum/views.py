from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from aspc.forum.forms import PostForm, QuestionForm, AnswerForm, SearchForm
from aspc.forum.models import Question, Post, Answer
from django.core.mail import send_mail
from aspc.settings import EMAIL_HOST_USER

class PostView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = PostForm()
        return render(request, 'posts/new_post.html', {'form': form})
    @method_decorator(login_required)
    def post(self, request):
        form = PostForm(request.POST)#, instance=review)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()
            form.save_m2m()
            return redirect(reverse('all_posts'))
        else:
            return render(request, 'posts/new_post.html', {'form' : form})
        
class QuestionView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = QuestionForm()
        return render(request, 'qna/new_question.html', {'form': form})
    @method_decorator(login_required)
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():  
            question = form.save(commit=False)
            question.author = self.request.user
            question.save()
            form.save_m2m()
        return redirect(reverse('all_questions'))


class AnswerView(View):
    @method_decorator(login_required)
    def get(self, request, question_id):
        form = AnswerForm()
        return render(request, 'qna/new_answer.html', {'form': form})
    @method_decorator(login_required)
    def post(self, request, question_id):
        form = AnswerForm(request.POST)
        if form.is_valid():  
            answer = form.save(commit=False)
            answer.author = self.request.user
            question = get_object_or_404(Question, id=question_id)
            answer.question = question
            answer.save()
            form.save_m2m()
            subject = 'You\'ve got a new answer to your question!'
            content = 'You\'ve received a new answer to your question! Check at https://aspc.pomona.edu/forum/question/{0}'.format(question_id)
            send_mail(subject,content,EMAIL_HOST_USER,[question.author.email])
        return redirect(reverse('question', kwargs={'question_id': question_id}))


@login_required
def showAllPosts(request):
    posts = Post.objects.all()
    return render(request, 'posts/posts.html', {'posts' : posts})

@login_required
def showAllQuestions(request):
    questions = Question.objects.all()
    return render(request, 'qna/questions.html', {'questions': questions})

@login_required
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'qna/question.html', {'q': question})

@login_required
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post.html', {'p': post})

@login_required
def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            page = form.cleaned_data["search_page"]
            tags = list(map(lambda tag: tag.name, form.cleaned_data["tags"]))
            if (page == 'Question'):
                questions = Question.objects.filter(tags__name__in=tags)
                return render(request, 'qna/questions.html', {'questions': questions})
            else:
                posts = Post.objects.filter(tags__name__in=tags)
                return render(request, 'posts/posts.html', {'posts' : posts})

    else:
        form = SearchForm()  
        return render(request, 'general/forum_home.html', {'form': form})
    return render(request, 'general/forum_home.html', {'form': form})

@login_required
def showResources(request):
    return render(request, 'general/resources.html')

