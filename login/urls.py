from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.log_in, name='log_in'),
    path('users/', views.tab_and_upload_csv_view, name='tab_and_upload_csv_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_request/', views.password_reset_request, name='password_reset_request'),
    path('delete_users/', views.delete_users, name='delete_users'),
]