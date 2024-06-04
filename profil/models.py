from django.db import models
from django.contrib.auth import get_user_model

class Profil(models.Model):
    User = get_user_model()
    user = models.ForeignObject(User,on_delete=models.CASCADE)
    Type = models.CharField(max_length=1)
    group = models.ForeignObject(Group,on_delete=models.CASCADE)

    def __str__(self):
        return self.user
