from django.shortcuts import render
from .models import Note
from django.contrib.auth.decorators import login_required
from .forms import NoteCreateForm
from subjects.models import Subject
from profil.models import Profil


# def get_prof_subjects(request):
#     return Subject.objects.filter(prof=request.user.profil).all()

def get_UEs(request,semester):
    # step 0 - get all subjects for user that is in the group
    subjects = Subject.objects.filter(student_group=request.user.profil.group).all()

    # step 1 - get all UE from subjects list
    

def get_student_notes(request,subject):
    return Note.objects.filter(profil=request.user.profil,subject=subject).all()

def get_formatted_notes(request):
    """
        in format
        [
            {
                "name":"UEName",
                "count":noteCount,
                "notes":[
                    {
                        "subject":"subjectName",
                        "note":noteValue (default -1)
                    },
                    ...
                ]
            }
            ...
        ]
    """
    subjects = get_student_subjects(request)
    notes = []
    for subject in subjects:
        


def list_notes_view(request):
    # Retrieve all notes from the database
    notes = Note.objects.all()

    # Render the template with the list of notes
    return render(request, 'list_notes.html', {'notes': notes})



def create_notes_view(request):
    form= NoteCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        form= NoteCreateForm()


    context={
        'form':form
    }
    return render(request, 'create_notes.html', context)

