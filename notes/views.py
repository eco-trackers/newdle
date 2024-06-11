from django.shortcuts import render
from .models import Note
from django.contrib.auth.decorators import login_required
from subjects.models import Subject
from profil.models import Profil
from django.shortcuts import get_object_or_404


def get_prof_subjects(request):
    return Subject.objects.filter(prof=request.user.profil).all()



def get_student_subjects(request):  # get courses the student is enrolled in
    groups = Profil.objects.get(request.user.id).group.all()
    return Subject.objects.filter(student_group__in=groups).distinct()

@login_required
def list_notes_view(request,subject_id):
    context = {'s':get_object_or_404(Subject,id=subject_id)}
    if request.user.profil.type=='0':
        notes = get_object_or_404(Note,subject=get_object_or_404(Subject,id=subject_id),profil=request.user.profil)
        context['note']= notes
   
    elif request.user.profil.type=='1'or request.user.profil.type=='2':
        notes=Note.objects.filter(subject=get_object_or_404(Subject,id=subject_id))
        context['notes']= notes


    #print("miaw: ",context)
    # Render the template with the list of notes
    return render(request, 'list_notes.html',context)




def create_notes_view(request):
    
    return render(request, 'create_notes.html', {})

