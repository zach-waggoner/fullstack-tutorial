from typing import Union

from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request as BaseRequest

from .models import User


class Request(BaseRequest):
    user: Union[User, AnonymousUser]
