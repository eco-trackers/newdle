from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from profil.models import Profil
from subjects.models import Subject
from .models import Absence
from .forms import AbsenceForm, AbsenceFormT, AttendanceForm, EditAbsenceForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.

class AbsenceView(View):
    @method_decorator(login_required)
    def get(self, request,id=None):
        if Profil.objects.get(user=request.user).type == '0' :
            if id is None or 'details' in request.GET:
                absences = Absence.objects.filter(student=Profil.objects.get(user=request.user)).order_by('-date')
                paginator = Paginator(absences, 10)
                page_number = request.GET.get('page')
                absences = paginator.get_page(page_number)
                return render(request, 'absence.html', {'mode': 'details', 'absences': absences})
            else:
                form = AbsenceForm()
                return render(request, 'absence.html', {'mode': 'input', 'form': form})
        elif Profil.objects.get(user=request.user).type == '1' :
            subject = Subject.objects.get(name=id)
            if id is None or 'details' in request.GET:
                absences = Absence.objects.filter(subject=Subject.objects.get(name=id)).order_by('-date')
                paginator = Paginator(absences, 10)
                page_number = request.GET.get('page')
                absences = paginator.get_page(page_number)
                return render(request, 'absence.html', {'mode': 'details', 'absences': absences})
            elif 'attendance' in request.GET:
                form = AttendanceForm(subject=subject)
                return render(request, 'absence.html', {'mode': 'attendance','form': form})
            else:
                form = AbsenceFormT(subject=subject)
                return render(request, 'absence.html', {'mode': 'input', 'form': form})
    @method_decorator(login_required)
    def post(self, request,id):
        if Profil.objects.get(user=request.user).type == '0' :
            form = AbsenceForm(request.POST)
            now = datetime.now()
            if form.is_valid():
                absence = form.save(commit=False)
                absence.student = Profil.objects.get(user=request.user)
                absence.subject = Subject.objects.get(name=id)
                absence.date = now
                absence.save()
                return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details")  
            return render(request, 'absence.html', {'mode': 'input', 'form': form})
        elif Profil.objects.get(user=request.user).type == '1' :
            subject = Subject.objects.get(name=id)    
            if 'attendance' in request.GET: 
                form = AttendanceForm(request.POST,subject=subject)
                if form.is_valid():
                    attendance_date = form.cleaned_data['date']
                    student_groups = subject.student_group.all()
                    students = Profil.objects.filter(group__in=student_groups)
                    for student in students:
                        status = form.cleaned_data[f'student_{student.id}']
                        absence = Absence.objects.create(
                            student=student,
                            subject=subject,
                            status=status,
                            date=attendance_date
                        )
                        absence.save() 
                    return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details")
                return render(request, 'absence.html', {'mode': 'attendance', 'form': form})
            else :      
                form = AbsenceFormT(request.POST,subject=subject)
                now = datetime.now()
                if form.is_valid():
                    absence = form.save(commit=False)
                    absence.subject = Subject.objects.get(name=id)
                    absence.save()
                    return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details")  
                return render(request, 'absence.html', {'mode': 'input', 'form': form})
            
            
            
def index_view(request):
    return render(request, 'index.html')


def delete_absence(request, id):
    if request.method == 'POST':
        absence_id = request.POST.get('absence_id')
        if absence_id:
            absence = get_object_or_404(Absence, id=absence_id)
            absence.delete()
    return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details") 

def edit_absence(request, id):
    absence = get_object_or_404(Absence, id=id)
    if request.method == 'POST':
        form = EditAbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            return redirect(reverse('absence:absence', kwargs={'id': absence.subject.name}) + '?details')
    else:
        form = EditAbsenceForm(instance=absence)
    return render(request, 'edit_absence.html', {'form': form, 'absence': absence})
