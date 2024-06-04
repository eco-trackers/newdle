from django.db import models
from django.contrib.auth import get_user_model
from group.models import Group

class Profil(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=1)
    group = models.ManyToManyField(Group,on_delete=models.CASCADE)

    def __str__(self):
        return self.user
