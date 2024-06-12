from django.shortcuts import render, redirect
from .models import Note
from django.contrib.auth.decorators import login_required
from .forms import NoteCreateForm
from subjects.models import Subject,UE
from profil.models import Profil


# def get_prof_subjects(request):
#     return Subject.objects.filter(prof=request.user.profil).all()

def get_all_student_notes(request):
    """
        format
        [
            {
                "subject":"subjectName",
                "UE":UE,
                "coef":coefValue,
                "note":noteValue (default -1)
            },
            ...
        ]
    """
    notes = []
    subjects = Subject.objects.all()
    for subject in subjects:
        # get not if exists
        note = -1
        try:
            note = int("{:,.0f}".format(Note.objects.get(profil=request.user.profil,subject=subject).valeur))
        except:
            pass

        notes.append({
            "subject":subject.name,
            "UE":subject.ue,
            "coef":subject.coef,
            "note":note
        })
    return notes

def get_formatted_notes(request):
    """
        in format
        [
            {
                "name":"UE",
                "count":noteCount,
                "notes":[
                    {
                        "subject":"subjectName",
                        "note":noteValue (default -1),
                        "coef":coefValue
                    },
                    ...
                ]
            }
            ...
        ]
    """
    subjects = get_all_student_notes(request)
    ues = []
    ues_list = []
    for subject in subjects:
        ue = subject["UE"]
        if ue not in ues_list:
            ues_list.append(ue)
            ues.append({
                "name":ue,
                "count":0,
                "notes":[]
            })
        
        for ue in ues:
            if ue["name"] == subject["UE"]:
                ue["count"] += 1
                ue["notes"].append({
                    "subject":subject["subject"],
                    "note":subject["note"],
                    "coef":subject["coef"]
                })
    print(ues)
    return ues
        
def get_notes(request,subject_id):
    """
        format
        [
            {
                "Studdent":Profil,
                "note":noteValue (default -1)
            },
            ...
        ]
    """

    notes = []
    # get subject group
    subject = Subject.objects.get(id=subject_id)
    # get all students in the groups (subject.student_group is many to many field so we need to get all students in the group)
    groups = subject.student_group.all()
    students = []
    for group in groups:
        # add only if the student is not already in the list
        for student in group.profil_set.all():
            if student not in students and student.type == '0':
                students.append(student)
        
    for student in students:
        # get note if exists
        note = -1
        try:
            note = int("{:,.0f}".format(Note.objects.get(profil=student,subject=subject).valeur))
        except:
            pass

        notes.append({
            "student":student,
            "note":note
        })
    return notes


# views

@login_required
def list_view(request):
    # test which role the user has
    if int(Profil.objects.get(user=request.user).type) > 0:
        return redirect('notes:edit.view')

    # if not redirect => you are a studdent

    # Retrieve all notes from the database
    ues = get_formatted_notes(request)

    # Render the template with the list of notes
    return render(request, 'notes/list_notes.html', {'ues': ues})


@login_required
def edit_view(request):
    # test which role the user has
    subjects = []
    match int(Profil.objects.get(user=request.user).type):
        case 0:
            redirect('notes:list.view')
        case 1:
            subjects = Subject.objects.filter(prof=Profil.objects.get(user=request.user)).all()
        case _:
            subjects = Subject.objects.all()
    return render(request, 'notes/subjects_note.html', {'subjects': subjects})

@login_required
def edit_detail(request,id):
    # test which role the user has
    if Profil.objects.get(user=request.user).type == '0':
        return redirect('notes:list.view')
    elif Profil.objects.get(user=request.user).type == '1' and not Subject.objects.get(id=id).prof == Profil.objects.get(user=request.user):
        return redirect('notes:edit.view')
    # get all students notes
    notes = get_notes(request,id)
    
    if request.method == 'POST':
        for note in notes:
            value = request.POST.get("note"+str(note["student"].id))
            print(value)
            if value == None or value == '':
                continue
            try:
                note_obj = Note.objects.get(profil=note["student"],subject=Subject.objects.get(id=id))
                note_obj.valeur = value
                note_obj.save()
            except:
                note_obj = Note(
                    profil=note["student"],
                    subject=Subject.objects.get(id=id),
                    valeur=value
                )
                note_obj.save()
        return redirect('notes:edit.view')

    # Render the template with the list of notes
    return render(request, 'notes/subject_detail.html', {'notes': notes,'subject':Subject.objects.get(id=id)})
    