from django import forms
from .models import Note

class NoteCreateForm(forms.ModelForm):
    class Meta:
        model=Note
        fields = [ 'subject', 'profil','valeur']
        labels = {
            'valeur': 'Note',
            'subject': 'Matière',
            'profil': 'Élève',
        }