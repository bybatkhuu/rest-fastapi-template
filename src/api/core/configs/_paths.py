import os
from typing import Any

from pydantic import Field, model_validator, field_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API
from ._base import BaseConfig


class PathsConfig(BaseConfig):
    tmp_dir: str = Field(default="../tmp", min_length=2, max_length=1024)
    uploads_dir: str = Field(default="{tmp_dir}/uploads", min_length=2, max_length=1024)
    data_dir: str = Field(default="../data", min_length=2, max_length=1024)
    security_dir: str = Field(
        default="{data_dir}/security", min_length=2, max_length=1024
    )
    ssl_dir: str = Field(
        default="{data_dir}/security/ssl", min_length=2, max_length=1024
    )
    asymmetric_keys_dir: str = Field(
        default="{data_dir}/security/asymmetric_keys", min_length=2, max_length=1024
    )
    # models_dir: str = Field(default="{data_dir}/models", min_length=2, max_length=1024)
    # model_dir: str = Field(
    #     default="{data_dir}/models/{{model_id}}", min_length=2, max_length=1024
    # )

    @field_validator("data_dir")
    @classmethod
    def _check_data_dir(cls, val: str) -> str:
        _data_dir_env = f"{ENV_PREFIX_API}DATA_DIR"
        if _data_dir_env in os.environ:
            val = os.getenv(_data_dir_env)

        return val

    @field_validator("tmp_dir")
    @classmethod
    def _check_tmp_dir(cls, val: str) -> str:
        _tmp_dir_env = f"{ENV_PREFIX_API}TMP_DIR"
        if _tmp_dir_env in os.environ:
            val = os.getenv(_tmp_dir_env)

        return val

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}PATHS_")


class FrozenPathsConfig(PathsConfig):
    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: dict[str, Any]) -> dict[str, Any]:
        for _key, _val in values.items():
            if isinstance(_val, str) and ("{data_dir}" in _val):
                values[_key] = _val.format(data_dir=values["data_dir"])

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = ["PathsConfig", "FrozenPathsConfig"]
