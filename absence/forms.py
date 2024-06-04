from django import forms
from .models import Absence


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Absence.STATUS_CHOICES),
        }
        labels = {
            'status': 'Statut',
        }
    
