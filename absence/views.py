from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from profil.models import Profil
from subjects.models import Subject
from .models import Absence, ClassPhoto, Pin
from .forms import AbsenceForm, AbsenceFormT, AttendanceForm, DateForm, EditAbsenceForm, PhotoUploadForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from django.core.paginator import Paginator
# Create your views here.

def is_prof(subject_id,profil_id):
    subject = Subject.objects.get(name=subject_id)
    user = Profil.objects.get(id=profil_id)
    if subject.prof.filter(user_id = user.id).exists() :
        return True
    return False

def is_student(subject_id, profil_id):
    subject = Subject.objects.get(name=subject_id)
    user = Profil.objects.get(id=profil_id)
    if subject.student_group.filter(id__in=user.group.all()).exists():
        return True
    return False

class AbsenceView(View):
    @method_decorator(login_required)
    def get(self, request,id=None):
        user = Profil.objects.get(user=request.user)
        subject = Subject.objects.get(name=id)
        student_group = subject.student_group
        if user.type == '0' and is_student(subject.name, user.id):
            if id is None or 'details' in request.GET:
                absences = Absence.objects.filter(student=Profil.objects.get(user=request.user)).order_by('-date')
                paginator = Paginator(absences, 10)
                page_number = request.GET.get('page')
                absences = paginator.get_page(page_number)
                return render(request, 'absence/absence.html', {'mode': 'details', 'absences': absences, 'level': int(Profil.objects.get(user=request.user).type), 'subject_id': id })
            else:
                form = AbsenceForm()
                return render(request, 'absence/absence.html', {'mode': 'input', 'form': form})
        elif (user.type == '1' and is_prof(subject.name, user.id)) or user.type == '2' :
            if id is None or 'details' in request.GET:
                absences = Absence.objects.filter(subject=Subject.objects.get(name=id)).order_by('-date')
                paginator = Paginator(absences, 10)
                page_number = request.GET.get('page')
                absences = paginator.get_page(page_number)
                return render(request, 'absence/absence.html', {'mode': 'details', 'absences': absences, 'level': int(Profil.objects.get(user=request.user).type), 'subject_id': id})
            elif 'attendance' in request.GET:
                form = AttendanceForm(subject=subject)
                context = {
                    'mode': 'attendance',
                    'form': form,
                    'level': int(Profil.objects.get(user=request.user).type),
                    'subject_id': id
                }
                return render(request, 'absence/absence.html', context)
            else:
                form = AbsenceFormT(subject=subject)
                context = {
                    'mode': 'input',
                    'form': form,
                    'level': int(Profil.objects.get(user=request.user).type),
                    'subject_id': id
                }
                return render(request, 'absence/absence.html', context)
            
        else :
            return redirect('group:show')
    @method_decorator(login_required)
    def post(self, request,id):
        user = Profil.objects.get(user=request.user)
        subject = Subject.objects.get(name=id)
        student_group = subject.student_group
        if user.type == '0' and user.group.name == student_group.name :
            form = AbsenceForm(request.POST)
            now = datetime.now()
            if form.is_valid():
                absence = form.save(commit=False)
                absence.student = Profil.objects.get(user=request.user)
                absence.subject = Subject.objects.get(name=id)
                absence.date = now
                absence.save()
                return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details")  
            return render(request, 'absence/absence.html', {'mode': 'input', 'form': form})
        elif (user.type == '1' and is_prof(subject.name, user.id)) or user.type == '2' :
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
                return render(request, 'absence/absence.html', {'mode': 'attendance', 'form': form})
            else :      
                form = AbsenceFormT(request.POST,subject=subject)
                now = datetime.now()
                if form.is_valid():
                    absence = form.save(commit=False)
                    absence.subject = Subject.objects.get(name=id)
                    absence.save()
                    return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details")  
                return render(request, 'absence/absence.html', {'mode': 'input', 'form': form})
        else :
            return redirect('group:show')
            
            
            
def index_view(request):
    return render(request, 'index.html')

@login_required
def delete_absence(request, id):
    if request.method == 'POST':
        absence_id = request.POST.get('absence_id')
        if absence_id:
            absence = get_object_or_404(Absence, id=absence_id)
            absence.delete()
    return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details") 


@login_required
def edit_absence(request, id):
    absence = get_object_or_404(Absence, id=id)
    if request.method == 'POST':
        form = EditAbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            return redirect(reverse('absence:absence', kwargs={'id': absence.subject.name}) + '?details')
    else:
        form = EditAbsenceForm(instance=absence)
    return render(request, 'absence/edit_absence.html', {'form': form, 'absence': absence})


