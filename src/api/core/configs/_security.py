from typing import Any

from pydantic import Field, constr, SecretStr, model_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import (
    ENV_PREFIX_API,
    HTTP_METHOD_REGEX,
    ASYMMETRIC_ALGORITHM_REGEX,
    JWT_ALGORITHM_REGEX,
)
from ._base import FrozenBaseConfig


_ENV_PREFIX_SECURITY = f"{ENV_PREFIX_API}SECURITY_"


class CorsConfig(FrozenBaseConfig):
    allow_origins: list[constr(strip_whitespace=True, min_length=1, max_length=256)] = (  # type: ignore
        Field(default=["*"])
    )
    allow_origin_regex: (
        constr(strip_whitespace=True, min_length=1, max_length=256) | None  # type: ignore
    ) = Field(default=None)
    allow_headers: list[constr(strip_whitespace=True, min_length=1, max_length=128)] = (  # type: ignore
        Field(default=["*"])
    )
    allow_methods: list[constr(strip_whitespace=True, pattern=HTTP_METHOD_REGEX)] = (  # type: ignore
        Field(
            default=[
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "HEAD",
                "OPTIONS",
                "CONNECT",
            ]
        )
    )
    allow_credentials: bool = Field(default=False)
    expose_headers: list[
        constr(strip_whitespace=True, min_length=1, max_length=128)  # type: ignore
    ] = Field(default=[])
    max_age: int = Field(default=600, ge=0, le=86_400)  # Seconds (10 minutes)

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}CORS_")


class X509AttrsConfig(FrozenBaseConfig):
    C: constr(strip_whitespace=True, to_upper=True) = Field(default="US", min_length=2, max_length=2)  # type: ignore
    ST: constr(strip_whitespace=True) = Field(default="Washington", min_length=2, max_length=256)  # type: ignore
    L: constr(strip_whitespace=True) = Field(default="Seattle", min_length=2, max_length=256)  # type: ignore
    O: constr(strip_whitespace=True) = Field(default="Organization", min_length=2, max_length=256)  # type: ignore
    OU: constr(strip_whitespace=True) = Field(default="Organization Unit", min_length=2, max_length=256)  # type: ignore
    CN: constr(strip_whitespace=True) = Field(default="localhost", min_length=2, max_length=256)  # type: ignore
    DNS: constr(strip_whitespace=True) = Field(default="localhost", min_length=2, max_length=256)  # type: ignore

    model_config = SettingsConfigDict(
        env_prefix=f"{_ENV_PREFIX_SECURITY}SSL_X509_ATTRS_"
    )


class SSLConfig(FrozenBaseConfig):
    enabled: bool = Field(default=False)
    generate: bool = Field(default=False)
    key_size: int = Field(default=2048, ge=2048, le=8192)
    key_fname: constr(strip_whitespace=True) = Field(default="key.pem", min_length=2, max_length=256)  # type: ignore
    cert_fname: constr(strip_whitespace=True) = Field(default="cert.pem", min_length=2, max_length=256)  # type: ignore
    x509_attrs: X509AttrsConfig = Field(default_factory=X509AttrsConfig)

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}SSL_")


class AsymmetricConfig(FrozenBaseConfig):
    generate: bool = Field(default=False)
    algorithm: constr(strip_whitespace=True) = Field(default="RS256", pattern=ASYMMETRIC_ALGORITHM_REGEX)  # type: ignore
    key_size: int = Field(default=2048, ge=2048, le=8192)
    private_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        default="private_key.pem", min_length=2, max_length=256
    )
    public_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        default="public_key.pem", min_length=2, max_length=256
    )

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}ASYMMETRIC_")


class JWTConfig(FrozenBaseConfig):
    secret: SecretStr = Field(default="FT_JWT_SECRET123", min_length=8, max_length=64)
    algorithm: constr(strip_whitespace=True) = Field(default="HS256", pattern=JWT_ALGORITHM_REGEX)  # type: ignore

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}JWT_")


class PasswordConfig(FrozenBaseConfig):
    pepper: SecretStr = Field(
        default="FT_PASSWORD_PEPPER123", min_length=8, max_length=32
    )
    min_length: int = Field(default=8, ge=8, le=128)
    max_length: int = Field(default=128, ge=8, le=128)

    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values["max_length"] < values["min_length"]:
            raise ValueError(
                "`min_length` is greater than `max_length`, should be vice versa!"
            )

        return values

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}PASSWORD_")


class SecurityConfig(FrozenBaseConfig):
    allowed_hosts: list[constr(strip_whitespace=True, min_length=1, max_length=256)] = (  # type: ignore
        Field(default=["*"])
    )
    forwarded_allow_ips: list[
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ] = Field(default=["*"])
    cors: CorsConfig = Field(default_factory=CorsConfig)
    ssl: SSLConfig = Field(default_factory=SSLConfig)
    asymmetric: AsymmetricConfig = Field(default_factory=AsymmetricConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    password: PasswordConfig = Field(default_factory=PasswordConfig)

    model_config = SettingsConfigDict(env_prefix=_ENV_PREFIX_SECURITY)


__all__ = [
    "SecurityConfig",
    "CorsConfig",
    "X509AttrsConfig",
    "SSLConfig",
    "AsymmetricConfig",
    "JWTConfig",
    "PasswordConfig",
]
