from django.shortcuts import render, redirect
from .models import Group
from django.contrib.auth.decorators import login_required

@login_required
def show(request):
    groups = Group.objects.all()
    return render(request, 'group/show.html', {'groups': groups})

@login_required
def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        # Create a new group object
        group = Group(name=name)
        group.save()
        
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
    
    group = Group.objects.get(id=id)
    return render(request, 'group/edit.html', {'group': group})

@login_required
def delete(request, id):
    group = Group.objects.get(id=id)
    group.delete()
    
    return redirect('group:show')