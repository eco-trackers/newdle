from django.db import models
from subjects.models import Subject
from profil.models import Profil
class Note(models.model):
    valeur=models.FloatField()
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    profil=models.ForeignKey(Profil,on_delete=models.CASCADE)

# Create your models here.
