from typing import TypedDict

from graphql import GraphQLResolveInfo as BaseGraphQLResolveInfo

from core.request import Request


class GraphQLResolveInfoContext(TypedDict):
    request: Request


class GraphQLResolveInfo(BaseGraphQLResolveInfo):
    context: GraphQLResolveInfoContext
