from django.shortcuts import render
from .models import Note
from django.contrib.auth.decorators import login_required
from .forms import NoteCreateForm


def list_notes_view(request):
    la_note=Note.objects.get(id=1)
    context={
        'note':la_note.valeur,
        'matière':la_note.subject,
        'eleve':la_note.profil,

    }
    
    return render(request, 'list_notes.html', context)


def create_notes_view(request):
    form= NoteCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form= NoteCreateForm()


    context={
        'form':form
    }
    return render(request, 'create_notes.html', context)

