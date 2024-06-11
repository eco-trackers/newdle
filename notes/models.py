from django.db import models
from subjects.models import Subject
from profil.models import Profil

class Note(models.Model):
    valeur=models.DecimalField(decimal_places=3,max_digits=1000)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    profil=models.ForeignKey(Profil,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.valeur) + '|' + str(self.subject)+'|'+str(self.profil)

# Create your models here.
