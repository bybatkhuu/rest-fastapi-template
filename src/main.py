#!/usr/bin/env python

# Third-party libraries
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(override=True)

# Internal modules
from api.bootstrap import create_app, run_server  # noqa: E402
from api.logger import logger  # noqa: E402


app: FastAPI = create_app()


def main() -> None:
    """Main function."""

    run_server(app="main:app")
    return


if __name__ == "__main__":
    logger.info("Starting server from 'main.py'...")
    main()


__all__ = ["app"]
