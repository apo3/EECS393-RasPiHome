from django.template import Context, loader, RequestContext
from piServer.models import UserProfile, Building, Outlet, Alarm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login', args=''))

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
    alarms = Alarm.objects.filter(outletID=outlet_id, startTime__isnull=True)
    timers = Alarm.objects.filter(outletID=outlet_id, startTime__isnull=False)
    print alarms
    print timers
    return render_to_response('outlet.html', {'building': building, 'outlet': outlet, 'alarms': alarms, 'timers': timers})

@login_required
def deleteAlarm(request, building_id, outlet_id, alarm_id):
    print 'Deleting alarm with id ' + alarm_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    alarm = get_object_or_404(Alarm, pk=alarm_id)
    alarm.delete()
    return HttpResponseRedirect(reverse('piServer.views.outlet', args=(building.id, outlet.id)))

@login_required
def newAlarm(request, building_id, outlet_id):
    print 'Creating an alarm for outlet ' + outlet_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    return render_to_response('newAlarm.html', {'building': building, 'outlet': outlet},
                               context_instance=RequestContext(request))

@login_required
def newTimer(request, building_id, outlet_id):
    print 'Creating a timer for outlet ' + outlet_id
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    return render_to_response('newTimer.html', {'building': building, 'outlet': outlet},
                               context_instance=RequestContext(request))

@login_required
def createTimer(request, building_id, outlet_id):
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
def createAlarm(request, building_id, outlet_id):
    building = get_object_or_404(Building, pk=building_id)
    outlet = get_object_or_404(Outlet, pk=outlet_id)
    name = request.POST['name']
    endTime = request.POST['endtime']
    alarm = Alarm(creator = request.user,
                  buildingID = building,
                  outletID = outlet,
                  alarmName = name,
                  startTime = None,
                  endTime = endTime,
                  desiredState = True)
    alarm.save()
    return HttpResponseRedirect(reverse('piServer.views.outlet', args=(building.id, outlet.id)))

@login_required
def newOutlet(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    return render_to_response('newOutlet.html', {'building': building},
                              context_instance=RequestContext(request))

@login_required
def createOutlet(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    name = request.POST['name']
    outlet = Outlet(outletName = name,
                    buildingID = building,
                    state = False,
                    energyTotal = 0)
    outlet.save()
    return HttpResponseRedirect(reverse('piServer.views.building', args=(building.id,)))

@login_required
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

@csrf_exempt
def newAccount(request):
    return render_to_response('newAccount.html', {}, context_instance=RequestContext(request))

@csrf_exempt
def createAccount(request):
    username = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    passwordconf = request.POST['password_conf']
    squestion = request.POST['squestion']
    sanswer = request.POST['sanswer']
    username_error = ''
    email_error = ''
    password_error = ''
    squestion_error = ''
    sanswer_error = ''
    
    if username == '' or len(username) > 30:
        username_error = "Username must be between 1 and 30 alphanumeric characters"
    if len(email) < 5 or len(email) > 30:
        email_error = "Email must be between 5 and 30 characters in form x@x.x"
    if password == '' or passwordconf == '' or password != passwordconf:
        password_error = "Check that you have a password and password confirmation is the same"
    if squestion == '':
        squestion_error = "You must provide a security question"
    if sanswer == '':
        sanswer_error = "You must provide a security answer"
    
    if len(username_error) > 0 or len(email_error) > 0 or len(password_error) > 0 or len(squestion_error) > 0 or len(sanswer_error) > 0:
        return render_to_response('newAccount.html', {'username_error': username_error,
                                                      'email_error': email_error,
                                                      'password_error': password_error,
                                                      'squestion_error': squestion_error,
                                                      'sanswer_error': sanswer_error})
    else:
        user = User(username = username,
                    email = email,
                    password = password)
        user.save()
        user_profile = UserProfile(user = user,
                                   sQuestion = int(squestion),
                                   sAnswer = sanswer,
                                   lastAddress = '127.0.0.0')
        user_profile.save()
        return render_to_response('index.html')