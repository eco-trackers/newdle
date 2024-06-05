from django.db import models
from subjects.models import Subject
from profil.models import Profil

class Note(models.Model):
    valeur=models.FloatField()
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    profil=models.ForeignKey(Profil,on_delete=models.CASCADE)
    def __str__(self):
        return self.valeur + '|' + str(self.subject)+'|'+str(self.profil)

# Create your models here.
