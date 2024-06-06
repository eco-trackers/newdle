from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.subjects_home_view,name="subjects-home-view"),
    path('<subject_id>/',views.subjects_get_view_detail,name='subjects-get-detail-view'),
]