from polls import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(
        r'^(?P<poll_id>\d+)/results/$',
        views.poll_results,
        name='results'
    ),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
]
