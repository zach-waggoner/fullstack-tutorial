import uuid
from typing import Iterable, Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    # TODO: PEP 612
    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        if not self.username:
            self.username = uuid.uuid4().hex
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class Mission(models.Model):
    name = models.CharField(max_length=255)
    links = models.JSONField()  # type: ignore

    def __str__(self) -> str:
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Rocket(models.Model):
    name = models.CharField(max_length=255)
    rocket_type = models.CharField(max_length=255, db_column="type")

    def __str__(self) -> str:
        return self.name


class Launch(models.Model):
    site = models.ForeignKey(Site, null=True, on_delete=models.SET_NULL)
    mission = models.ForeignKey(Mission, null=True, on_delete=models.CASCADE)
    rocket = models.ForeignKey(Rocket, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.site} : {self.mission} : {self.rocket}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trips = models.ManyToManyField(Launch)

    def __str__(self) -> str:
        return str(self.user)
