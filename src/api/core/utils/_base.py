import sys
from functools import lru_cache

CLI_KEYWORDS = [
    "uvicorn",
    "gunicorn",
    "fastapi",
    "pytest",
    "unittest",
    "alembic",
]


@lru_cache
def is_running_cli() -> bool:
    for _keyword in CLI_KEYWORDS:
        if (
            sys.argv[0].endswith(_keyword)
            or sys.argv[0].endswith(f"{_keyword}.exe")
            or sys.argv[0].endswith(f"{_keyword}/__main__.py")
        ):
            return True

    return False


__all__ = [
    "is_running_cli",
]
