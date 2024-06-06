from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Subject
from profil.models import Profil

# 0 etudiant
# 1 prof
# 2 admin

# managament of subjects only, for marks, check

@login_required
def subjects_home_view(request): # show the list of subjects to manage
    if request.user.profil.type == '2': # if admin, list the id of all subjects
        subjects_list = Subject.objects.all() 
    elif request.user.profil.type == '1': # if prof, list only the subjects he is responsible for
        subjects_list = Subject.objects.filter(prof=request.user.profil)
    elif request.user.profil.type == '0': # if etudiant, list only the subjects he is registered for    
        subjects_list = Subject.objects.filter(student_group=request.user.profil.group)
    else:
        print("user unknown")
        subjects_list = []

    return render(request,'subjects_template.html',{'subjects_list':subjects_list})

@login_required
def subjects_get_detail_view(request,subject_id): # show the details of a subject
    subject = get_object_or_404(Subject,id=subject_id)
    return render(request,'subject_detail_template.html',{subject:subject})

def get_prof_subjects(prof_id): #TODO fix dis
    return Subject.objects.filter(prof=get_object_or_404(Profil,id=prof_id)).all()

def get_student_subjects(student_id): #TODO fix dis
    return Subject.objects.filter(prof=get_object_or_404(Profil,id=student_id).profil.group.all())

def is_subject_manager(user_id,subject_id): # to know if the logged user teaches a specific subject
    user = get_object_or_404(get_user_model(),id=user_id)
    subject = get_object_or_404(Subject,id=subject_id)
    if user.profil.type == '2':
        return True
    else:
        if user.profil.type == '1':
            prof_subjects_list = Subject.objects.filter(prof=user.profil.group.all())
            if subject in prof_subjects_list:
                return True
    return False

@login_required
def subjects_add_user(user_id,subject_id):
    # add a user to a subject
    if not is_subject_manager(user_id,subject_id):
        return False
    
    user = get_object_or_404(get_user_model(),id=user_id)
    subject = get_object_or_404(Subject,id=subject_id)
    if user.profil.type == '1':
        subject.prof.add(user.profil)
    elif user.profil.type == '0':
        subject.student_group.add(user.profil.group)


@login_required
def subjects_remove_user(user_id,subject_id):
    pass
