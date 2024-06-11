from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from group.models import Group
from profil.models import Profil
from .models import Subject,UE
from django.contrib import messages

# 0 etudiant
# 1 prof
# 2 admin


@login_required
def get_prof_ue(request):
    return_list = []
    if request.user.profil.type == '2':
        return UE.objects.all()
    elif request.user.profil.type == '1':
        for subject in get_prof_subjects(request):
            if request.user.profil in subject.prof.all():
                return_list.append(subject.ue)
    else:
        return []

# frontend view
@login_required
def subjects_home_view(request):  # show the list of subjects to manage
    
    ue_dict = {}

    if request.user.profil.type == '2':  # if admin, list the id of all subjects
        ue_list = UE.objects.all()
    elif request.user.profil.type == '1':  # if prof, list only the subjects he is responsible for
        ue_list = get_prof_ue(request)
    elif request.user.profil.type == '0':  # if etudiant, list only the subjects he is registered for
        ue_list = get_student_ues(request)
    else:
        print("user unknown")
        ue_dict = {}
    
    if ue_list is not None:
        for ue in ue_list:
            ue_dict[ue] = get_ue_subjects(request,ue)

    #return render(request, 'subjects/subjects_template.html', {'subjects_list': subjects_list})
    return render(request, 'matières.html',{'ue_dict':ue_dict})


# frontend view
@login_required
# show the details of a subject
def subjects_get_detail_view(request, subject_id):
    # if is_subject_manager(request,subject_id) is False:
    #     # permission denied
    #     return redirect('subjects:subjects-home-view')
    subject = get_object_or_404(Subject, id=subject_id)
    context = { 'subject_id':subject.id,
                'subject_name': subject.name,
                'subject_coef': subject.coef,
                'subject_ue': subject.ue,
                'subject_prof': subject.prof.all(),
                'subject_student_list': get_subject_students(request,subject_id),
                'subject_group_list': subject.student_group.all(),
                'can_manage_subject': is_subject_manager(request,subject_id)}
    #return render(request, 'subjects/subject_detail_template.html', context)
    return render(request, 'matière.html',context)

