from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('<int:subject_id>',views.list_notes_view,name="liste.view"),
    path('create/',views.create_notes_view,name="create.view")
    
]