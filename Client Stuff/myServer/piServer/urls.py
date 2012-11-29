from django.conf.urls import patterns, url
from piServer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', views.logout_view),
    url(r'^account/new/$', views.newAccount),
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
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/new/$', views.new),
    url(r'^buildings/(?P<building_id>\d+)/outlets/(?P<outlet_id>\d+)/alarms/new/create/$', views.createAlarm),
)
