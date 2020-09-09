from typing import Any, Type

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def handle_user_post_save(sender: Type[User], instance: User, **kwargs: Any) -> None:
    try:
        instance.profile
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
