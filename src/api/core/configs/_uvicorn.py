import os
from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API

from ._base import BaseConfig


class UvicornConfig(BaseConfig):
    access_log: bool = Field(default=False)
    server_header: bool = Field(default=False)
    proxy_headers: bool = Field(default=True)
    forwarded_allow_ips: list[str] | str | None = Field(default=["*"])
    ssl_keyfile: str | None = Field(default=None)
    ssl_certfile: str | None = Field(default=None)
    reload: bool = Field(default=False)
    reload_dirs: list[str] | str | None = Field(default=None)
    reload_includes: list[str] | str | None = Field(
        default=["*.json", "*.yml", "*.yaml", "*.toml", "*.md"]
    )
    reload_excludes: list[str] | str | None = Field(
        default=[".*", "~*", ".py[cod]", ".sw.*", "__pycache__", "*.log", "logs"]
    )

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}UVICORN_")


class FrozenUvicornConfig(UvicornConfig):
    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "reload" in data:
                if data["reload"]:
                    if (not data.get("reload_dirs")) and os.path.isdir("./src"):
                        data["reload_dirs"] = ["./src"]
                else:
                    data["reload_includes"] = None
                    data["reload_excludes"] = None
                    data["reload_dirs"] = None

        return data

    model_config = SettingsConfigDict(frozen=True)


__all__ = [
    "UvicornConfig",
    "FrozenUvicornConfig",
]
