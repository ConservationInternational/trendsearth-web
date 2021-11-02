"""ldmpweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from core import views
urlpatterns = [path('', include('account.urls')),
               path('dashboard/', include('core.urls')), ]

urlpatterns += [
    path('ajax/algorithm/<int:id>/runmode/<int:runmode>',
         views.ajax_get_algorithm_view, name='ajax_get_algo_view'),
    path('ajax/algorithm/<int:id>/runmode',
         views.ajax_get_runmode, name='ajax_get_runmode'), ]
