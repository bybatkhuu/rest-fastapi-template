from typing import Any

from fastapi import Request

from beans_logging_fastapi import log_http_error

from api.core.constants import ErrorCodeEnum
from api.config import config
from api.core.exceptions import PrimaryKeyError, UniqueKeyError
from api.core.responses import BaseResponse
from api.logger import logger


# For unhandled Exception or 500 internal server error:
def server_error_handler(request: Request, exc: Exception) -> BaseResponse:
    """Error handler for any kind of unhandled Exception or 500 internal server error.

    Args:
        request (Request  , required): Request object from FastAPI.
        exc     (Exception, required): Any kind of Exception object.

    Returns:
        BaseResponse: Response object.
    """

    _error_enum = ErrorCodeEnum.INTERNAL_SERVER_ERROR
    if isinstance(exc, PrimaryKeyError):
        _error_enum = ErrorCodeEnum.DB_PK_ERROR
    if isinstance(exc, UniqueKeyError):
        _error_enum = ErrorCodeEnum.DB_UQ_ERROR

    _request_id: str = request.state.request_id
    _exc_str = str(exc)
    _status_code = _error_enum.value.status_code
    _error: dict[str, Any] = _error_enum.value.model_dump()
    _error["detail"] = _exc_str
    _message: str = _error.get("message", "Internal Server Error")

    logger.exception(f"[{_request_id}] {_error_enum.value.code} - {_exc_str}")
    log_http_error(
        request=request,
        status_code=_status_code,
        msg_format_str=config.api.logger.http.std.err_msg_format_str,
    )
    return BaseResponse(
        request=request, status_code=_status_code, message=_message, error=_error
    )


__all__ = ["server_error_handler"]
