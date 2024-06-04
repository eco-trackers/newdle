from django.urls import path
from . import views

app_name='absence'
urlpatterns = [
    path('../', views.index_view, name='index'),
    path('', views.AbsenceView.as_view(), name='absence')
]
