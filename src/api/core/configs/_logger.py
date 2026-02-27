import os

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

from beans_logging.config import FileConfigPM as BaseFileConfigPM
from beans_logging_fastapi import LoggerConfigPM as BaseLoggerConfigPM

from api.core.constants import ENV_PREFIX_API

from ._base import BaseConfig


class FileConfigPM(BaseFileConfigPM, BaseConfig):
    logs_dir: str = Field(default="/var/log/{api_slug}", min_length=2, max_length=1024)

    @field_validator("logs_dir", mode="after")
    @classmethod
    def _check_logger(cls, val: str) -> str:
        _logs_dir = os.getenv(f"{ENV_PREFIX_API}LOGS_DIR", "")
        if _logs_dir:
            val = _logs_dir

        return val


class LoggerConfigPM(BaseLoggerConfigPM, BaseConfig):
    app_name: str = Field(default="{api_slug}", min_length=1, max_length=128)
    file: FileConfigPM = Field(default_factory=FileConfigPM)

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}LOGGER_")


class FrozenLoggerConfigPM(LoggerConfigPM):
    model_config = SettingsConfigDict(frozen=True)


__all__ = [
    "FileConfigPM",
    "LoggerConfigPM",
    "FrozenLoggerConfigPM",
]
