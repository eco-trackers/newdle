from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

@login_required
def principal(request):
    return render(request, 'principal.html')

def eco(request):
    return render(request, 'eco.html')

def contact(request):
    return render(request, 'contact.html')

def page_404(request, exception):
    return render(request, '404.html', status=404)