from typing import TypedDict

from graphql import GraphQLResolveInfo as BaseGraphQLResolveInfo

from .http import HttpRequest


class GraphQLResolveInfoContext(TypedDict):
    request: HttpRequest


class GraphQLResolveInfo(BaseGraphQLResolveInfo):
    context: GraphQLResolveInfoContext
