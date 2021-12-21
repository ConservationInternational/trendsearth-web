from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.signout, name='logout'),
    path('password_reset', views.password_reset_view,
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'),
        name='password_reset_complete'),
    path('profile', views.view_profile, name='profile'),
    path('profile/edit', views.edit_profile, name='profile_edit'),
    path('settings', views.settings_view, name='settings'),
    path('admin', views.admin_view, name='admin'),
    path('admin/users/<int:user_id>', views.view_user, name='view_user'),
    path('feedback', views.view_feedback, name='feedback'),
]
