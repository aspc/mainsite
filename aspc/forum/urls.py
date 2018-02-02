from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from aspc.forum.views import home, ReviewView, therapist

urlpatterns = [
    url(r'^$', home, name="forum_home"),
    url(r'^question/$', showAllQuestions, name="all_questions"),
    url(r'^question/(?P<therapist_id>\d+)/answer/?$', login_required(AnswerView.as_view()), name="new_answer"),
    url(r'^question/new/?$', login_required(QuestionView.as_view()), name="new_question"),
    url(r'^post/$', showAllPosts, name="all_posts"),
    url(r'^post/(?P<post_id>\d+)/?$', post, name="post"),
    url(r'^post/new/?$', login_required(PostView.as_view()), name="new_post"),
    url(r'^question/(?P<question_id>\d+)/?$', QuestionDetailView.as_view(), name="question"),
]