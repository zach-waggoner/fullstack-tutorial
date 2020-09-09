import os
from typing import Iterable, List, Literal, NamedTuple, Optional

from ariadne import (
    MutationType,
    ObjectType,
    QueryType,
    fallback_resolvers,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.contrib.django.scalars import date_scalar, datetime_scalar
from django.conf import settings
from django.contrib.auth import login
from django.db.models import QuerySet
from rest_framework.authtoken.models import Token

from .forms import UserForm
from .graphql import GraphQLResolveInfo
from .models import Launch, Mission, User
from .pagination import CursorPagination, PaginatedResponse

PatchSize = Literal["SMALL", "LARGE"]

query = QueryType()

mutation = MutationType()

launch = ObjectType("Launch")

rocket = ObjectType("Rocket")
rocket.set_alias("type", "rocket_type")

user = ObjectType("User")

mission = ObjectType("Mission")


class TripUpdateResponse(NamedTuple):
    success: bool
    message: Optional[str] = None
    launches: Optional[Iterable[Launch]] = None


@query.field("launches")
def resolve_launches(
    obj: None,
    info: GraphQLResolveInfo,
    page_size: int = 20,
    cursor: Optional[str] = None,
) -> PaginatedResponse[Launch]:
    request = info.context["request"]
    queryset = Launch.objects.all()
    pagination = CursorPagination[Launch]()
    return pagination.paginate_queryset(request, queryset, page_size, cursor)


@query.field("launch")
def resolve_launch(obj: None, info: GraphQLResolveInfo, pk: int) -> Launch:
    return Launch.objects.get(pk=pk)


@query.field("me")
def resolve_me(obj: None, info: GraphQLResolveInfo) -> Optional[User]:
    request = info.context["request"]
    return request.user if request.user.is_authenticated else None


@launch.field("is_booked")
def resolve_launch_is_booked(obj: Launch, info: GraphQLResolveInfo) -> bool:
    request = info.context["request"]
    return request.user.is_authenticated and request.user.profile.trips.filter(pk=obj.pk).exists()


@user.field("trips")
def resolve_user_trips(obj: User, info: GraphQLResolveInfo) -> QuerySet[Launch]:
    return obj.profile.trips.all()


@mission.field("mission_patch")
def resolve_mission_mission_patch(
    obj: Mission, info: GraphQLResolveInfo, size: PatchSize = "LARGE"
) -> Optional[str]:
    mission_patch: Optional[str] = obj.links[
        "mission_patch_small" if size == "SMALL" else "mission_patch"
    ]
    return mission_patch


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


type_defs = load_schema_from_path(os.path.join(settings.BASE_DIR, "core/schema.graphql"))
schema = make_executable_schema(
    type_defs, query, mutation, date_scalar, datetime_scalar, fallback_resolvers
)
