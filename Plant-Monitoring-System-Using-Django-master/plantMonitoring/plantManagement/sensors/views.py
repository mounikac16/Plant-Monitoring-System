from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from login.forms import UserForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    template = 'sensors/index.html'
    plantnum = plantID.objects.all()
    print(plantnum)
    data={'username': request.user, 'plantnum': plantnum}
    return render(request, template, data)

@csrf_exempt
def add_reading(request):
    if request.POST.get('plant'):
    	data1 = request.POST.get('plant').split(' ')
    	for n in range(1, len(data1)-3):
    		moisture = plant.objects.create(pid=plantID.objects.get(pid=n), soilMoisture = data1[n+3])
    		moisture.save()
    	weather = weatherStation.objects.create(temperature=data1[0], humidity=data1[1], overHeadTank=data1[2], rainGauge=data1[3])
    	weather.save()
    	return HttpResponse(status=200)
    return  HttpResponse(status=400)

# specific to particular plant requested
@login_required
@csrf_exempt
def display(request, pid):
	moisture = plant.objects.filter(pid=pid)[::-1]
	print(moisture)
	plantDetail = plantID.objects.filter(pid=pid)[::-1]
	w = weatherStation.objects.filter(pk=weatherStation.objects.count())
	weather = weatherStation.objects.get(pk=weatherStation.objects.count())
	T = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).temperature for k in range(0, 11)][::-1]
	H = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).humidity for k in range(0, 11)][::-1]
	OHT = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).overHeadTank for k in range(0, 11)][::-1]
	RG = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).rainGauge for k in range(0, 11)][::-1]
	D = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.time for k in range(0, 11)][::-1]
	Dt =[weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.date for k in range(0, 11)][::-1] 
	if len(moisture) == 0:
		data={'username': request.user, 'w': w ,'sM': "None", 'plantName': plantDetail[0].plantName, 'latitude': plantDetail[0].latitude, 'longitude': plantDetail[0].longitude,  'pid': pid, 'weather': weather,'temperature' : T,'humidity': H, 'overHeadTank': OHT, 'rainGauge': RG,'tm': zip(D,Dt)}
		template = 'sensors/plant.html'
		return render(request, template, data)
	data={'username': request.user,'w': w , 'sM': moisture, 'latitude': plantDetail[0].latitude, 'longitude': plantDetail[0].longitude, 'plantName': plantDetail[0].plantName, 'pid': pid, 'weather': weather,'temperature' : T,'humidity': H, 'overHeadTank': OHT, 'rainGauge': RG,'tm': zip(D,Dt)}
	#print(w)
	template = 'sensors/plant.html'
	return render(request, template, data)

@csrf_exempt
def motorControl(request, pid):
	#plant = plantID.objects.filter(pid=pid)[::-1]
	if request.method=='POST':
		template = loader.get_template('sensors/motorControl.html')
		if request.POST['status'] == 'automatic':
			mode = 'automatic'
			status = "none"
			print(actuator)
		else:
			mode = 'manual'
			status = request.POST['status']
			print(actuator, status)
	context = {
		'pid': pid,
		'mode': mode,
		'status': status,
	}
	return HttpResponse(template.render(context, request))


@login_required
def weather(request):
	if request.method == "GET":
		plantnum = plantID.objects.all()
		weather = weatherStation.objects.get(pk=weatherStation.objects.count())
		T = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).temperature for k in range(0, 11)][::-1]
		H = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).humidity for k in range(0, 11)][::-1]
		OHT = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).overHeadTank for k in range(0, 11)][::-1]
		RG = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).rainGauge for k in range(0, 11)][::-1]
		template = 'sensors/weather.html'
		data={'username': request.user, 'plantnum': plantnum, 'temperature': T, 'humidity': H, 'overHeadTank': OHT, 'rainGauge': RG}
		#print(T, H, OHT, RG)
		return render(request, template, data)

