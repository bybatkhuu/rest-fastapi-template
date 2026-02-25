from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API

from ._base import BaseConfig


class ServerConfig(BaseConfig):
    access_log: bool = Field(default=False)
    server_header: bool = Field(default=False)
    proxy_headers: bool = Field(default=True)
    forwarded_allow_ips: list[str] | str | None = Field(default=["*"])
    ssl_keyfile: str | None = Field(default=None)
    ssl_certfile: str | None = Field(default=None)
    reload: bool = Field(default=False)
    reload_includes: list[str] | None = Field(
        default=["*.json", "*.yml", "*.yaml", "*.toml", "*.md"]
    )
    reload_excludes: list[str] | None = Field(
        default=[".*", "~*", ".py[cod]", ".sw.*", "__pycache__", "*.log", "logs"]
    )

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}UVICORN_")


class FrozenServerConfig(ServerConfig):
    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not values["reload"]:
            values["reload_includes"] = None
            values["reload_excludes"] = None

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = [
    "ServerConfig",
    "FrozenServerConfig",
]
