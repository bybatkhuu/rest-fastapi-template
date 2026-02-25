from typing import Any

import jwt
from jwt.types import Options
from jwt.api_jwt import AllowedPrivateKeyTypes, AllowedPublicKeyTypes
from pydantic import validate_call, SecretStr

from potato_util.dt import now_utc_dt


@validate_call(config={"arbitrary_types_allowed": True})
def encode(
    payload: dict[str, Any], key: SecretStr | AllowedPrivateKeyTypes, algorithm: str
) -> str:
    """Encodes payload into JWT token.

    Args:
        payload    (dict[str, Any]                    , required): Payload to encode into token.
        key        (SecretStr | AllowedPrivateKeyTypes, required): Secret key to encode token with.
        algorithm  (str                               , required): Algorithm to encode token with.

    Raises:
        ValueError: If 'sub' is not provided in payload.
        ValueError: If 'jti' is not provided in payload.
        ValueError: If 'exp' is not provided in payload.

    Returns:
        str: Encoded JWT token.
    """

    if "sub" not in payload:
        raise ValueError("`sub` is required in payload!")

    if "exp" not in payload:
        raise ValueError("'exp' is required in payload!")

    if "iat" not in payload:
        payload["iat"] = now_utc_dt()

    if "jti" not in payload:
        raise ValueError("'jti' is required in payload!")

    if isinstance(key, SecretStr):
        key = key.get_secret_value()

    _jwt_token = jwt.encode(payload=payload, key=key, algorithm=algorithm)
    return _jwt_token


@validate_call(config={"arbitrary_types_allowed": True})
def decode(
    token: str,
    key: SecretStr | AllowedPublicKeyTypes,
    algorithm: str,
    options: Options = {},
) -> dict[str, Any]:
    """Decodes JWT token and returns payload.

    Args:
        token     (str                              , required): JWT token to decode.
        key       (SecretStr | AllowedPublicKeyTypes, required): Secret key to decode token with.
        algorithm (str                              , required): Algorithm to decode token with.
        options   (Options                          , optional): Options to decode token with. Defaults to {}.

    Raises:
        jwt.ExpiredSignatureError: If token is expired.
        jwt.InvalidTokenError    : If token is invalid.

    Returns:
        dict[str, Any]: Decoded payload from JWT token.
    """

    if "require" not in options:
        options["require"] = ["sub", "exp", "iat", "jti"]

    if isinstance(key, SecretStr):
        key = key.get_secret_value()

    _payload = jwt.decode(jwt=token, key=key, algorithms=[algorithm], options=options)
    return _payload


__all__ = [
    "encode",
    "decode",
]
