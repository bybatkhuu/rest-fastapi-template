import os
import pathlib
from typing import Any

from pydantic import Field, constr, model_validator, field_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API
from api.core.utils import validator
from ._base import BaseConfig


class DocsConfig(BaseConfig):
    enabled: bool = Field(default=True)
    openapi_url: constr(strip_whitespace=True, max_length=128) | None = Field(  # type: ignore
        default="{api_prefix}/openapi.json"
    )
    docs_url: (constr(strip_whitespace=True, max_length=128)) | None = (  # type: ignore
        Field(default="{api_prefix}/docs")
    )
    redoc_url: constr(strip_whitespace=True, max_length=128) | None = Field(  # type: ignore
        default="{api_prefix}/redoc"
    )
    swagger_ui_oauth2_redirect_url: (
        constr(strip_whitespace=True, max_length=128) | None  # type: ignore
    ) = Field(default="{api_prefix}/docs/oauth2-redirect")
    summary: constr(strip_whitespace=True, min_length=2, max_length=128) | None = Field(  # type: ignore
        default="This is a REST API service."
    )
    description: str = Field(default="", max_length=8192)
    terms_of_service: (
        constr(strip_whitespace=True, min_length=1, max_length=256) | None  # type: ignore
    ) = Field(default="https://example.com/terms")
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
    @field_validator("description")
    @classmethod
    def _check_description(cls, val: str) -> str:
        _src_dir = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
        _description_path = str(_src_dir / "./api/configs/docs/description.md")
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
