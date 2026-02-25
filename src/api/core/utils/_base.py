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
    _is_running_cli = False
    for _keyword in CLI_KEYWORDS:
        if (
            sys.argv[0].endswith(_keyword)
            or sys.argv[0].endswith(f"{_keyword}.exe")
            or sys.argv[0].endswith(f"{_keyword}/__main__.py")
        ):
            _is_running_cli = True
            break

    return _is_running_cli


__all__ = [
    "is_running_cli",
]
