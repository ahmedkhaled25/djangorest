from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def user_create_handler(sender, instance, created, **prams):
    if created:
        Token.objects.create(user=instance)
