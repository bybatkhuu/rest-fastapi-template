from typing import Any

from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Security, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from potato_util.constants import ALPHANUM_HOST_REGEX
from potato_util import validator

from api.core.constants import ErrorCodeEnum
from api.config import config
from api.helpers.crypto import jwt as jwt_helper
from api.core.exceptions import BaseHTTPException

_http_bearer = HTTPBearer(auto_error=False)


def auth_jwt(
    request: Request,
    authorization: HTTPAuthorizationCredentials | None = Security(_http_bearer),
) -> dict[str, Any]:
    """Dependency function to authenticate the access token (JWT) and get the payload.

    Args:
        request       (Request                     , required): The FastAPI request object.
        authorization (HTTPAuthorizationCredentials, required): 'Authorization: Bearer <access_token>'
                                                                    header credentials.

    Raises:
        BaseHTTPException: If the access token is missing.
        BaseHTTPException: If the access token has expired.
        BaseHTTPException: If the access token is invalid.

    Returns:
        dict[str, Any]: The decoded access token payload.
    """

    if not authorization:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_INVALID,
            message="Not authenticated!",
            headers={"WWW-Authenticate": 'Bearer error="missing_token"'},
        )

    _access_token: str = authorization.credentials
    if not validator.is_valid(val=_access_token, pattern=ALPHANUM_HOST_REGEX):
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_INVALID,
            message="Invalid access token!",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    _payload: dict[str, Any]
    try:
        _payload: dict[str, Any] = jwt_helper.decode(
            token=_access_token,
            key=config.api.security.jwt.secret,
            algorithm=config.api.security.jwt.algorithm,
        )
    except ExpiredSignatureError:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_EXPIRED,
            message="Access token has expired!",
            headers={"WWW-Authenticate": 'Bearer error="expired_token"'},
        )
    except InvalidTokenError:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_INVALID,
            message="Invalid access token!",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    request.state.user_id = _payload.get("sub")
    return _payload


def get_user_id(payload: dict[str, Any] = Depends(auth_jwt)) -> str:
    """Dependency function to get the user ID from the token payload.

    Args:
        payload (dict[str, Any], required): The decoded access token payload.

    Returns:
        str: The user ID.
    """

    _user_id: str = payload.get("sub", "")
    return _user_id


def is_auth(user_id: str = Depends(get_user_id)) -> bool:
    """Dependency function to check if the user is authenticated.

    Args:
        user_id (str, required): The user ID.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """

    if not user_id:
        return False

    return True


class AuthScopeDep:
    def __init__(self, allow_scope: str, allow_owner: bool = False):
        self.allow_scope = allow_scope
        self.allow_owner = allow_owner

    def __call__(
        self, request: Request, payload: dict[str, Any] = Depends(auth_jwt)
    ) -> dict[str, Any]:
        """Dependency function to check the scope permissions of the user.

        Args:
            request (Request       , required): The FastAPI request object.
            payload (dict[str, Any], required): The decoded access token (JWT) payload.

        Raises:
            BaseHTTPException: If the user has insufficient scope permissions.

        Returns:
            dict[str, Any]: The decoded access token payload.
        """

        if self.allow_owner:
            _auth_user_id: str = payload.get("sub", "")
            _path_params: list[str] = list(request.path_params.values())
            if _path_params and (_path_params[0] == _auth_user_id):
                return payload

        _token_all_scope: str = payload.get("scope", "")
        _token_scope_list: list[str] = _token_all_scope.split(" ")
        if self.allow_scope not in _token_scope_list:
            raise BaseHTTPException(
                error_enum=ErrorCodeEnum.FORBIDDEN,
                message="You do not have enough scope permissions!",
                description="The request requires more scope permissions.",
                headers={
                    "WWW-Authenticate": (
                        'Bearer error="insufficient_scope", '
                        'error_description="The request requires more scope permissions."'
                    )
                },
            )

        return payload


__all__ = [
    "auth_jwt",
    "get_user_id",
    "is_auth",
    "AuthScopeDep",
]
