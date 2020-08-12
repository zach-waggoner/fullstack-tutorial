from typing import Union

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest as BaseHttpRequest

from .models import User


class HttpRequest(BaseHttpRequest):
    user: Union[User, AnonymousUser]
