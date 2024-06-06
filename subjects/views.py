from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Subject

# 0 etudiant
# 1 prof
# 2 admin

# managament of subjects only, for marks, check

#TODO redirect all backend views back to their src page
#TODO replace user id with profile id


# frontend view
@login_required
def subjects_home_view(request): # show the list of subjects to manage
    if request.user.profil.type == '2': # if admin, list the id of all subjects
        subjects_list = Subject.objects.all()
    elif request.user.profil.type == '1': # if prof, list only the subjects he is responsible for
        subjects_list = get_prof_subjects(request.user.id)
    elif request.user.profil.type == '0': # if etudiant, list only the subjects he is registered for    
        subjects_list = get_student_subjects(request.user.profile.id)
    else:
        print("user unknown")
        subjects_list = []
    print(subjects_list)
    return render(request,'subjects/subjects_template.html',{'subjects_list':subjects_list})


#frontend view
@login_required
def subjects_get_detail_view(request,subject_id): # show the details of a subject
    subject = get_object_or_404(Subject,id=subject_id)
    return render(request,'subject_detail_template.html',{'subject':subject})


# super backend view
@login_required
def get_prof_subjects(prof_id): #TODO fix dis
    return Subject.objects.filter(prof=get_object_or_404(Profil,id=prof_id)).all()


# super backend view
@login_required
def get_student_subjects(student_id): #TODO fix dis
    return Subject.objects.filter(student_group=get_object_or_404(Group,id=student_id)).all()


#super backend view, TODO check queryset
@login_required
def is_subject_manager(user_id,subject_id): # to know if the logged user teaches a specific subject
    user = get_object_or_404(get_user_model(),id=user_id)
    subject = get_object_or_404(Subject,id=subject_id)
    if user.profil.type == '2':
        return True
    else:
        if user.profil.type == '1': # is a teacher
            if subject in Subject.objects.filter(prof=user.profil.group.all()): # see if subject is in the list of subjects the prof can manage
                return True
    return False



# -----------------------
# managing the courses


# super backend view
@login_required
def subjects_add_group(group_id,subject_id):    # add a group to course
    if not is_subject_manager(request.user,subject_id):  # check if user is a teacher that is manager of the course
        return False
    subject.student_group.add(get_object_or_404(Group,id=group_id))
    return True


# super backend view
@login_required
def subjects_remove_group(group_id,subject_id):    # remove group from course
    if not is_subject_manager(request.user,subject_id):  # check if user is a teacher that is manager of the course
        return False
    subject.student_group.add(get_object_or_404(Group,id=group_id))
    return True
