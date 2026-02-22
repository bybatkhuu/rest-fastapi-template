from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    CliSettingsSource,
    PydanticBaseSettingsSource,
)


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        validate_default=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

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
            file_secret_settings,
            dotenv_settings,
            env_settings,
            CliSettingsSource(settings_cls, cli_parse_args=True),
            init_settings,
        )


class FrozenBaseConfig(BaseConfig):
    model_config = SettingsConfigDict(frozen=True)


__all__ = [
    "BaseConfig",
    "FrozenBaseConfig",
]
