from django.urls import path
from . import views

app_name='absence'
urlpatterns = [
    path('../', views.index_view, name='index'),
    path('<str:id>/', views.AbsenceView.as_view(), name='absence'),
    path('', views.absence_main, name='absence_none'),
    path('<str:id>/delete/', views.delete_absence, name='absence_delete'),
    path('<str:id>/edit/', views.edit_absence, name='absence_edit'),
    path('<str:id>/upload_photo/', views.upload_photo_view, name='photo_upload'),
    path('<str:id>/check_photo/', views.check_photo, name='check_photo'),
    path('<str:id>/mark_presence/', views.mark_presence_view, name='mark_presence'),
    path('<str:id>/mark_presence/delete', views.mark_presence_delete, name='mark_presence_delete'),
    path('<str:id>/check_photo/delete', views.photo_delete, name='photo_delete')
]
