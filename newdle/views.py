from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from absence.models import Absence
from notes.models import Note
from notes.views import get_notes
from profil.models import Profil
from absence.views import get_subjects,get_subjects_prof
from subjects.models import Subject

def index(request):
    return render(request, 'index.html')

@login_required
def principal(request):
    user = Profil.objects.get(user=request.user)
    type = user.type
    absences_data = []
    n_abs = None
    n_late = None
    note = None
    match type:
        case '0':
            subjects = get_subjects(user.id)
            absences = Absence.objects.filter(student=user.id, status='0').values('subject_id', 'subject__name').annotate(absence_count=Count('id'))
            n_abs =  Absence.objects.filter(student=user.id, status='0').count()
            n_late =  Absence.objects.filter(student=user.id, status='1').count()
        case '1':
            subjects = get_subjects_prof(user.id)
            absences = Absence.objects.filter(status='0').values('subject_id', 'subject__name').annotate(absence_count=Count('id'))
        case '2':
            subjects = Subject.objects.all()
            absences = Absence.objects.filter(status='0').values('subject_id', 'subject__name').annotate(absence_count=Count('id'))

    
    for subject in subjects:
        subject_absences = next((item for item in absences if item['subject_id'] == subject.id), None)
        notes = get_notes(request, subject.id)
        if type == '0':
            note =  note = next((item['note'] for item in notes if item['student'] == user), 'Aucune')
        else :
            i=0
            n=0
            for item in notes:
                n += item['note']
                i += 1
            if i != 0:
                note = n/i
                    
        if subject_absences:
            absences_data.append({
                'subject': subject,
                'absence_count': subject_absences['absence_count'],
                'note': note
            })
        else:
            absences_data.append({
                'subject': subject,
                'absence_count': 0,
                'note': note
            })

    context = {
        'subjects_with_absences': absences_data,
        'type': type,
        'n_abs': n_abs,
        'n_late':n_late
    }
    return render(request, 'principal.html',context)

def eco(request):
    return render(request, 'eco.html')

def contact(request):
    return render(request, 'contact.html')

def page_404(request, exception):
    return render(request, '404.html', status=404)