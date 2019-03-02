from django.conf.urls import url																													
from . import views

app_name = 'sensors'

urlpatterns = [
	# homepage
    url(r'^$', views.index, name='index'),
	#temperature
	url(r'^temperature/$',views.temperature, name='temperature'),
	#humidity
	url(r'^humidity/$',views.humidity, name='humidity'),
	#overhead tank
	url(r'^OHT/$',views.OHT, name='OHT'),
	#rain gauge
	url(r'^rain/$',views.rain, name='rain'),
	#weather station
	url(r'^weather/$',views.weather, name='weather'),
	#add new reading
    url(r'^addreading/$', views.add_reading, name='addreading'),
    #display particular plant info
    url(r'^display/(?P<pid>[0-9]+)/$', views.display, name='display'),
    url(r'^weather/display/(?P<pid>[0-9]+)/$', views.display, name='display'),
    #soil moisture
    url(r'^display/(?P<pid1>[0-9]+)/sm/(?P<pid>[0-9]+)/',views.sm, name='sm'),
    url(r'^weather/display/(?P<pid1>[0-9]+)/sm/(?P<pid>[0-9]+)/',views.sm, name='sm'),
    #add new plant
    url(r'^addplant/$', views.addplant, name='addplant'),
    #demo
    url(r'^demo/$', views.demo, name='demo'),   
    #map
    url(r'^map/',views.map, name='map'),
    #about us
    url(r'^about/$', views.about, name='about'),
    # motorControl
    url(r'^control/(?P<pid>[0-9]+)/$', views.motorControl, name='motorControl'),
]
