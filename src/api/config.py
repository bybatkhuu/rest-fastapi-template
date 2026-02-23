import os

from potato_util.io import read_all_configs

from api.core.configs import MainConfig
from api.logger import logger

_config_dict = {}
_configs_dir = os.path.join(os.getcwd(), "configs")
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
