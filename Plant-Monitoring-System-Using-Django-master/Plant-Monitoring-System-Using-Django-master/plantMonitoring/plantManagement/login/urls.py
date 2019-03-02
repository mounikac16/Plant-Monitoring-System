from django.conf.urls import url, include

from . import views

app_name = 'login'

urlpatterns = [

	url(r'^$',views.indexView,name='home'),
	
	url(r'^register/$',views.UserRegisterView,name='register'),

	url(r'^login/$',views.UserLoginView,name='login'),
]
