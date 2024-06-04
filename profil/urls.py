from django.urls import path
from . import views

app_name='profil'
urlpatterns = [
    path('../', views.index_view, name='index'),
    path('', views.profil_render, name='profil')
]
