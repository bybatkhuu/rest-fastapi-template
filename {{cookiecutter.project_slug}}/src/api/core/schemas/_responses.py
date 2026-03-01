from typing import Any

from pydantic import Field, constr

from potato_util.constants import HTTPMethodEnum

from api.config import config

from ._base import ExtraBasePM, BasePM


class LinksResPM(ExtraBasePM):
    self_link: constr(strip_whitespace=True, max_length=2048) | None = Field(  # type: ignore
        default=None,
        alias="self",
        title="Self link",
        description="Link to the current resource.",
        examples=[f"{config.api.prefix}/resources"],
    )


class PageLinksResPM(LinksResPM):
    first_link: constr(strip_whitespace=True, max_length=2048) | None = Field(  # type: ignore
        default=None,
        alias="first",
        title="First link",
        description="Link to the first page of the resource.",
        examples=[f"{config.api.prefix}/resources/?skip=0&limit=100"],
    )
    prev_link: constr(strip_whitespace=True, max_length=2048) | None = Field(  # type: ignore
        default=None,
        alias="prev",
        title="Previous link",
        description="Link to the previous page of the resource.",
        examples=[f"{config.api.prefix}/resources/?skip=100&limit=100"],
    )
    next_link: constr(strip_whitespace=True, max_length=2048) | None = Field(  # type: ignore
        default=None,
        alias="next",
        title="Next link",
        description="Link to the next page of the resource.",
        examples=[f"{config.api.prefix}/resources/?skip=300&limit=100"],
    )
    last_link: constr(strip_whitespace=True, max_length=2048) | None = Field(  # type: ignore
        default=None,
        alias="last",
        title="Last link",
        description="Link to the last page of the resource.",
        examples=[f"{config.api.prefix}/resources/?skip=400&limit=100"],
    )


class MetaResPM(ExtraBasePM):
    base_url: None | (
        constr(strip_whitespace=True, min_length=2, max_length=256)  # type: ignore
    ) = Field(
        default=None,
        title="Base URL",
        description="Current request base URL.",
        examples=["https://api.{{cookiecutter.domain}}"],
    )
    method: HTTPMethodEnum | None = Field(
        default=None,
        title="Method",
        description="Current request method.",
        examples=["GET"],
    )


class ErrorResPM(BasePM):
    code: constr(strip_whitespace=True) = Field(  # type: ignore
        ...,
        min_length=3,
        max_length=36,
        title="Error code",
        description="Code that represents the error.",
        examples=["400_00000"],
    )
    description: constr(strip_whitespace=True) | None = Field(  # type: ignore
        default=None,
        max_length=1024,
        title="Error description",
        description="Description of the error.",
        examples=["Bad request syntax or unsupported method."],
    )
    detail: Any | dict | list = Field(
        default=None,
        title="Error detail",
        description="Detail of the error.",
        examples=[
            {
                "loc": ["body", "field"],
                "msg": "Error message.",
                "type": "Error type.",
                "ctx": {"constraint": "value"},
            }
        ],
    )


class BaseResPM(BasePM):
    message: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Message",
        description="Response message about the current request.",
        examples=["Successfully processed the request."],
    )
    data: Any | dict | list = Field(
        default=None,
        title="Data",
        description="Resource data or any data related to response.",
        examples=["Any data: dict, list, str, int, float, null, etc."],
    )
    links: LinksResPM = Field(
        default_factory=LinksResPM,
        title="Links",
        description="Links related to the current request or resource.",
    )
    meta: MetaResPM = Field(
        default_factory=MetaResPM,
        title="Meta",
        description="Meta information about the current request.",
    )
    error: ErrorResPM | Any = Field(
        default=None,
        title="Error",
        description="Error information about the current request.",
        examples=[None],
    )


__all__ = [
    "LinksResPM",
    "PageLinksResPM",
    "MetaResPM",
    "ErrorResPM",
    "BaseResPM",
]
