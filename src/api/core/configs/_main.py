import os

from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import SettingsConfigDict

from potato_util import is_debug_mode

from api.core.constants import EnvEnum, ENV_PREFIX

from ._base import FrozenBaseConfig
from ._uvicorn import UvicornConfig, FrozenUvicornConfig
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
        _uvicorn: UvicornConfig = val.uvicorn
        if info.data["env"] == EnvEnum.DEVELOPMENT:
            _uvicorn.reload = True

        if val.security.ssl.enabled:
            if not _uvicorn.ssl_keyfile:
                _uvicorn.ssl_keyfile = os.path.join(
                    val.paths.ssl_dir, val.security.ssl.key_fname
                )

            if not _uvicorn.ssl_certfile:
                _uvicorn.ssl_certfile = os.path.join(
                    val.paths.ssl_dir, val.security.ssl.cert_fname
                )

        _uvicorn = FrozenUvicornConfig(**_uvicorn.model_dump())
        val = FrozenApiConfig(uvicorn=_uvicorn, **val.model_dump(exclude={"uvicorn"}))
        return val

    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX, env_nested_delimiter="__")


__all__ = [
    "MainConfig",
]
