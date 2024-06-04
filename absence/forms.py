from django import forms
from .models import Absence


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(choices=Absence.STATUS_CHOICES, attrs={'class': 'form-check'}),
        }
        labels = {
            'status': 'Statut',
        }
    
