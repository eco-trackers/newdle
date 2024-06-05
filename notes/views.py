from django.shortcuts import render
from .models import Notes
@login_required

def list_notes_view(request):
    Notes = notes.objects.all().select_related('subject')  # Assuming Absence model has a ForeignKey to Subject model
    context = {
        'notes': notes,
    }
    return render(request, 'notes/list.html', context)


def create_notes_view(request):
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
    return render(request, 'notes/create.html', context)