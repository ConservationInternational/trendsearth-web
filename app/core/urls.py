from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:algo_id>', views.view_algorithm, name='view_algorithm'),
]
