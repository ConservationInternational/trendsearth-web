from django.urls import path
from . import views

urlpatterns = [
    path('job', views.index, name='job'),
    path('job/<int:job_id>/view',
         views.view_job, name='view_job')
]
