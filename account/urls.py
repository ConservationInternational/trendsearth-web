from django.urls import path
from . import views


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout', views.signout, name='logout'),
    path('profile', views.view_profile, name='profile'),
]
