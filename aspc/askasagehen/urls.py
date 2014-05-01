from django.conf.urls import patterns, url
from aspc.askasagehen.views import home, question

urlpatterns = patterns('',
	url(r'question', question, name='submit_question'),
	url(r'', home, name='askasagehen')
)