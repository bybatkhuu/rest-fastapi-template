from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import validate_call, SecretStr
from fastapi.concurrency import run_in_threadpool


@validate_call
def hash(
    password: SecretStr, password_salt: SecretStr, password_pepper: SecretStr
) -> str:
    """Hashes password with salt and pepper using Argon2id.

    Args:
        password        (SecretStr, required): Password to hash.
        password_salt   (SecretStr, required): Salt to hash password with.
        password_pepper (SecretStr, required): Pepper to hash password with.

    Returns:
        str: Hashed password.
    """

    _ph = PasswordHasher()
    _seasoned_password = (
        password.get_secret_value()
        + password_salt.get_secret_value()
        + password_pepper.get_secret_value()
    )
    _hash_password = _ph.hash(_seasoned_password)
    return _hash_password


@validate_call
def verify(
    hashed_password: str,
    password: SecretStr,
    password_salt: SecretStr,
    password_pepper: SecretStr,
) -> bool:
    """Verifies password with salt and pepper against hashed password using Argon2id.

    Args:
        hashed_password (str      , required): Hashed password.
        password        (SecretStr, required): Raw password to verify.
        password_salt   (SecretStr, required): Salt to verify password with.
        password_pepper (SecretStr, required): Pepper to verify password with.

    Returns:
        bool: True if password is match, False otherwise.
    """

    _ph = PasswordHasher()
    _seasoned_password = (
        password.get_secret_value()
        + password_salt.get_secret_value()
        + password_pepper.get_secret_value()
    )

    try:
        _ph.verify(hashed_password, _seasoned_password)
        return True
    except VerifyMismatchError:
        return False


@validate_call
async def async_hash(
    password: SecretStr, password_salt: SecretStr, password_pepper: SecretStr
) -> str:
    """Async hashes password with salt and pepper using Argon2id.

    Args:
        password        (SecretStr, required): Password to hash.
        password_pepper (SecretStr, required): Pepper to hash password with.
        password_salt   (SecretStr, required): Salt to hash password with.

    Returns:
        str: Hashed password.
    """

    _hash_password: str = await run_in_threadpool(
        hash, password, password_salt, password_pepper
    )
    return _hash_password


@validate_call
async def async_verify(
    hashed_password: str,
    password: SecretStr,
    password_salt: SecretStr,
    password_pepper: SecretStr,
) -> bool:
    """Async verifies password with salt against hashed password using Argon2id.

    Args:
        hashed_password (str      , required): Hashed password.
        password        (SecretStr, required): Raw password to verify.
        password_salt   (SecretStr, required): Salt to verify password with.
        password_pepper (SecretStr, required): Pepper to verify password with.

    Returns:
        bool: True if password is match, False otherwise.
    """

    _is_match: bool = await run_in_threadpool(
        verify, hashed_password, password, password_salt, password_pepper
    )
    return _is_match


__all__ = [
    "hash",
    "verify",
    "async_hash",
    "async_verify",
]
