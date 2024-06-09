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


class ClassPhoto(models.Model):
    photo = models.ImageField(upload_to='static/class_photos/')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Photo pour {self.subject.name} le {self.upload_date}"
    
class Pin(models.Model):
    photo = models.ForeignKey(ClassPhoto, on_delete=models.CASCADE)
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pin by {self.user} on {self.photo}"
