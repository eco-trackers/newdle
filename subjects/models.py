from django.db import models
from profil.models import Profil

class UE(models.model):
    pass

class Subject(models.model):
    name = models.CharField(max_length=50)
    ue = models.ManyToManyField(to=UE,on_delete=models.CASCADE)
    prof = models.ManyToManyField(to=Profil,on_delete=models.CASCADE)
    student_group = models.ManyToManyField(to=Group,on_delete=models.CASCADE)
    coef = models.CharField(max_length=3)


    def __str__(self):
        return self.name + '|' + str(self.ue) + '|'  + str(self.prof) +'|' + str(self.student_group)
