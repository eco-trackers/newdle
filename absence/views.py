from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from profil.models import Profil
from .models import Absence
from .forms import AbsenceForm
from django.contrib.auth.decorators import login_required
# Create your views here.


class AbsenceView(View):
    def get(self, request):
        if 'details' in request.GET:
            absences = Absence.objects.filter(student=Profil.objects.get(user=request.user))
            return render(request, 'absence.html', {'mode': 'details', 'absences': absences})
        else:
            form = AbsenceForm()
            return render(request, 'absence.html', {'mode': 'input', 'form': form})

    def post(self, request):
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.student = Profil.objects.get(user=request.user)
            absence.save()
            return redirect(reverse('absence:absence') + '?details')  
        return render(request, 'absence.html', {'mode': 'input', 'form': form})
    
def index_view(request):
    return render(request, 'index.html')
