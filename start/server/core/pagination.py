from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from urllib.parse import parse_qs, urlparse

from django.db.models import Model, QuerySet
from rest_framework.pagination import CursorPagination as DrfCursorPagination

from .request import Request

T = TypeVar("T", bound=Model)


# TODO: https://github.com/python/mypy/issues/685
@dataclass(frozen=True)
class PaginatedResponse(Generic[T]):
    results: List[T]
    cursor: Optional[str]
    has_more: bool


class CursorPagination(Generic[T]):
    def __init__(self) -> None:
        self.drf_pagination = DrfCursorPagination()
        self.drf_pagination.ordering = "pk"

    def paginate_queryset(
        self,
        request: Request,
        queryset: QuerySet[T],
        page_size: int,
        cursor: Optional[str] = None,
    ) -> PaginatedResponse[T]:
        self.drf_pagination.page_size = page_size
        if cursor:
            request.GET = request.GET.copy()
            request.GET["cursor"] = cursor
        return PaginatedResponse(
            results=self.drf_pagination.paginate_queryset(queryset, request),
            cursor=self._get_cursor(),
            has_more=bool(self.drf_pagination.has_next),
        )

    def _get_cursor(self) -> Optional[str]:
        next_link = self.drf_pagination.get_next_link()
        return next_link and parse_qs(urlparse(next_link).query)["cursor"][0]
