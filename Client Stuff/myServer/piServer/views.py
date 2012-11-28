from django.template import Context, loader, RequestContext
from piServer.models import UserProfile, Building, Outlet, Alarm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

@login_required
def index(request):
    print request.user
    building_list = Building.objects.filter(owner=request.user)
    return render_to_response('index.html', {'building_list': building_list})

def building(request, building_id):
    print building_id
    building = get_object_or_404(Building, pk=building_id)
    outlets = Outlet.objects.filter(buildingID=building_id)
    return render_to_response('building.html', {'building': building, 'outlets': outlets})

def outlet(request, building_id, outlet_id):
    print outlet_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    alarms = Alarm.objects.filter(outletID=outlet_id)
    return render_to_response('outlet.html', {'building': building, 'outlet': outlet, 'alarms': alarms})

def deleteAlarm(request, building_id, outlet_id, alarm_id):
    print 'Deleting alarm with id ' + alarm_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    alarm = get_object_or_404(Alarm, pk=alarm_id)
    alarm.delete()
    return HttpResponseRedirect(reverse('piServer.views.outlet', args=(building.id, outlet.id)))

def new(request, building_id, outlet_id):
    print 'Creating an alarm for outlet ' + outlet_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    return render_to_response('newAlarm.html', {'building': building, 'outlet': outlet},
                               context_instance=RequestContext(request))
    
def createAlarm(request, building_id, outlet_id):
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    name = request.POST['name']
    startTime = request.POST['starttime']
    endTime = request.POST['endtime']
    alarm = Alarm(creator = request.user,
                  buildingID = building,
                  outletID = outlet,
                  alarmName = name,
                  startTime = startTime,
                  endTime = endTime,
                  desiredState = True)
    alarm.save()
    return HttpResponseRedirect(reverse('piServer.views.outlet', args=(building.id, outlet.id)))