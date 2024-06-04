from django.urls import path
from . import views

app_name='absence'
urlpatterns = [
    path('../', views.index_view, name='index'),
    path('<str:id>/', views.AbsenceView.as_view(), name='absenceinput'),
    path('', views.AbsenceView.as_view(), name='absence')
]
