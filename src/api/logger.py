from pydantic import validate_call
from fastapi.concurrency import run_in_threadpool

from beans_logging_fastapi import logger

from api.core.constants import WarnEnum


@validate_call
def log_mode(
    message: str, level: str = "INFO", warn_mode: WarnEnum = WarnEnum.ALWAYS
) -> None:
    """Log message with level and warn mode.

    Args:
        message   (str,          reqiured): Message to log.
        level     (LogLevelEnum, optional): Log level when warn mode is `WarnEnum.ALWAYS`. Defaults to "INFO".
        warn_mode (WarnEnum,     optional): Warn mode to use. Defaults to `WarnEnum.ALWAYS`.

    Raises:
        ValueError: If `level` is not a valid log level.
    """

    level = level.upper()
    if warn_mode == WarnEnum.ALWAYS:
        if level == "INFO":
            logger.info(message)
        elif level == "SUCCESS":
            logger.success(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "ERROR":
            logger.error(message)
        elif level == "CRITICAL":
            logger.critical(message)
        elif level == "TRACE":
            logger.trace(message)
        else:
            raise ValueError(f"Unknown log level: '{level}'")

    elif warn_mode == WarnEnum.DEBUG:
        logger.debug(message)

    return


@validate_call
async def async_log_mode(
    message: str, level: str = "INFO", warn_mode: WarnEnum = WarnEnum.ALWAYS
) -> None:
    """Log message with level and warn mode in async mode.

    Args:
        message   (str     , required): Message to log.
        level     (str     , optional): Log level when warn mode is `WarnEnum.ALWAYS`. Defaults to "INFO".
        warn_mode (WarnEnum, optional): Warn mode to use. Defaults to `WarnEnum.ALWAYS`.
    """

    level = level.upper()
    if warn_mode == WarnEnum.ALWAYS:
        if level == "INFO":
            await run_in_threadpool(logger.info, message)
        elif level == "SUCCESS":
            await run_in_threadpool(logger.success, message)
        elif level == "WARNING":
            await run_in_threadpool(logger.warning, message)
        elif level == "ERROR":
            await run_in_threadpool(logger.error, message)
        elif level == "CRITICAL":
            await run_in_threadpool(logger.critical, message)
        elif level == "TRACE":
            await run_in_threadpool(logger.trace, message)
        else:
            raise ValueError(f"Unknown log level: '{level}'")

    elif warn_mode == WarnEnum.DEBUG:
        await run_in_threadpool(logger.debug, message)

    return


__all__ = [
    "logger",
    "log_mode",
    "async_log_mode",
]
