from django.urls import path
from . import views

urlpatterns = [
    path('home', views.dashboard, name='dashboard'),
    path('algorithm/<int:algo_id>', views.view_algorithm, name='view_algorithm'),
]
