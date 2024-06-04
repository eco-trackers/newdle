from django.db import models
from datetime import datetime
from profil.models import Profil
from subjects.models import Subjects
# Create your models here.
class Absence :
    status = models.CharField(max_length=1) # 0->Absent 1-> 
    student = models.ForeignKey(Profil, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.status
