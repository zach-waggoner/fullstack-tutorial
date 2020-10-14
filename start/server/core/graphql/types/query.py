from typing import Optional

from ariadne import QueryType

from core.graphql import GraphQLResolveInfo
from core.models import Launch, User
from core.pagination import CursorPagination, PaginatedResponse

query = QueryType()


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
