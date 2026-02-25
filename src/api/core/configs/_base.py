import sys

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    CliSettingsSource,
    PydanticBaseSettingsSource,
)

is_running_server_cli = False
if (
    sys.argv[0].endswith("uvicorn")
    or sys.argv[0].endswith("fastapi")
    or sys.argv[0].endswith("gunicorn")
):
    is_running_server_cli = True


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        validate_default=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )


class FrozenBaseConfig(BaseConfig):
    model_config = SettingsConfigDict(frozen=True)


class BaseMainConfig(FrozenBaseConfig):

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:

        _sources = [file_secret_settings]
        if not is_running_server_cli:
            _sources.append(CliSettingsSource(settings_cls, cli_parse_args=True))
        _sources.extend([dotenv_settings, env_settings, init_settings])
        _sources = tuple(_sources)
        return _sources


__all__ = [
    "BaseConfig",
    "FrozenBaseConfig",
    "BaseMainConfig",
]
