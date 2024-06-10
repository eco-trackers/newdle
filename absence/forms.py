from django import forms

from profil.models import Profil
from .models import Absence

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(attrs={'class': 'form-check'}),
        }
        labels = {
            'status': 'Statut',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = Absence.STATUS_CHOICES
        self.fields['status'].initial = '1'  
        
class AbsenceFormT(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date','student','status']
        widgets = {
            'date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}),
            'status': forms.RadioSelect(attrs={'class': 'form-check-input',  'type':'checkbox'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date de l\'absence',
            'status': 'Statut',
            'student': 'Etudiant',
        }
    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = Absence.STATUS_CHOICES
        self.fields['status'].initial = '1'  
        if subject:
            # Récupérer les instances du groupe associé au sujet
            student_groups = subject.student_group.all()
            # Filtrer les profils par ces instances de groupe
            self.fields['student'].queryset = Profil.objects.filter(group__in=student_groups)
        
            
            
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date']
        widgets = {
            'date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}),
        }
        labels = {
            'date': 'Date et heure de l\'appel',
        }
    
    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        if subject:
            student_groups = subject.student_group.all()
            students = Profil.objects.filter(group__in=student_groups)
            for student in students:
                # Ajouter un champ de choix pour chaque étudiant avec le statut d'absence comme choix
                self.fields[f'student_{student.id}'] = forms.ChoiceField(
                    choices=Absence.STATUS_CHOICES,
                    label=student.user.username,
                    widget=forms.RadioSelect,
                    required=False
                )


class EditAbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date','status']
        widgets = {
            'date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}),
            'status': forms.RadioSelect(choices=Absence.STATUS_CHOICES),
        }
        labels = {
            'date': 'Date de l\'absence',
            'status': 'Statut',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = Absence.STATUS_CHOICES
        self.fields['status'].initial = '1'  