@login_required
def upload_photo_view(request,id):
    subject = get_object_or_404(Subject, name=id)
    user = Profil.objects.get(user=request.user)
    if is_prof(subject.name, user.id) or user.type == '2':
        
        if request.method == 'POST':
            form = PhotoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.subject = Subject.objects.get(name=id)
                photo.save()
                return redirect(reverse('absence:absence', kwargs={'id': id}) + '?details')
        else:
            form = PhotoUploadForm()
        return render(request, 'absence/upload_photo.html', {'form': form})
    else :
        return redirect(reverse('absence:absence', kwargs={'id': id}) + '?details')


@login_required
def mark_presence_view(request, id):
    time_threshold = datetime.now() - timedelta(hours=2)
    subject = Subject.objects.get(name=id)
    user = Profil.objects.get(user=request.user)
    
    if user.type == '0':
        selected_photo_id = request.GET.get('photo')
        selected_photo = None
        mode = 'npinned'
        photos = ClassPhoto.objects.filter(subject=subject).order_by('-upload_date')
    
    
        if selected_photo_id:
            selected_photo = get_object_or_404(ClassPhoto, pk=selected_photo_id, subject=subject)
            pins = Pin.objects.filter(photo=selected_photo)
        
        if Pin.objects.filter(photo=selected_photo, user=user).exists():
            mode = 'pinned'
    

        if ClassPhoto.objects.filter(subject=subject.id).exists():
            if request.method == 'POST':
                try:
                    x = float(request.POST['x']) * 100
                    y = float(request.POST['y']) * 100
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid coordinates.'})

                if not Pin.objects.filter(photo=selected_photo, user=user).exists():
                    pin = Pin(photo=selected_photo, user=user, x=x, y=y)
                    pin.save()
                    return JsonResponse({'status': 'ok', 'pin_id': pin.id})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Vous avez déjà placé un pin.'})

            pins = Pin.objects.filter(photo=selected_photo)
            user_pin = pins.filter(user=user).first()
            user_pin_data = None
            user_pin_id = None
            if user_pin:
                user_pin_data = {
                    'x': user_pin.x,
                    'y': user_pin.y
                }
                user_pin_id = user_pin.id
            return render(request, 'absence/mark_presence.html', { 'mode':mode,'subject':id, 'pins': pins,'user_pin': user_pin, 'user_pin_data': user_pin_data,'photos': photos,
            'selected_photo': selected_photo, 'user_pin_id': user_pin_id})
        else :
            return render(request, 'absence/mark_presence.html', {'mode':'nophoto', 'subject':id})
    else :
        return redirect(reverse('absence:absence', kwargs={'id': id}) + '?details')
    
    
def get_subjects(profil_id):
        user = Profil.objects.get(id=profil_id)
        groups = user.group.all()
        subjects = Subject.objects.filter(student_group__in=groups).distinct()
        return subjects
def get_subjects_prof(profil_id):
        user = Profil.objects.get(id=profil_id)
        subjects =  Subject.objects.filter(prof = user.id).distinc()
        return subjects
      
@login_required
def absence_main(request):
    user = Profil.objects.get(user=request.user)
    type = user.type
    match type:
        case 0:
            subjects = get_subjects(user.id)
        case 1:
            subjects = get_subjects_prof(user.id)
        case 2:
            subjects = Subject.objects.all()


    return render(request, 'absence/absence_main.html', {'subjects':subjects, 'type':type})

@login_required
def check_photo(request,id):
    subject = get_object_or_404(Subject, name=id)
    user = Profil.objects.get(user=request.user)
    
    if is_prof(subject.name, user.id) or user.type == '2':
        
        selected_photo_id = request.GET.get('photo')
        selected_photo = None
        pins = []


        photos = ClassPhoto.objects.filter(subject=subject).order_by('-upload_date')
    
    
        if selected_photo_id:
            selected_photo = get_object_or_404(ClassPhoto, pk=selected_photo_id, subject=subject)
            pins = Pin.objects.filter(photo=selected_photo)
        
        return render(request, 'absence/check_photo.html', {
            'photos': photos,
            'selected_photo': selected_photo,
            'pins': pins,
            'subject': subject
        })
    else :
        return redirect(reverse('absence:absence', kwargs={'id': id}) + '?details')

@login_required
def mark_presence_delete(request, id):
    user = Profil.objects.get(user=request.user)
    selected_photo_id = request.GET.get('photo')
    subject = Subject.objects.get(name=id)

    if request.method == 'POST':
        pin_id = request.POST.get('pin_id')
        print(f"Received pin_id: {pin_id}")
        if pin_id:
            pin = get_object_or_404(Pin, id=pin_id, user=user)
            pin.delete()
            return HttpResponseRedirect(reverse('absence:mark_presence', kwargs={'id': id}))

    # Rediriger vers la page d'origine si la requête n'est pas POST ou si l'ID du pin est manquant
    return HttpResponseRedirect(reverse('absence:mark_presence', kwargs={'id': id}))