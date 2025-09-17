from typing import Any

from pydantic import Field, constr, model_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API
from ._base import BaseConfig


class DevConfig(BaseConfig):
    reload: bool = Field(default=False)
    reload_includes: (
        list[constr(strip_whitespace=True, min_length=1, max_length=256)]  # type: ignore
    ) | None = Field(default=["*.json", "*.yml", "*.yaml", "*.toml", "*.md"])
    reload_excludes: (
        list[constr(strip_whitespace=True, min_length=1, max_length=256)] | None  # type: ignore
    ) = Field(default=[".*", "~*", ".py[cod]", ".sw.*", "__pycache__", "*.log", "logs"])

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}DEV_")


class FrozenDevConfig(DevConfig):
    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not values["reload"]:
            values["reload_includes"] = None
            values["reload_excludes"] = None

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = ["DevConfig", "FrozenDevConfig"]
