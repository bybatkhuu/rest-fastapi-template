import os

from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import SettingsConfigDict

from potato_util import is_debug_mode

from api.core.constants import EnvEnum, ENV_PREFIX

from ._base import FrozenBaseConfig
from ._dev import DevConfig, FrozenDevConfig
from ._api import ApiConfig, FrozenApiConfig


# Main config schema:
class MainConfig(FrozenBaseConfig):
    env: EnvEnum = Field(default=EnvEnum.LOCAL)
    debug: bool = Field(default=False)
    api: ApiConfig = Field(default_factory=ApiConfig)

    @field_validator("env", mode="after")
    @classmethod
    def _check_env(cls, val: EnvEnum) -> EnvEnum:
        _env = os.getenv("ENV", "").upper()
        if _env:
            val = EnvEnum(_env)

        return val

    @field_validator("debug", mode="after")
    @classmethod
    def _check_debug(cls, val: bool) -> bool:
        if is_debug_mode():
            val = True

        return val

    @field_validator("api", mode="after")
    @classmethod
    def _check_api(cls, val: ApiConfig, info: ValidationInfo) -> FrozenApiConfig:
        _dev: DevConfig = val.dev
        if info.data["env"] == EnvEnum.DEVELOPMENT:
            _dev.reload = True

        _dev = FrozenDevConfig(**_dev.model_dump())
        val = FrozenApiConfig(dev=_dev, **val.model_dump(exclude={"dev"}))
        return val

    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX, env_nested_delimiter="__")


__all__ = [
    "MainConfig",
]
