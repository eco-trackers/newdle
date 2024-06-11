from django.contrib import admin
from django.urls import path,include
from . import views


app_name='subjects'

urlpatterns = [
    path('',views.subjects_home_view,name="subjects-home-view"),
    path('<int:subject_id>/',views.subjects_get_detail_view,name='subjects-get-detail-view'),
    path('<int:subject_id>/edit/',views.edit_view,name='subjects-edit-view'),
    path('new',views.create_subject,name='subjects-new-view'),
    path('<int:subject_id>/delete/',views.delete_subject,name='subjects-delete-view'),
    path('ue/',views.ue_home_view,name='ue-home-view'),
    path('ue/<int:ue_id>/',views.ue_get_detail_view,name='ue-get-detail-view'),
    path('ue/new',views.create_ue,name='ue-new-view'),
    path('ue/<int:ue_id>/edit/',views.edit_ue_view,name='ue-edit-view'),
    path('ue/<int:ue_id>/delete/',views.delete_ue,name='ue-delete-view'),
    path('maquette/',views.view_maquette,name='maquette-view'),
]