@login_required
def get_subject_students(request,subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    student_list = []

    for group in subject.student_group.all():
        student_list.append(group.profil_set.all())
    return student_list


# super backend view
@login_required
def get_prof_subjects(request):
    if request.user.profil.type == '2':
        return Subject.objects.all()
    elif request.user.profil.type == '1':
        return Subject.objects.filter(prof=request.user.profil).all()
    else:
        return []


# super backend view
@login_required
def get_student_subjects(request):  # get courses the student is enrolled in
    groups = Profil.objects.get(user=request.user).group.all()
    return Subject.objects.filter(student_group__in=groups).distinct()


# super backend view, TODO check queryset
@login_required
# to know if the logged user teaches a specific subject
def is_subject_manager(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.user.profil.type == '2':
        return True
    else:
        if request.user.profil.type == '1':  # is a teacher
            # see if subject is in the list of subjects the prof can manage
            if subject in get_prof_subjects(request):
                return True
    return False



# -----------------------
# managing the courses

# super backend view
@login_required
def subjects_add_group(request, subject_id,group_id):    # add a group to course
    # check if user is a teacher that is manager of the course
    if not is_subject_manager(request.user, subject_id):
        return redirect('subjects:subjects-home-view')
    subject.student_group.add(get_object_or_404(Group, id=group_id))
    return redirect('subjects:subjects-get-detail-view', subject_id)


# super backend view
@login_required
def subjects_remove_group(request, subject_id,group_id):  # remove group from course
    # check if user is a teacher that is manager of the course
    if not is_subject_manager(request.user, subject_id):
        return redirect('subjects:subjects-home-view')
    subject.student_group.remove(get_object_or_404(Group, id=group_id))
    return redirect('subjects:subjects-get-detail-view', subject_id)

@login_required
def subjects_add_prof(request, subject_id,prof_id): # add a prof to course as manager
    if not is_subject_manager(request.user, subject_id):
        return redirect('subjects:subjects-home-view')
    
    subject = get_object_or_404(Subject, id=subject_id)
    subject.prof.add(get_object_or_404(Profil, id=prof_id))
    
    return render(request, 'subjects/subject_detail_template.html', {'subject': subject})

@login_required
def subjects_remove_prof(request, subject_id,prof_id):
    if not is_subject_manager(request.user, subject_id):
        return redirect('subjects:subjects-home-view')
    
    subject = get_object_or_404(Subject, id=subject_id)
    subject.prof.remove(get_object_or_404(Profil, id=prof_id))

    return render(request, 'subjects/subject_detail_template.html', {'subject': subject})


@login_required
def create_subject(request):
    if request.user.profil.type == '0':
        return redirect('subjects:subjects-home-view')

    if request.method == 'POST':
        subject = Subject()
        subject.name = request.POST['name']
        subject.coef = request.POST['coef']
        
        ue_id = request.POST['ue']
        prof_id_list = request.POST.getlist('prof')
        group_id_list = request.POST.getlist('group')

        subject.ue = UE.objects.filter(id=ue_id)[0]

        subject.save()

        if len(group_id_list) > 0:
            for group_id in group_id_list:
                subject.student_group.add(get_object_or_404(Group, id=group_id))# add the group to the list of groups
            print(f"added {len(group_id_list)} groups to the ue list")
        else:
            messages.error(request, "No group selected! Please select a group")
            return render(request, 'subjects/subject_create.html',{'ue_list': UE.objects.all(),
                  'prof_list': Profil.objects.filter(type='1').all(),
                  'group_list': Group.objects.all()}) # eror msg
        
        if len(prof_id_list) > 0:
            for prof_id in prof_id_list:
                subject.prof.add(get_object_or_404(Profil, id=prof_id))# add the group to the list of groups
            print(f"added {len(UE.objects.filter(id__in=prof_id_list))} profs to the ue list")
        
        
        
        

        subject.save()
        return redirect('subjects:subjects-home-view')
    else:

        context = {'ue_list': UE.objects.all(),
                  'prof_list': Profil.objects.filter(type='1').all(),
                  'group_list': Group.objects.all()}
        
        return render(request, 'subject_create.html',context)
        

@login_required
def edit_view(request,subject_id):
    if not is_subject_manager(request, subject_id):
        return redirect('subjects:subjects-home-view')
    
    if request.method == 'POST':
        subject = get_object_or_404(Subject, id=subject_id)
        
        subject.name = request.POST['name']
        subject.coef = request.POST['coef']
        
        ue_id = request.POST['ue']
        prof_id_list = request.POST.getlist('prof')
        group_id_list = request.POST.getlist('group')

        subject.ue = UE.objects.filter(id=ue_id)[0]

        if len(group_id_list) > 0:
            subject.student_group.clear()
            for group_id in group_id_list:
                subject.student_group.add(get_object_or_404(Group, id=group_id))# add the group to the list of groups
            #print(f"added {len(group_id_list)} groups to the ue list")
        else:
            messages.error(request, "No group selected! Please select a group")
            return render(request, 'subject_edit.html',{   'subject': get_object_or_404(Subject, id=subject_id),
                  'ue_list': UE.objects.all(),
                  'prof_list': Profil.objects.filter(type='1').all(),
                  'group_list': Group.objects.all()}) # need to add messgae block to base for eror msg to appear
        
        if len(prof_id_list) > 0:
            subject.prof.clear()
            for prof_id in prof_id_list:
                subject.prof.add(get_object_or_404(Profil, id=prof_id))# add the group to the list of groups
            #print(f"added {len(UE.objects.filter(id__in=prof_id_list))} profs to the ue list")
        
        

        subject.save()
        return redirect('subjects:subjects-get-detail-view',subject_id)

    context = {   'subject': get_object_or_404(Subject, id=subject_id),
                  'ue_list': UE.objects.all(),
                  'prof_list': Profil.objects.filter(type='1').all(),
                  'group_list': Group.objects.all(),
                  'subject_ue': get_object_or_404(Subject, id=subject_id).ue,}


    return render(request, 'subject_edit.html', context)

@login_required
def delete_subject(request,subject_id):
    if not is_subject_manager(request, subject_id):
        return subjects_get_detail_view(request, subject_id)
    
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()

    return redirect('subjects:subjects-home-view')

@login_required
def get_student_ues(request):
    
    student_groups = Profil.objects.get(user=request.user).group.all()
    
    
    subjects = Subject.objects.filter(student_group__in=student_groups).distinct()
    
    
    ues = list(set([subject.ue for subject in subjects]))
    
    return ues


@login_required
def ue_home_view(request):
    if request.user.profil.type == '2':
        return render(request, 'subjects/ue_template.html', {'ue_list': UE.objects.all()})
    elif request.user.profil.type == '1':
        return render(request, 'subjects/ue_template.html', {'ue_list': UE.objects.all()})
    elif request.user.profil.type == '0':
        return render(request, 'subjects/ue_template.html', {'ue_list': get_student_ues(request)})

@login_required
def is_ue_manager(request, ue_id):
    if request.user.profil.type == '2':
        return True
    elif request.user.profil.type == '1':
        return True
    elif request.user.profil.type == '0':
        return False
    else:
        return False

@login_required
def ue_get_detail_view(request,ue_id):
    if not is_ue_manager(request, ue_id):
        return redirect('subjects:ue-home-view')
    ue = get_object_or_404(UE, id=ue_id)
    return render(request, 'subjects/ue_detail_template.html', {'ue': ue,
        'can_manage_ue': is_ue_manager(request, ue_id)
    })



@login_required
def create_ue(request):
    if request.user.profil.type == '0':
        return redirect('subjects:ue-home-view')
    
    if request.method == 'POST':
        ue = UE()
        #TODO sanitize inputs
        ue.name = request.POST['name']
        ue.semester = request.POST['semester']
        ue.coef = request.POST['coef']
        ue.save()
        return redirect('subjects:ue-home-view')
    else:
        return render(request, 'subjects/ue_create.html')


@login_required
def is_ue_manager(request, ue_id):
    if request.user.profil.type == '2':
        return True
    elif request.user.profil.type == '1':
        return True
    elif request.user.profil.type == '0':
        return False
    else:
        return False

@login_required
def delete_ue(request,ue_id):
    if not is_ue_manager(request, ue_id):
        return ue_get_detail_view(request, ue_id)
    
    ue = get_object_or_404(UE, id=ue_id)
    ue.delete()

    return redirect('subjects:ue-home-view')

@login_required
def edit_ue_view(request,ue_id):
    if not is_ue_manager(request, ue_id):
        return ue_home_view(request)
    
    if request.method == 'POST':
        ue = get_object_or_404(UE, id=ue_id)

        ue.name = request.POST['name']
        ue.semester = request.POST['semester']
        ue.coef = request.POST['coef']


        ue.save()
        return redirect('subjects:ue-get-detail-view',ue_id)
    else:
        return render(request, 'subjects/ue_edit.html',{'ue': get_object_or_404(UE, id=ue_id)})


@login_required
def get_ue_subjects(request,input_ue):
    return Subject.objects.filter(ue=input_ue).all()

@login_required
def view_maquette(request):
    if request.user.profil.type == '0':
        
        ue_dict = {}

        if request.user.profil.type == '2':  # if admin, list the id of all subjects
            ue_list = UE.objects.all()
        elif request.user.profil.type == '1':  # if prof, list only the subjects he is responsible for
            ue_list = get_prof_ue(request)
        elif request.user.profil.type == '0':  # if etudiant, list only the subjects he is registered for
            ue_list = get_student_ues(request)
        else:
            print("user unknown")
            ue_dict = {}
        
        if ue_list is not None:
            for ue in ue_list:
                ue_dict[ue] = get_ue_subjects(request,ue)

        return render(request, 'subjects/maquette_template.html',{'ue_dict':ue_dict})
    else: # admin et profs pas de maquette a afficher
        return redirect('subjects:ue-home-view')