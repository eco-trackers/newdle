from django.db import models
from subjects.models import Subject
from profil.models import Profil

class Note(models.Model):
    valeur=models.DecimalField(decimal_places=3,max_digits=1000)
    subject=models.CharField(max_length=20)
    profil=models.CharField(max_length=20)
    def __str__(self):
        return self.valeur + '|' + str(self.subject)+'|'+str(self.profil)