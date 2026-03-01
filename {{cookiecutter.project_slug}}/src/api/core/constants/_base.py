ENV_PREFIX = "{{cookiecutter.env_prefix}}"
ENV_PREFIX_API = f"{ENV_PREFIX}API_"

API_SLUG = "{{cookiecutter.project_slug}}"

__all__ = [
    "ENV_PREFIX",
    "ENV_PREFIX_API",
    "API_SLUG",
]
