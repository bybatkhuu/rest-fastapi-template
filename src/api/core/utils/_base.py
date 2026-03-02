import sys
from functools import lru_cache

BINARY_MODULES = [
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

    for _binary_module in BINARY_MODULES:
        if (
            sys.argv[0].endswith(_binary_module)
            or sys.argv[0].endswith(f"{_binary_module}.exe")
            or sys.argv[0].endswith(f"{_binary_module}/__main__.py")
        ):
            return True

    return False


__all__ = [
    "is_running_bin",
]
