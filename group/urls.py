from django.urls import path
from . import views

app_name = 'group'
urlpatterns = [
    path('', views.show, name='show'),
    path('<int:id>/', views.show, name='show'),
    path('create/', views.create, name='create'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
]