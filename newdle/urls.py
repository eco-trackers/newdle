from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subjects/', include('subjects.urls',namespace='subjects-home-view')),
    path('login/', include('login.urls',namespace='log_in')),
    path('group/', include('group.urls')),
    path('absence/', include('absence.urls')),
    path('notes/',include('notes.urls',namespace='liste.view')),
    path('profil/',include('profil.urls')),
    path('principal/',views.principal, name='principal'),
    path('eco-conception/',views.eco, name='eco'),
   path('contact/',views.contact, name='contact'),
    path('', views.index, name='index'),
]
handler404 = 'newdle.views.page_404'