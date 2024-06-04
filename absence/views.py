from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from profil.models import Profil
from subjects.models import Subject
from .models import Absence
from .forms import AbsenceForm
from django.contrib.auth.decorators import login_required
# Create your views here.


class AbsenceView(View):
    def get(self, request,id='Det'):
        if 'details' in request.GET:
            absences = Absence.objects.filter(student=Profil.objects.get(user=request.user))
            return render(request, 'absence.html', {'mode': 'details', 'absences': absences})
        else:
            form = AbsenceForm()
            return render(request, 'absence.html', {'mode': 'input', 'form': form})

    def post(self, request,id):
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.student = Profil.objects.get(user=request.user)
            absence.subject = Subject.objects.get(name=id)
            absence.save()
            return redirect(reverse('absence:absence') + '?details')  
        return render(request, 'absence.html', {'mode': 'input', 'form': form})
    
def index_view(request):
    return render(request, 'index.html')
