from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ClassPhoto

@receiver(post_delete, sender=ClassPhoto)
def delete_classphoto_file(sender, instance, **kwargs):
    if instance.photo and hasattr(instance.photo, 'path'):
        instance.photo.delete(save=False)