from datetime import datetime
from django import forms

from subjects.models import Subject
from .models import Absence

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date','status', 'subject']
        widgets = {
            'status': forms.Select(choices=Absence.STATUS_CHOICES),
            'subject': forms.Select(),
            'date': forms.HiddenInput(),
        }
        labels = {
            'status': 'Statut',
            'subject': 'Matière',
        }
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Sélectionner une matière")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.now()
        self.fields['date'].widget.attrs['readonly'] = True
        
