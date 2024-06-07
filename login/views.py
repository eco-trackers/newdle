from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from profil.models import Profil, Group
from django.core.files.storage import FileSystemStorage
import csv
import os
#from django.views.decorators.http import require_POST utile?

FROM_EMAIL='maxime.sanciaume@uha.fr'

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
    return render(request, 'login/connection.html', {'form': form})

def send_password_reset_email(user,email):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://127.0.0.1:8000/login/reset/{uid}/{token}/"
    subject = 'Password Reset'
    html_message = render_to_string('login/password_reset_email.html', {'username': user.username,'reset_link': reset_link})
    plain_message = strip_tags(html_message)
    from_email = FROM_EMAIL
    to_email = email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

@login_required
def tab_and_upload_csv_view(request):
    if not Profil.objects.get(user=request.user).type == '2':
        return render(request, 'index.html')
    
    data = []
    error = None

    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            error = 'Le fichier doit être un CSV.'
        else:
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)

            with open(fs.path(filename), newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';') #delimiter=; si besoin
                for row in reader:
                    data.append({
                        "nom": row.get("NOM", "").strip().lower(),
                        "prenom": row.get("Prénom", "").strip().lower(),
                        "email": row.get("email", "").strip().lower(),
                        "password": row.get("password", "").strip(),
                        "role": row.get("role", "").strip().lower(),
                    })
            
            os.remove(filename)
            
            User = get_user_model()

            # Créer ou mettre à jour les utilisateurs et profils
            for entry in data:
                first_name = entry["prenom"]
                last_name = entry["nom"]
                email = entry["email"]
                role = entry["role"]
                default_password = entry["password"] or User.objects.make_random_password()
                username = f"{first_name}.{last_name}@uha.fr"

                if role == 'student':
                    user_type = '0'
                elif role == 'professor':
                    user_type = '1'
                elif role == 'admin':
                    user_type = '2'
                else: # par défaut étudiant
                    user_type = '0'
                
                # Récupérer ou créer l'utilisateur avec le nom d'utilisateur
                user, created = User.objects.get_or_create(username=username, defaults={'first_name':first_name,'last_name':last_name})
                
                # Si l'utilisateur existe déjà, mettez à jour ses informations
                if not created:
                    user.first_name = first_name
                    user.last_name = last_name                 
                    user.set_password(default_password)
                    user.save()
                    send_password_reset_email(user,email) #reset utile?
                
                # Définir le mot de passe par défaut uniquement pour les nouveaux utilisateurs
                if created:
                    user.set_password(default_password)
                    user.save()
                    send_password_reset_email(user,email)
                    user, created = User.objects.get_or_create(username=username, defaults={'first_name':first_name,'last_name':last_name})

                # Créer ou mettre à jour le profil
                profil, profil_created = Profil.objects.update_or_create(
                user=user,
                defaults={'type': user_type}
                )
                
                # Assurez que le groupe par défaut existe et ajoutez l'utilisateur au groupe
                default_group, created = Group.objects.get_or_create(name='default')
                profil.group.add(default_group)

            messages.success(request, 'Users and profiles created or updated successfully')

    return render(request, 'login/users.html', {'data': data, 'error': error})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(get_user_model(), pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            username = request.POST.get('username')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'password_reset_form.html', {'uidb64': uidb64, 'token': token})

            if user.username != username:
                messages.error(request, "The username does not match the token.")
                return render(request, 'password_reset_form.html', {'uidb64': uidb64, 'token': token})

            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('login:log_in')
        else:
            return render(request, 'login/password_reset_form.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "The reset password link is no longer valid.")
        return redirect('login:log_in')

def password_reset_request(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            messages.warning(request, "You have been logged out to reset your password.")
        username = request.POST.get('username')
        user = get_user_model().objects.filter(username=username).first()
        if user:
            send_password_reset_email(user,username)
            messages.success(request, "A password reset link has been sent to your email address.")
        else:
            messages.error(request, "No user is associated with this email address.")
    return render(request, 'login/password_reset_sent.html')
