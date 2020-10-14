from ariadne import ObjectType

from core.graphql import GraphQLResolveInfo
from core.models import Launch

launch = ObjectType("Launch")


@launch.field("is_booked")
def resolve_launch_is_booked(obj: Launch, info: GraphQLResolveInfo) -> bool:
    request = info.context["request"]
    return request.user.is_authenticated and request.user.profile.trips.filter(pk=obj.pk).exists()
