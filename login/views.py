from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
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

FROM_EMAIL = 'maxime.sanciaume@uha.fr'

def log_in(request):
    user_type = None
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                profil = Profil.objects.get(user=user)
                user_type = profil.type
                return redirect('/principal/')
    else:
        form = AuthenticationForm()
        if request.user.is_authenticated:
            try:
                profil = Profil.objects.get(user=request.user)
                user_type = profil.type
            except Profil.DoesNotExist:
                user_type = None
                
    context = {
        'form': form,
        'user_type': user_type
    }
    print(user_type)
    return render(request, 'login/connection.html', context)

def send_password_reset_email(user, email):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://127.0.0.1:8000/login/reset/{uid}/{token}/"
    subject = 'Password Reset'
    html_message = render_to_string('login/password_reset_email.html', {'username': user.username, 'reset_link': reset_link})
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
        action = request.POST.get("action")
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            error = 'Le fichier doit être un CSV.'
        else:
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)

            with open(fs.path(filename), newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    data.append({
                        "nom": row.get("NOM", "").strip().lower(),
                        "prenom": row.get("Prénom", "").strip().lower(),
                        "email": row.get("email", "").strip().lower(),
                        "password": row.get("password", "").strip(),
                        "role": row.get("role", "").strip().lower(),
                    })
            
            os.remove(filename)

            if action == "delete": #redirect(delete users)
                return render(request, 'login/users.html', {'data': data, 'error': error})
            else:
                User = get_user_model()
                for entry in data:
                    first_name = entry["prenom"]
                    last_name = entry["nom"]
                    email = entry["email"]
                    role = entry["role"]
                    default_password = entry["password"] or User.objects.make_random_password()
                    if first_name and last_name:
                        username = f"{first_name}.{last_name}@uha.fr"

                        if role == 'student':
                            user_type = '0'
                        elif role == 'professor':
                            user_type = '1'
                        elif role == 'admin':
                            user_type = '2'
                        else:
                            user_type = '0'
                        
                        user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name, 'last_name': last_name})
                        
                        if not created:
                            user.first_name = first_name
                            user.last_name = last_name                 
                            user.set_password(default_password)
                            user.save()
                            send_password_reset_email(user, email)
                        
                        if created:
                            user.set_password(default_password)
                            user.save()
                            send_password_reset_email(user, email)

                        profil, profil_created = Profil.objects.update_or_create(
                            user=user,
                            defaults={'type': user_type}
                        )
                        
                        default_group, created = Group.objects.get_or_create(name='Default Group')
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
            messages.warning(request, "Vous avez été déconnecté pour réinitialiser votre mot de passe.")

        username = request.POST.get('username').strip().lower()

        try:
            user = get_user_model().objects.get(username=username)
            profil = Profil.objects.get(user=user)
        except get_user_model().DoesNotExist:
            user = None
            profil = None
            
        except Profil.DoesNotExist:
            user = get_user_model().objects.get(username=username)
            profil = None

        if user is not None and profil is not None:
            send_password_reset_email(user, username)
            messages.success(request, "Un lien de réinitialisation de mot de passe a été envoyé à votre adresse e-mail.")
            return render(request, 'login/password_reset_sent.html')
        else:
            messages.error(request, "Aucun utilisateur n'est associé à ce nom d'utilisateur ou le type de profil est incorrect.")
            return render(request, 'login/connection.html')

    return render(request, 'login/password_reset_sent.html')


@login_required
def delete_users(request):
    if request.method == "POST":
        username_list = request.POST.getlist('user_usernames')
        User = get_user_model()
        for username in username_list:
            if username:  
                user = User.objects.filter(username=username).first()
                if user:
                    user.delete()
        messages.success(request, 'Selected users have been deleted successfully.')
    return redirect('login:tab_and_upload_csv_view')
