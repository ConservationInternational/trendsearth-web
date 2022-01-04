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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from core import views as core_views
from account import views as account_views
from job import views as job_views

urlpatterns = [path('', include('account.urls')),
               path('', include('core.urls')),
               path('', include('job.urls')), ]

urlpatterns += [
    path('ajax/algorithm/<int:id>/runmode/<int:runmode>',
         core_views.ajax_get_algorithm_view, name='ajax_get_algo_view'),
    path('ajax/algorithm/<int:id>/runmode',
         core_views.ajax_get_runmode, name='ajax_get_runmode'),
    path('ajax/get/climate_dataset',
         core_views.ajax_load_climate_dataset, name='ajax_get_climate_dataset'),
    path('ajax/regions',
         account_views.ajax_get_regions, name='ajax_get_regions'),
    path('ajax/cities',
         account_views.ajax_get_cities, name='ajax_get_cities'),
    path('ajax/change/aoi',
         account_views.ajax_change_aoi, name='ajax_change_aoi'),
    path('ajax/load/aoi',
         account_views.ajax_load_aoi, name='ajax_load_aoi'),
    path('register/user',
         account_views.ajax_register_user, name='ajax_register_user'),
    path('ajax/user/edit/',
         account_views.update_user_details,
         name='ajax_edit_user'),
    path('ajax/upload/profile_image/',
         account_views.ajax_upload_profile_image,
         name='ajax_upload_profile_image'),
    path('ajax/update/algorithms_visibility',
         account_views.ajax_update_algorithms_visibility,
         name='ajax_update_algorithms_visibility'),
    path('ajax/matrix_table',
         core_views.ajax_get_matrix_table, name='ajax_get_matrix_table'),
    path('ajax/aggregation_table/reset',
         core_views.ajax_reset_aggregation_table, name='ajax_reset_agg_table'),
    path('ajax/update/aggregation_method',
         core_views.ajax_update_aggregation_method,
         name='ajax_update_agg_method'),
    path('ajax/run/job',
         job_views.ajax_run_job,
         name='ajax_run_job'),
    path('ajax/job/results/<int:script_id>',
         job_views.ajax_load_results,
         name='ajax_job_results'),
    path('ajax/job/table/<int:script_id>',
         job_views.ajax_load_jobs,
         name='ajax_job_table'),
    path('ajax/download/<int:id>',
         job_views.ajax_download_job,
         name='ajax_download_job'),
    path('ajax/cancel/<int:id>',
         job_views.ajax_cancel_job,
         name='ajax_download_job'),
    path('ajax/delete/<int:id>',
         job_views.ajax_delete_job,
         name='ajax_download_job'),
    path('ajax/add_layer',
         core_views.add_layer_to_map,
         name='add_layer_to_map')]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