@login_required
@csrf_exempt
def sm(request, pid1, pid):
	print("entered")
	moisture = plant.objects.filter(pid=pid)[::-1]
	print(moisture)
	plantDetail = plantID.objects.filter(pid=pid)[::-1]
	D = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.time for k in range(0, 11)][::-1]
	Dt =[weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.date for k in range(0, 11)][::-1] 
	if len(moisture) == 0:
		data={'username': request.user,'sM': zip("None",D,Dt), 'plantName': plantDetail[0].plantName, 'latitude': plantDetail[0].latitude, 'longitude': plantDetail[0].longitude,  'pid': pid}
		template = 'sensors/sm.html'
		return render(request, template, data)
	data={'username': request.user, 'sM': zip(moisture,D,Dt), 'latitude': plantDetail[0].latitude, 'longitude': plantDetail[0].longitude, 'plantName': plantDetail[0].plantName, 'pid': pid}
	print(moisture)
	template = 'sensors/sm.html'
	return render(request, template, data)

@csrf_exempt
def demo(request):
	template = 'sensors/demo.html'
	return render(request, template)

@csrf_exempt
def about(request):
	template = 'sensors/about.html'
	return render(request, template)

@login_required
@csrf_exempt
def addplant(request):
	if request.method == "POST":
		plantName = request.POST['plantname']
		latitude = request.POST['lat']
		longitude = request.POST['long']
		p = plantID.objects.count()
		plant = plantID.objects.create(pid=p+1, plantName=plantName, latitude=latitude, longitude=longitude)
		plant.save()
		return redirect('sensors:index')
	template = 'sensors/addplant.html'
	return render(request, template)

@login_required
def temperature(request):
	if request.method == "GET":
		weather = weatherStation.objects.get(pk=weatherStation.objects.count())
		T = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).temperature for k in range(0, 11)][::-1]
		D = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.time for k in range(0, 11)][::-1]
		Dt =[weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.date for k in range(0, 11)][::-1] 
		template = 'sensors/temperature.html'
		data={'username': request.user, 'temperature': zip(T, D, Dt)}
		return render(request, template, data)

@login_required
def humidity(request):
	if request.method == "GET":
		weather = weatherStation.objects.get(pk=weatherStation.objects.count())
		H = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).humidity for k in range(0, 11)][::-1]
		D = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.time for k in range(0, 11)][::-1]
		Dt =[weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.date for k in range(0, 11)][::-1] 
		template = 'sensors/humidity.html'
		data={'username': request.user, 'humidity': zip(H, D, Dt)}
		return render(request, template, data)

@login_required
def OHT(request):
	if request.method == "GET":
		weather = weatherStation.objects.get(pk=weatherStation.objects.count())
		OHT = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).overHeadTank for k in range(0, 11)][::-1]
		D = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.time for k in range(0, 11)][::-1]
		Dt =[weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.date for k in range(0, 11)][::-1] 
		template = 'sensors/OHT.html'
		data={'username': request.user, 'oht': zip(OHT, D, Dt)}
		return render(request, template, data)

@login_required
def rain(request):
	if request.method == "GET":
		weather = weatherStation.objects.get(pk=weatherStation.objects.count())
		R = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).rainGauge for k in range(0, 11)][::-1]
		D = [weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.time for k in range(0, 11)][::-1]
		Dt =[weatherStation.objects.get(pk=weatherStation.objects.count()-k).read_time.date for k in range(0, 11)][::-1] 
		template = 'sensors/rain.html'
		data={'username': request.user, 'rainLevel': zip(R, D, Dt)}
		print(R, D, Dt)
		return render(request, template, data)

@login_required
def map(request):
    if request.method == 'GET':
    	plantD = plantID.objects.all()
    	num = []
    	lat = []
    	longi = []
    	num2 = []
    	lat2 = []
    	longi2 = []
    	k=0
    	for q in plantD:
    		if(k<2):
	    	    num.append(q.pid)
	    	    lat.append(q.latitude)
	    	    longi.append(q.longitude)
	    	else:
	    		num2.append(q.pid)
	    		lat2.append(q.latitude)
	    		longi2.append(q.longitude)
	    	k=k+1

    	k=len(num)
    	data={'username': request.user,'locate': zip(num,lat,longi),'locate2': zip(num2,lat2,longi2)}
    	template = 'sensors/map.html'
    	print(num,lat,longi)
    	return render(request, template, data)