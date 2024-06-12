from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('',views.list_view,name="list.view"),
    path('edit/',views.edit_view,name="edit.view"),
    path('edit/<int:id>',views.edit_detail,name="detail.view"),
]