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
def is_running_bin() -> bool:
    """Checks if the application is running as a binary environment module (e.g., via uvicorn, fastapi, gunicorn, etc.)
    by inspecting the command-line arguments.

    Returns:
        bool: True if running as a binary environment module, False otherwise.
    """

    for _keyword in CLI_KEYWORDS:
        if (
            sys.argv[0].endswith(_keyword)
            or sys.argv[0].endswith(f"{_keyword}.exe")
            or sys.argv[0].endswith(f"{_keyword}/__main__.py")
        ):
            return True

    return False


__all__ = [
    "is_running_bin",
]
