import os
from typing import Literal, Optional

from ariadne import (
    ObjectType,
    QueryType,
    fallback_resolvers,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.contrib.django.scalars import date_scalar, datetime_scalar
from django.conf import settings
from django.db.models import QuerySet

from .graphql import GraphQLResolveInfo
from .models import Launch, Mission, User

PatchSize = Literal["SMALL", "LARGE"]

query = QueryType()

launch = ObjectType("Launch")

rocket = ObjectType("Rocket")
rocket.set_alias("type", "rocket_type")

user = ObjectType("User")

mission = ObjectType("Mission")


@query.field("launches")
def resolve_launches(obj: None, info: GraphQLResolveInfo) -> QuerySet[Launch]:
    return Launch.objects.all()


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


type_defs = load_schema_from_path(os.path.join(settings.BASE_DIR, "core/schema.graphql"))
schema = make_executable_schema(type_defs, query, date_scalar, datetime_scalar, fallback_resolvers)
