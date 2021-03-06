from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt
from piServer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    (r'^login/$', csrf_exempt(login), {'template_name': 'login.html'}, "login"),
    url(r'^logout/$', views.logout_view),
    url(r'^account/new/$', views.newAccount),
    url(r'^account/new/create/$', views.createAccount),
    url(r'^buildings/new/$', views.newBuilding),
    url(r'^buildings/create/$', views.createBuilding),
    url(r'^buildings/new/create/$', views.createBuilding),
    url(r'^buildings/(?P<building_id>\d+)/$', views.building),
    url(r'^buildings/(?P<building_id>\d+)/outlets/new/$', views.newOutlet),
    url(r'^buildings/(?P<building_id>\d+)/outlets/create/$', views.createOutlet),
    url(r'^buildings/(?P<building_id>\d+)/outlets/new/create/$', views.createOutlet),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/$', views.outlet),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/delete$', views.deleteOutlet),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/flip/(?P<flip_state>\d+)/$', views.flipState),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/(?P<alarm_id>\d+)/delete/$', views.deleteAlarm),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/new/$', views.newAlarm),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/new/create/$', views.createAlarm),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/timers/new/$', views.newTimer),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/timers/new/create/$', views.createTimer),
)
