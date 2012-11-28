from django.conf.urls import patterns, url
from piServer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^buildings/(?P<building_id>\d+)/$', views.building),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/$', views.outlet),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/(?P<alarm_id>\d+)/delete/$', views.deleteAlarm),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/new/$', views.new),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/new/create$', views.createAlarm),
)
