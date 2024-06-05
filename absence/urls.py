from django.urls import path
from . import views

app_name='absence'
urlpatterns = [
    path('../', views.index_view, name='index'),
    path('<str:id>/', views.AbsenceView.as_view(), name='absence'),
    path('', views.AbsenceView.as_view(), name='absence_none'),
    path('<str:id>/delete/', views.delete_absence, name='absence_delete'),
    path('<int:id>/edit/', views.edit_absence, name='absence_edit'),
]
