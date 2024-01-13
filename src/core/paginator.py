from typing import Generic, List, TypeVar

from pydantic import BaseModel, conint
from pydantic.generics import GenericModel


class PageParams(BaseModel):
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10


T = TypeVar("T")


class PagedResponseSchema(GenericModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    # count: int
    results: List[T]


def paginate(
    page_params: PageParams,
    count,
    queryset,
) -> PagedResponseSchema[T]:
    """Paginate the query."""

    # paginated_query = query.offset((page_params.page - 1) * page_params.size).limit(page_params.size).all()

    return PagedResponseSchema(
        total=count,
        page=page_params.page,
        size=page_params.size,
        results=queryset,
    )