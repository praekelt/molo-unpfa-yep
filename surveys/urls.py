from surveys import views
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<question_id>[0-9]+)/survey/$', views.survey, name='survey'),
]
