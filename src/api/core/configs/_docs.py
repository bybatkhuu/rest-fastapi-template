import os
import pathlib
from typing import Any

from pydantic import Field, model_validator, field_validator
from pydantic_settings import SettingsConfigDict

from potato_util import validator

from api.core.constants import ENV_PREFIX_API

from ._base import BaseConfig


class DocsConfig(BaseConfig):
    enabled: bool = Field(default=False)
    openapi_url: str | None = Field(default="{api_prefix}/openapi.json")
    docs_url: str | None = Field(default="{api_prefix}/docs")
    redoc_url: str | None = Field(default="{api_prefix}/redoc")
    swagger_ui_oauth2_redirect_url: str | None = Field(
        default="{api_prefix}/docs/oauth2-redirect"
    )
    summary: str | None = Field(default="This is a REST API service.")
    description: str = Field(default="", max_length=8192)
    terms_of_service: str | None = Field(default="https://example.com/terms")
    contact: dict[str, Any] | None = Field(
        default={
            "name": "Support Team",
            "email": "support@example.com",
            "url": "https://example.com/contact",
        }
    )
    license_info: dict[str, Any] | None = Field(
        default={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        }
    )
    openapi_tags: list[dict[str, Any]] | None = Field(
        default=[
            {"name": "Utils", "description": "Useful utility endpoints."},
            {"name": "Tasks", "description": "Endpoints to manage tasks."},
            {"name": "Default", "description": "Redirection of default endpoints."},
        ]
    )
    swagger_ui_parameters: dict[str, Any] | None = Field(
        default={"syntaxHighlight": {"theme": "nord"}}
    )

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}DOCS_")


class FrozenDocsConfig(DocsConfig):
    @field_validator("description", mode="after")
    @classmethod
    def _check_description(cls, val: str) -> str:
        _src_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
        _description_path = str(
            _src_dir / "./api/configs/docs/description.md"
        )  # TODO: make it more flexible or remove it
        if (not val) and os.path.isfile(_description_path):
            with open(_description_path) as _file:
                val = _file.read()

        return val

    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: dict[str, Any]) -> dict[str, Any]:

        if values["openapi_url"] == "":
            values["openapi_url"] = None

        if values["docs_url"] == "":
            values["docs_url"] = None

        if values["redoc_url"] == "":
            values["redoc_url"] = None

        if values["swagger_ui_oauth2_redirect_url"] == "":
            values["swagger_ui_oauth2_redirect_url"] = None

        if validator.is_falsy(values["enabled"]):
            values["openapi_url"] = None
            values["docs_url"] = None
            values["redoc_url"] = None
            values["swagger_ui_oauth2_redirect_url"] = None

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = ["DocsConfig", "FrozenDocsConfig"]
