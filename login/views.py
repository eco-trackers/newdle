from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from profil.models import Profil, Group

def sign_up(request):
    if request.method == 'POST':
        # Create the form
        form = UserCreationForm(request.POST)

        # Modify the messages dinamacally
        form.fields['username'].help_text = ''#Will be displayed
        form.fields['password1'].help_text = ''#Decide a new password
        
        if form.is_valid():
            user = form.save()
            profil = Profil.objects.create(user=user, type='0')
            default_group, created = Group.objects.get_or_create(name='default')
            profil.group.add(default_group)
            return render(request, 'index.html')
    else:
        # If method is not post
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'connection.html', context)

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/principal/')
    else:
        form = AuthenticationForm()
    return render(request, 'connection.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')
