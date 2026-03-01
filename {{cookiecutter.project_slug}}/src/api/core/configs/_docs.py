from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import SettingsConfigDict

from potato_util import validator

from api.core.constants import ENV_PREFIX_API

from ._base import BaseConfig


class DocsConfig(BaseConfig):
    enabled: bool = Field(default=True)
    openapi_url: str | None = Field(default="{api_prefix}/openapi.json")
    docs_url: str | None = Field(default="{api_prefix}/docs")
    redoc_url: str | None = Field(default="{api_prefix}/redoc")
    swagger_ui_oauth2_redirect_url: str | None = Field(
        default="{api_prefix}/docs/oauth2-redirect"
    )
    summary: str | None = Field(default="{{cookiecutter.project_description}}")
    description: str = Field(default="", max_length=8192)
    terms_of_service: str | None = Field(
        default="https://{{cookiecutter.domain}}/terms"
    )
    contact: dict[str, Any] | None = Field(
        default={
            "name": "Support Team",
            "email": "support@{{cookiecutter.domain}}",
            "url": "https://{{cookiecutter.domain}}/contact",
        }
    )
    license_info: dict[str, Any] | None = Field(
        default={
            "name": "{{cookiecutter.license}}",
            "url": "https://opensource.org/licenses/{{cookiecutter.license.split(' ')[0].lower()}}",
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
    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if ("openapi_url" in data) and (data["openapi_url"] == ""):
                data["openapi_url"] = None

            if ("docs_url" in data) and (data["docs_url"] == ""):
                data["docs_url"] = None

            if ("redoc_url" in data) and (data["redoc_url"] == ""):
                data["redoc_url"] = None

            if ("swagger_ui_oauth2_redirect_url" in data) and (
                data["swagger_ui_oauth2_redirect_url"] == ""
            ):
                data["swagger_ui_oauth2_redirect_url"] = None

            try:
                if ("enabled" in data) and validator.is_falsy(data["enabled"]):
                    data["openapi_url"] = None
                    data["docs_url"] = None
                    data["redoc_url"] = None
                    data["swagger_ui_oauth2_redirect_url"] = None
            except ValueError:
                pass

        return data

    model_config = SettingsConfigDict(frozen=True)


__all__ = ["DocsConfig", "FrozenDocsConfig"]
