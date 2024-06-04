from django.urls import path
from . import views

app_name='login'
urlpatterns = [
    path('../', views.index_view, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('', views.log_in, name='log_in')
]
