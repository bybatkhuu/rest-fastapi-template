import os
import pathlib
from typing import Any, Dict, List, Optional

from pydantic import Field, constr, model_validator, field_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API
from api.core.utils import validator
from ._base import BaseConfig


class DocsConfig(BaseConfig):
    enabled: bool = Field(...)
    openapi_url: None | (
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ) = Field(default=None)
    docs_url: None | (constr(strip_whitespace=True, max_length=128)) = (  # type: ignore
        Field(default=None)
    )
    redoc_url: None | (
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ) = Field(default=None)
    swagger_ui_oauth2_redirect_url: None | (
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ) = Field(default=None)
    summary: None | (
        constr(strip_whitespace=True, min_length=2, max_length=128)  # type: ignore
    ) = Field(default=None)
    description: str = Field(default="", max_length=8192)
    terms_of_service: None | (
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ) = Field(default=None)
    contact: dict[str, Any] | None = Field(default=None)
    license_info: dict[str, Any] | None = Field(default=None)
    openapi_tags: list[dict[str, Any]] | None = Field(default=None)
    swagger_ui_parameters: dict[str, Any] | None = Field(default=None)

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
