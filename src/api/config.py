import os

from potato_util.io import read_all_configs

from api.core.constants import ENV_PREFIX_API, API_SLUG
from api.core.configs import MainConfig
from api.logger import logger

# _configs_dir = os.path.join(os.getcwd(), "..", "configs")
_configs_dir = os.path.join("/etc", API_SLUG)
_configs_dir_env = os.getenv(f"{ENV_PREFIX_API}CONFIGS_DIR", "")
if _configs_dir_env:
    _configs_dir = _configs_dir_env

_config_dict = {}
if os.path.isdir(_configs_dir):
    _config_dict = read_all_configs(configs_dir=_configs_dir)

try:
    config = MainConfig(**_config_dict)
except Exception:
    logger.exception("Failed to load config:")
    raise SystemExit(1)


__all__ = [
    "MainConfig",
    "config",
]
