from django.template import Context, loader, RequestContext
from piServer.models import UserProfile, Building, Outlet, Alarm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

def logout_view(request):
    logout(request)
    return render_to_response('login.html')

@login_required
def index(request):
    building_list = Building.objects.filter(owner=request.user)
    return render_to_response('index.html', {'building_list': building_list})

@login_required
def building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    outlets = Outlet.objects.filter(buildingID=building_id)
    return render_to_response('building.html', {'building': building, 'outlets': outlets})

@login_required
def outlet(request, building_id, outlet_id):
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    alarms = Alarm.objects.filter(outletID=outlet_id)
    return render_to_response('outlet.html', {'building': building, 'outlet': outlet, 'alarms': alarms})

@login_required
def deleteAlarm(request, building_id, outlet_id, alarm_id):
    print 'Deleting alarm with id ' + alarm_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    alarm = get_object_or_404(Alarm, pk=alarm_id)
    alarm.delete()
    return HttpResponseRedirect(reverse('piServer.views.outlet', args=(building.id, outlet.id)))

@login_required
def new(request, building_id, outlet_id):
    print 'Creating an alarm for outlet ' + outlet_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    return render_to_response('newAlarm.html', {'building': building, 'outlet': outlet},
                               context_instance=RequestContext(request))

@login_required
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

@login_required
def newOutlet(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    return render_to_response('newOutlet.html', {'building': building},
                              context_instance=RequestContext(request))

def createOutlet(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    name = request.POST['name']
    outlet = Outlet(outletName = name,
                    buildingID = building,
                    state = False,
                    energyTotal = 0)
    outlet.save()
    return HttpResponseRedirect(reverse('piServer.views.building', args=(building.id,)))

def flipState(request, building_id, outlet_id, flip_state):
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    if flip_state == '0':
        outlet.state = False
    else:
        outlet.state = True
    outlet.save()
    return HttpResponseRedirect(reverse('piServer.views.building', args=(building.id,)))

@login_required
def deleteOutlet(request, building_id, outlet_id):
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    outlet.delete()
    return HttpResponseRedirect(reverse('piServer.views.building', args=(building.id,)))

@login_required
def newBuilding(request):
    return render_to_response('newBuilding.html', {}, context_instance=RequestContext(request))

@login_required
def createBuilding(request):
    name = request.POST['name']
    building = Building(buildingname = name,
                        owner = request.user,
                        onlineState = True)
    building.save()
    return HttpResponseRedirect(reverse('piServer.views.index', args=()))

def newAccount(request):
    return render_to_response('newAccount.html', {}, context_instance=RequestContext(request))