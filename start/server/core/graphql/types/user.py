from ariadne import ObjectType
from django.db.models import QuerySet

from core.graphql import GraphQLResolveInfo
from core.models import Launch, User

user = ObjectType("User")


@user.field("trips")
def resolve_user_trips(obj: User, info: GraphQLResolveInfo) -> QuerySet[Launch]:
    return obj.profile.trips.all()
