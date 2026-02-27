# Third-party libraries
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(override=True)

# Internal modules
from api.bootstrap import create_app, run_server  # noqa: E402

app: FastAPI = create_app()


def main() -> None:
    """Main function."""

    run_server(app="api.main:app")
    return


__all__ = [
    "app",
    "main",
]
