from django.db import models
from profil.models import Profil
from group.models import Group

class UE(models.Model):
    name = models.CharField(max_length=50)
    semester = models.CharField(max_length=2)
    coef = models.CharField(max_length=3)

    def __str__(self):
        return self.name + '|' + str(self.semester) + '|'  + str(self.coef)

class Subject(models.Model):
    name = models.CharField(max_length=50)
    ue = models.ForeignKey(UE,on_delete=models.CASCADE)
    prof = models.ManyToManyField(to=Profil)
    student_group = models.ManyToManyField(to=Group)
    coef = models.CharField(max_length=3)

    def __str__(self):
        return self.name