from django.shortcuts import render
from .models import Notes
from django.contrib.auth.decorators import login_required


@login_required
def list_notes_view(request,subject_name=None,):
    if request.user.profil.type == '2':  
        notes = Notes.objects.all().select_related('subject', 'student')  
    elif request.user.profil.type == '1':
        subjects=get_prof_subjects(request.user.id)
        notes = Notes.objects.filter(subjects=subjects).select_related('subject', 'student')
    elif request.user.profil.type == '0':
        subjects=get_student_subjects(request.user.id)     
        notes = Notes.objects.filter(subjects=subjects).select_related('subject')
    else :
        return render(request, 'notes/unauthorized.html')
    context = {
            'notes': notes,
        }
    return render(request, 'notes/list.html', context)

@login_required
def create_notes_view(request):
    if request.user.profil.type == '1':
        if request.method == 'POST':
            form = NotesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('list_notes')  # Assuming you have a URL named 'list_absences'
        else:
            form = NotesForm()
        context = {
            'form': form,
        }
    else:
        return render(request, 'notes/unauthorized.html')
    return render(request, 'notes/create.html', context)