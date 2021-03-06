from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
	path('', views.index, name="index"), 
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('bulk',views.bulk, name="bulk"),
	path('redirection',views.main, name="main"),
	path('result/', views.logoutUser, name="result"),
	path('single/', views.single, name="single"),
	# path('editprofile/', views.profile, name="profile"),
	# path('profile/<str:name>', views.profilepage, name="profilepage"),
]
