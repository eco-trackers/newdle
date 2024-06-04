from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Profil

@login_required
def profil_render(request):
    profil = get_object_or_404(Profil, user=request.user)
    return render(request, 'account.html',{'profil':profil})

def index_view(request):
    return render(request, 'index.html')