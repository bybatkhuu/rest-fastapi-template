from enum import Enum

ENV_PREFIX = "FT_"
ENV_PREFIX_API = f"{ENV_PREFIX}API_"

API_SLUG = "rest-fastapi-template"


class EnvEnum(str, Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"
    DEMO = "DEMO"
    DOCS = "DOCS"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class WarnEnum(str, Enum):
    ERROR = "ERROR"
    ALWAYS = "ALWAYS"
    DEBUG = "DEBUG"
    IGNORE = "IGNORE"


class HashAlgoEnum(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha224 = "sha224"
    sha256 = "sha256"
    sha384 = "sha384"
    sha512 = "sha512"


class ConfigFileFormatEnum(str, Enum):
    YAML = "YAML"
    JSON = "JSON"
    TOML = "TOML"
    INI = "INI"


class HTTPSchemeEnum(str, Enum):
    http = "http"
    https = "https"


__all__ = [
    "ENV_PREFIX",
    "ENV_PREFIX_API",
    "API_SLUG",
    "EnvEnum",
    "WarnEnum",
    "HashAlgoEnum",
    "ConfigFileFormatEnum",
    "HTTPSchemeEnum",
]
