from pydantic import Field
from pydantic_settings import SettingsConfigDict

from api.core.constants import ENV_PREFIX_API

from ._base import FrozenBaseConfig


class GZipConfig(FrozenBaseConfig):
    min_size: int = Field(default=1024, ge=0, le=10_485_760)
    compresslevel: int = Field(default=9, ge=1, le=9)

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}GZIP_")


__all__ = ["GZipConfig"]
