from datetime import datetime
from django import forms

from subjects.models import Subject
from .models import Absence

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date','status']
        widgets = {
            'status': forms.Select(choices=Absence.STATUS_CHOICES),
            'date': forms.HiddenInput(),
        }
        labels = {
            'status': 'Statut',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.now()
        self.fields['date'].widget.attrs['readonly'] = True
        
