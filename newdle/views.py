from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from absence.models import Absence
from profil.models import Profil
from absence.views import get_subjects,get_subjects_prof
from subjects.models import Subject

def index(request):
    return render(request, 'index.html')

@login_required
def principal(request):
    user = Profil.objects.get(user=request.user)
    type = user.type
    match type:
        case '0':
            subjects = get_subjects(user.id)
        case '1':
            subjects = get_subjects_prof(user.id)
        case '2':
            subjects = Subject.objects.all()
    n_abs = None
    n_late = None
    absences_data = []
    
    if type == '0':
        absences = Absence.objects.filter(student=user.id, status='0').values('subject_id', 'subject__name').annotate(absence_count=Count('id'))
        
        # Créer une liste de sujets avec absences
        for subject in subjects:
            subject_absences = next((item for item in absences if item['subject_id'] == subject.id), None)
            if subject_absences:
                absences_data.append({
                    'subject': subject,
                    'absence_count': subject_absences['absence_count']
                })
            else:
                absences_data.append({
                    'subject': subject,
                    'absence_count': 0
                })
    
    context = {
        'subjects_with_absences': absences_data,
        'type': type,
    }
    return render(request, 'principal.html',context)

def eco(request):
    return render(request, 'eco.html')

def contact(request):
    return render(request, 'contact.html')

def page_404(request, exception):
    return render(request, '404.html', status=404)