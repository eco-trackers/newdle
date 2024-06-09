from django.shortcuts import render
from .models import Note
from django.contrib.auth.decorators import login_required
from .forms import NoteCreateForm
from subjects.models import Subject
from profil.models import Profil


#def get_prof_subjects(request):
  #  return Subject.objects.filter(prof=request.user.profil).all()



#def get_student_subjects(request):  # get courses the student is enrolled in
 #   groups = Profil.objects.get(request.user.id).group.all()
  #  return Subject.objects.filter(student_group__in=groups).distinct()


def list_notes_view(request):
 #   subject=get_student_subjects(request)
  #  notes = Note.objects.filter(subject=subject).select_related('subject')
   # context={
    #    'note':notes.valeur,
     #   'matière':notes.subject,
      #  'eleve':notes.profil,

    #}
    
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

