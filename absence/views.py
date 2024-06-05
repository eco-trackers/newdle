from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from profil.models import Profil
from subjects.models import Subject
from .models import Absence
from .forms import AbsenceForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from django.core.paginator import Paginator
import pytz
# Create your views here.

class AbsenceView(View):
    @method_decorator(login_required)
    def get(self, request,id=None):
        if id is None or 'details' in request.GET:
            absences = Absence.objects.filter(student=Profil.objects.get(user=request.user)).order_by('-date')
            paginator = Paginator(absences, 10)
            page_number = request.GET.get('page')
            absences = paginator.get_page(page_number)
            return render(request, 'absence.html', {'mode': 'details', 'absences': absences})
        else:
            form = AbsenceForm()
            return render(request, 'absence.html', {'mode': 'input', 'form': form})
    @method_decorator(login_required)
    def post(self, request,id):
        form = AbsenceForm(request.POST)
        local_tz = pytz.timezone('Europe/Paris')
        now = datetime.now(local_tz)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.student = Profil.objects.get(user=request.user)
            absence.subject = Subject.objects.get(name=id)
            absence.date = now
            absence.save()
            return redirect(f"{reverse('absence:absence', kwargs={'id': id})}?details")  
        return render(request, 'absence.html', {'mode': 'input', 'form': form})
    
def index_view(request):
    return render(request, 'index.html')
