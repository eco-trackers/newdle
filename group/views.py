from django.shortcuts import render, redirect
from .models import Group
from profil.models import Profil
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def show(request,id=None):
    g = []
    match int(Profil.objects.get(user=request.user).type):
        case 0:
            g = Profil.objects.get(user=request.user).group.all()
        case 1:
            g = Profil.objects.get(user=request.user).group.all()
        case 2:
            g = Group.objects.all()

    users = []
    if id:
        group = Group.objects.get(id=id)
        users = group.profil_set.all()
    data = {
        'groups': g,
        'level': int(Profil.objects.get(user=request.user).type),
        'id_selected': id!=None,
        'users_length': len(users),
        'users': users
    }
    return render(request, 'group/show.html', data)

@login_required
def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        # Create a new group object
        group = Group(name=name)
        group.save()

        # Add the user to the group
        Profil.objects.get(user=request.user).group.add(group)
        
        return redirect('group:show')
    
    if int(Profil.objects.get(user=request.user).type) < 1:
        return redirect('group:show')
    
    return render(request, 'group/create.html')

@login_required
def edit(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        # Change the group object
        group = Group.objects.get(id=id)
        group.name = name
        group.save()
        
        return redirect('group:show')
    
    #test if the user is allowed to edit the group
    if int(Profil.objects.get(user=request.user).type) < 1:
        return redirect('group:show')
    
    if int(Profil.objects.get(user=request.user).type) == 1:
        if not Group.objects.get(id=id) in Profil.objects.get(user=request.user).group.all():
            return redirect('group:show')

    # generate dict for the template
    users = []
    for user in User.objects.all():
        users.append({
            'user': user,
            'in': Group.objects.get(id=id) in Profil.objects.get(user=user).group.all()
        })


    group = Group.objects.get(id=id)
    return render(request, 'group/edit.html', {'group': group,"users":users})

@login_required
def delete(request, id):
    if int(Profil.objects.get(user=request.user).type) < 1:
        return redirect('group:show')
    
    if int(Profil.objects.get(user=request.user).type) == 1:
        if not Group.objects.get(id=id) in Profil.objects.get(user=request.user).group.all():
            return redirect('group:show')
    
    group = Group.objects.get(id=id)
    group.delete()
    
    return redirect('group:show')