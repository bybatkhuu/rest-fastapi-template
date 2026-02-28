import os
from typing import TypeVar, Any

from pydantic import validate_call

from potato_util.io import read_all_configs

from api.core.constants import ENV_PREFIX_API, API_SLUG
from api.core.configs import MainConfig
from api.logger import logger

ConfigType = TypeVar("ConfigType", bound=MainConfig)


@validate_call
def load_config(
    configs_dir: str = os.path.join("/etc", API_SLUG),
    env_name: str = f"{ENV_PREFIX_API}CONFIGS_DIR",
    config_schema: type[ConfigType] = MainConfig,
) -> ConfigType:
    _configs_dir_env = os.getenv(env_name, "")
    if _configs_dir_env:
        configs_dir = _configs_dir_env

    _config_dict: dict[str, Any] = {}
    if os.path.isdir(configs_dir):
        _config_dict = read_all_configs(configs_dir=configs_dir)

    _config: ConfigType | None = None
    try:
        _config = config_schema(**_config_dict)
    except Exception:
        logger.exception("Failed to load config:")
        raise SystemExit(1)

    return _config


config = load_config()


__all__ = [
    "MainConfig",
    "load_config",
    "config",
]
