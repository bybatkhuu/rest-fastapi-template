import sys
from typing import Any

from pydantic import Field, field_validator, ValidationInfo, model_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API, HTTPSchemeEnum, API_SLUG

from ._base import BaseConfig, FrozenBaseConfig
from ._uvicorn import UvicornConfig
from ._security import SecurityConfig
from ._docs import DocsConfig, FrozenDocsConfig
from ._paths import PathsConfig, FrozenPathsConfig
from ._logger import LoggerConfigPM, FrozenLoggerConfigPM


is_running_server_cli = False
if (
    sys.argv[0].endswith("uvicorn")
    or sys.argv[0].endswith("fastapi")
    or sys.argv[0].endswith("gunicorn")
):
    is_running_server_cli = True


class GZipConfig(FrozenBaseConfig):
    min_size: int = Field(default=1024, ge=0, le=10_485_760)
    compresslevel: int = Field(default=9, ge=1, le=9)

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}GZIP_")


class ApiConfig(BaseConfig):
    title: str = Field(default="FastAPI Template", min_length=2, max_length=128)
    slug: str = Field(default=API_SLUG, min_length=2, max_length=128)
    http_scheme: HTTPSchemeEnum = Field(default=HTTPSchemeEnum.http)
    bind_host: str = Field(
        default="0.0.0.0", min_length=2, max_length=128  # nosec B104
    )
    port: int = Field(default=8000, ge=80, lt=65536)
    version: str = Field(default="1", min_length=1, max_length=16)
    prefix: str = Field(default="/api/v{api_version}", max_length=128)
    gzip: GZipConfig = Field(default_factory=GZipConfig)
    uvicorn: UvicornConfig = Field(default_factory=UvicornConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    docs: DocsConfig = Field(default_factory=DocsConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    logger: LoggerConfigPM = Field(default_factory=LoggerConfigPM)

    @field_validator("prefix", mode="after")
    @classmethod
    def _check_prefix(cls, val: str, info: ValidationInfo) -> str:
        if val and ("{api_version}" in val):
            val = val.format(api_version=info.data["version"])

        return val

    @field_validator("security", mode="after")
    @classmethod
    def _check_security(
        cls, val: SecurityConfig, info: ValidationInfo
    ) -> SecurityConfig:

        if (not is_running_server_cli) and val.ssl.enabled:
            info.data["http_scheme"] = HTTPSchemeEnum.https

        return val

    @field_validator("docs", mode="after")
    @classmethod
    def _check_docs(cls, val: DocsConfig, info: ValidationInfo) -> DocsConfig:
        _docs_dict = val.model_dump()
        if val.enabled:
            for _key, _doc in _docs_dict.items():
                if (
                    isinstance(_doc, str)
                    and _key.endswith("url")
                    and ("{api_prefix}" in _doc)
                ):
                    _docs_dict[_key] = _doc.format(api_prefix=info.data["prefix"])

        val = FrozenDocsConfig(**_docs_dict)
        return val

    @field_validator("paths", mode="after")
    @classmethod
    def _check_paths(cls, val: PathsConfig, info: ValidationInfo) -> FrozenPathsConfig:
        _paths_dict = val.model_dump()
        for _key, _path in _paths_dict.items():
            if isinstance(_path, str) and ("{api_slug}" in _path):
                _paths_dict[_key] = _path.format(api_slug=info.data["slug"])

        val = FrozenPathsConfig(**_paths_dict)
        return val

    @field_validator("logger", mode="after")
    @classmethod
    def _check_logger(cls, val: LoggerConfigPM, info: ValidationInfo) -> LoggerConfigPM:
        if "{api_slug}" in val.app_name:
            val.app_name = val.app_name.format(api_slug=info.data["slug"])

        val = FrozenLoggerConfigPM(**val.model_dump())
        return val

    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX_API)


class FrozenApiConfig(ApiConfig):

    @model_validator(mode="before")
    @classmethod
    def _check_args(cls, values: dict[str, Any]) -> dict[str, Any]:
        if is_running_server_cli:
            _has_host_arg = False
            for _i, _arg in enumerate(sys.argv):
                if (
                    _arg.startswith("--ssl")
                    or _arg.startswith("--keyfile")
                    or _arg.startswith("--certfile")
                ):
                    values["http_scheme"] = HTTPSchemeEnum.https

                if _arg.startswith("--host="):
                    _has_host_arg = True
                    values["bind_host"] = _arg.split("=")[1]
                elif (_arg == "--host") and (_i + 1 < len(sys.argv)):
                    _has_host_arg = True
                    values["bind_host"] = sys.argv[_i + 1]

                if _arg.startswith("--port="):
                    values["port"] = int(_arg.split("=")[1])
                elif (_arg == "--port") and (_i + 1 < len(sys.argv)):
                    values["port"] = int(sys.argv[_i + 1])

            if not _has_host_arg:
                values["bind_host"] = "127.0.0.1"

                if sys.argv[0].endswith("fastapi") and sys.argv[1] == "run":
                    values["bind_host"] = "0.0.0.0"  # nosec B104

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = [
    "ApiConfig",
    "FrozenApiConfig",
]
