from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^read/$', views.read_data, name='read_data'),
    url(r'^$', views.home, name='home'),
    url(r'^trip_list/$', views.trip_list, name='trip_list'),
    url(r'^trip_set_new/$', views.trip_set_new, name='trip_set_new'),
    url(r'^trip_set_list/$', views.trip_set_list, name='trip_set_list'),
    url(r'^trip_set/(?P<pk>[0-9]+)/$', views.trip_set_detail, name='trip_set_detail'),
    url(r'^trip_set_project/(?P<pk>[0-9]+)/$', views.project, name='project'),
    url(r'^trip_set_create_graph/(?P<pk>[0-9]+)/$', views.create_graph, name='create_graph'),
]