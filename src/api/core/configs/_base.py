from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    CliSettingsSource,
    NestedSecretsSettingsSource,
)

from api.core import utils


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        validate_default=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )


class FrozenBaseConfig(BaseConfig):
    model_config = SettingsConfigDict(frozen=True)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            NestedSecretsSettingsSource(file_secret_settings),
            dotenv_settings,
            env_settings,
            init_settings,
        )


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
        _sources = []
        if not utils.is_running_cli():
            _sources.append(CliSettingsSource(settings_cls, cli_parse_args=True))
        _sources.extend(
            [
                NestedSecretsSettingsSource(file_secret_settings),
                dotenv_settings,
                env_settings,
                init_settings,
            ]
        )
        return tuple(_sources)


__all__ = [
    "BaseConfig",
    "FrozenBaseConfig",
    "BaseMainConfig",
]
