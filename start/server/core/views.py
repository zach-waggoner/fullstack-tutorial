from typing import Any, Dict, List, Optional, Sequence, Type

from ariadne.contrib.django.views import GraphQLView as BaseGraphQLView
from ariadne.types import ContextValue
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from rest_framework.authentication import BaseAuthentication
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import BaseParser
from rest_framework.settings import api_settings

from .request import Request


class AppView(TemplateView):
    template_name = "core/app.html"


class GraphQLView(BaseGraphQLView):
    parser_classes: Sequence[Type[BaseParser]] = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes: Sequence[
        Type[BaseAuthentication]
    ] = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    content_negotiation_class: Type[
        BaseContentNegotiation
    ] = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.args = args
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def initialize_request(self, http_request: HttpRequest) -> Request:
        return Request(
            http_request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=self.get_parser_context(),
        )

    def get_parsers(self) -> List[BaseParser]:
        return [parser() for parser in self.parser_classes]

    def get_authenticators(self) -> List[BaseAuthentication]:
        return [auth() for auth in self.authentication_classes]

    def get_content_negotiator(self) -> BaseContentNegotiation:
        if not getattr(self, "_negotiator", None):
            self._negotiator = self.content_negotiation_class()
        return self._negotiator

    def get_parser_context(self) -> Dict[str, Any]:
        return {
            "view": self,
            "args": getattr(self, "args", ()),
            "kwargs": getattr(self, "kwargs", {}),
        }

    def get_context_for_request(self, request: HttpRequest) -> Optional[ContextValue]:
        if callable(self.context_value):
            return self.context_value(request)
        return self.context_value or {"request": Request(request)}
