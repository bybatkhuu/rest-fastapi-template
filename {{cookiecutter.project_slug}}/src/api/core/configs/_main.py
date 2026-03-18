import os

from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import SettingsConfigDict

from potato_util.constants import EnvEnum

from api.core.constants import ENV_PREFIX

from ._base import BaseMainConfig
from ._uvicorn import UvicornConfig, FrozenUvicornConfig
from ._api import ApiConfig, FrozenApiConfig


# Main config schema:
class MainConfig(BaseMainConfig):
    env: EnvEnum = Field(default=EnvEnum.LOCAL, alias="env")
    debug: bool = Field(default=False, alias="debug")
    api: ApiConfig = Field(default_factory=ApiConfig)

    @field_validator("api", mode="after")
    @classmethod
    def _check_api(cls, val: ApiConfig, info: ValidationInfo) -> FrozenApiConfig:
        _uvicorn: UvicornConfig = val.uvicorn
        if ("env" in info.data) and (info.data["env"] == EnvEnum.DEVELOPMENT):
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

    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX,
        env_nested_delimiter="__",
        cli_prefix="",
        secrets_dir="/run/secrets",
        secrets_prefix="",
        secrets_nested_delimiter="_",
        secrets_dir_missing="ok",  # pragma: allowlist secret
    )  # type: ignore


__all__ = [
    "MainConfig",
]
