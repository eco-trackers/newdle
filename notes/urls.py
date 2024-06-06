from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('notes/',views.list_notes_view,name="notes.view"),
    path('notes/',views.list_notes_view,name="notes.view")

]