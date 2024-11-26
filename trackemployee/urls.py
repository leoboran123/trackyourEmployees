"""trackemployee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from user import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('adminLogin/', views.login_user, name="loginAdmin"),
    path('adminRegister/', views.register_admin, name="registerAdmin"),

    path('logout/', views.logout_user, name="logout"),

    path('vacation/', views.seeDatas, name="seeVacations"),
    
    path('checkStaff/', views.checkStaff, name="seeStaffs"),
    path('mymessages/', views.checkMessages, name="seeMessages"),

    path('requestVacation/', views.requestVacation, name="reqVacation"),

    path('requestApproved/', views.requestApproved, name="reqApp"),
    path('requestDeclined/', views.requestDeclined, name="reqDec"),





]
