from django.db import models
from datetime import datetime
from profil.models import Profil
from subjects.models import Subject
# Create your models here.
class Absence(models.Model) :
    STATUS_CHOICES = [
        ('0', 'Absent(e)'),
        ('1', 'Présent(e)'),
        ('2', 'En retard'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES) # 0->Absent 1->Present 2->Retard
    student = models.ForeignKey(Profil, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    
    def get_status_display_custom(self):
        for choice in self.STATUS_CHOICES:
            if choice[0] == self.status:
                return choice[1]
        return None
    
    def __str__(self):
        status_display = self.get_status_display_custom()
        return status_display + '|' + str(self.subject)+'|'+str(self.student)
