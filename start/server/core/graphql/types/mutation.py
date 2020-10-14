from typing import Iterable, List, NamedTuple, Optional

from ariadne import MutationType
from django.contrib.auth import login
from rest_framework.authtoken.models import Token

from core.forms import UserForm
from core.graphql import GraphQLResolveInfo
from core.models import Launch, User


class TripUpdateResponse(NamedTuple):
    success: bool
    message: Optional[str] = None
    launches: Optional[Iterable[Launch]] = None


mutation = MutationType()


@mutation.field("login")
def resolve_login(
    obj: None, info: GraphQLResolveInfo, email: Optional[str] = None
) -> Optional[Token]:
    request = info.context["request"]
    if not request.user.is_authenticated and email:
        try:
            user: Optional[User] = User.objects.get(email=email)
        except User.DoesNotExist:
            form = UserForm({"email": email})
            user = form.save() if form.is_valid() else None
        if user:
            login(request, user)
    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        return token
    return None


@mutation.field("book_trips")
def resolve_book_trips(
    obj: None, info: GraphQLResolveInfo, launch_pks: List[int]
) -> TripUpdateResponse:
    request = info.context["request"]
    launches = Launch.objects.filter(pk__in=launch_pks)
    if request.user.is_authenticated:
        request.user.profile.trips.add(*launches)
        booked_pks = list(launches.values_list("pk", flat=True))
    else:
        booked_pks = []
    success = len(booked_pks) == len(launch_pks)
    return TripUpdateResponse(
        success=success,
        message="trips booked successfully"
        if success
        else f"the following launches couldn't be booked: {set(launch_pks) - set(booked_pks)}",
        launches=launches,
    )


@mutation.field("cancel_trip")
def resolve_cancel_trip(obj: None, info: GraphQLResolveInfo, launch_pk: int) -> TripUpdateResponse:
    request = info.context["request"]
    if not request.user.is_authenticated:
        return TripUpdateResponse(success=False, message="failed to cancel trip")
    try:
        launch = Launch.objects.get(pk=launch_pk)
    except Launch.DoesNotExist:
        return TripUpdateResponse(success=False, message="failed to cancel trip")
    request.user.profile.trips.remove(launch)
    return TripUpdateResponse(success=True, message="trip cancelled", launches=[launch])
