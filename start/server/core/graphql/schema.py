from ariadne import fallback_resolvers, load_schema_from_path, make_executable_schema
from django.conf import settings

from .scalars import scalars
from .types import types

type_defs = load_schema_from_path(settings.BASE_DIR / "core/graphql/schema.graphql")
schema = make_executable_schema(type_defs, *types, *scalars, fallback_resolvers)
