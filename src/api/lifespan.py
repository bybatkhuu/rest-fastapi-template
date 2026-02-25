import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from potato_util.io import async_create_dir

from api.__version__ import __version__
from api.config import config
from api.helpers.crypto import asymmetric as asymmetric_helper
from api.helpers.crypto import ssl as ssl_helper
from api.logger import logger


def _create_ssl_certs() -> None:
    """Create SSL certificates if enabled and not exist."""

    if config.api.security.ssl.generate:
        ssl_helper.create_ssl_certs(
            ssl_dir=config.api.paths.ssl_dir,
            key_fname=config.api.security.ssl.key_fname,
            cert_fname=config.api.security.ssl.cert_fname,
            key_size=config.api.security.ssl.key_size,
            x509_attrs=config.api.security.ssl.x509_attrs.model_dump(),
        )

    return


def _check_ssl_certs() -> None:
    """Check SSL certificates if enabled."""

    if config.api.security.ssl.enabled:
        _ssl_keyfile_path = os.path.join(
            config.api.paths.ssl_dir, config.api.security.ssl.key_fname
        )
        _ssl_certfile_path = os.path.join(
            config.api.paths.ssl_dir, config.api.security.ssl.cert_fname
        )

        if (not os.path.isfile(_ssl_keyfile_path)) or (
            not os.path.isfile(_ssl_certfile_path)
        ):
            logger.error("SSL key or certificate file not found!")
            raise SystemExit(1)

    return


def pre_init() -> None:
    """Pre-initialization tasks before creating FastAPI application."""

    _create_ssl_certs()
    _check_ssl_certs()

    return


async def _async_create_dirs() -> None:
    """Create directories before starting FastAPI application.

    Raises:
        SystemExit: If failed to create directories.
    """

    try:
        await async_create_dir(config.api.paths.data_dir)
        # Add directories needs to be created here...
    except Exception:
        logger.exception("Failed to create directories:")
        raise SystemExit(1)

    return


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for FastAPI application.
    Startup and shutdown events are logged.

    Args:
        app (FastAPI, required): FastAPI application instance.
    """

    logger.info("Preparing to startup...")
    # await _async_create_dirs()
    if config.api.security.asymmetric.generate:
        await asymmetric_helper.async_create_keys(
            asymmetric_keys_dir=config.api.paths.asymmetric_keys_dir,
            key_size=config.api.security.asymmetric.key_size,
            private_key_fname=config.api.security.asymmetric.private_key_fname,
            public_key_fname=config.api.security.asymmetric.public_key_fname,
        )

    # Add startup code here...
    logger.success("Finished preparation to startup.")
    logger.opt(colors=True).info(f"Version: <c>{__version__}</c>")
    logger.opt(colors=True).info(f"API version: <c>{config.api.version}</c>")
    logger.opt(colors=True).info(f"API prefix: <c>{config.api.prefix}</c>")
    logger.opt(colors=True).info(
        f"Listening on: <c>{config.api.http_scheme}://{config.api.bind_host}:{config.api.port}</c>"
    )

    yield

    logger.info("Praparing to shutdown...")
    # Add shutdown code here...
    logger.success("Finished preparation to shutdown.")


__all__ = [
    "pre_init",
    "lifespan",
]
