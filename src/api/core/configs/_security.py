from pydantic import Field, constr, SecretStr
from pydantic_settings import SettingsConfigDict

from api.core.constants import (
    ENV_PREFIX,
    ENV_PREFIX_API,
    HTTP_METHOD_REGEX,
    ASYMMETRIC_ALGORITHM_REGEX,
    JWT_ALGORITHM_REGEX,
)

from ._base import FrozenBaseConfig

_ENV_PREFIX_SECURITY = f"{ENV_PREFIX_API}SECURITY_"


class CorsConfig(FrozenBaseConfig):
    allow_origins: list[str] = Field(default=["*"])
    allow_origin_regex: str | None = Field(default=None)
    allow_headers: list[str] = Field(default=["*"])
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
    expose_headers: list[str] = Field(default=[])
    max_age: int = Field(default=600, ge=0, le=86_400)  # Seconds (10 minutes)

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}CORS_")


class X509AttrsConfig(FrozenBaseConfig):
    C: str = Field(default="US", min_length=2, max_length=2)
    ST: str = Field(default="Washington", min_length=2, max_length=256)
    L: str = Field(default="Seattle", min_length=2, max_length=256)
    O: str = Field(default="Organization", min_length=2, max_length=256)
    OU: str = Field(default="Organization Unit", min_length=2, max_length=256)
    CN: str = Field(default="localhost", min_length=2, max_length=256)
    DNS: str = Field(default="localhost", min_length=2, max_length=256)

    model_config = SettingsConfigDict(
        env_prefix=f"{_ENV_PREFIX_SECURITY}SSL_X509_ATTRS_"
    )


class SSLConfig(FrozenBaseConfig):
    enabled: bool = Field(default=False)
    generate: bool = Field(default=False)
    key_size: int = Field(default=2048, ge=2048, le=8192)
    key_fname: str = Field(default="key.pem", min_length=2, max_length=256)
    cert_fname: str = Field(default="cert.pem", min_length=2, max_length=256)
    x509_attrs: X509AttrsConfig = Field(default_factory=X509AttrsConfig)

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}SSL_")


class AsymmetricConfig(FrozenBaseConfig):
    generate: bool = Field(default=False)
    algorithm: str = Field(default="RS256", pattern=ASYMMETRIC_ALGORITHM_REGEX)
    key_size: int = Field(default=2048, ge=2048, le=8192)
    private_key_fname: str = Field(
        default="private_key.pem", min_length=2, max_length=256
    )
    public_key_fname: str = Field(
        default="public_key.pem", min_length=2, max_length=256
    )

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}ASYMMETRIC_")


class JWTConfig(FrozenBaseConfig):
    secret: SecretStr = Field(
        default_factory=lambda: SecretStr(f"{ENV_PREFIX}JWT_SECRET123"),
        min_length=8,
        max_length=64,
    )
    algorithm: str = Field(default="HS256", pattern=JWT_ALGORITHM_REGEX)

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}JWT_")


class PasswordConfig(FrozenBaseConfig):
    pepper: SecretStr = Field(
        default_factory=lambda: SecretStr(f"{ENV_PREFIX}PASSWORD_PEPPER123"),
        min_length=8,
        max_length=32,
    )
    min_length: int = Field(default=8, ge=8, le=128)
    max_length: int = Field(default=128, ge=8, le=128)

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}PASSWORD_")


class SecurityConfig(FrozenBaseConfig):
    allowed_hosts: list[str] = Field(default=["*"])
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
