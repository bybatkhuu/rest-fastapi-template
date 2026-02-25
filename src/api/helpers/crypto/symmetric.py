import base64

from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from pydantic import validate_call

from potato_util.constants import WarnEnum
from beans_logging import logger


@validate_call(config={"arbitrary_types_allowed": True})
def decrypt_aes_cbc(
    ciphertext: str | bytes,
    key: bytes,
    iv: bytes,
    base64_decode: bool = False,
    as_str: bool = False,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> str | bytes:
    """Decrypts a ciphertext using AES-CBC key and iv.

    Args:
        ciphertext    (str | bytes, required): The ciphertext to decrypt.
        key           (bytes      , required): The key to use for decryption.
        iv            (bytes      , required): The initialization vector to use for decryption.
        base64_decode (bool       , optional): Whether to decode the ciphertext from base64. Defaults to False.
        as_str        (bool       , optional): Whether to return the plaintext as a string or bytes.
                                                        Defaults to False.
        warn_mode     (WarnEnum   , optional): The warning mode to use. Defaults to WarnEnum.DEBUG.

    Raises:
        Exception: If failed to decrypt ciphertext using AES-CBC key and iv for any reason.

    Returns:
        str | bytes: The decrypted plaintext as a string or bytes.
    """

    if isinstance(ciphertext, str):
        ciphertext = ciphertext.encode()

    if base64_decode:
        ciphertext = base64.b64decode(ciphertext)

    _plaintext: str | bytes
    try:
        _message = "Decrypting ciphertext using AES-CBC key and iv..."
        if warn_mode == WarnEnum.ALWAYS:
            logger.info(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        _cipher = ciphers.Cipher(
            algorithm=algorithms.AES(key=key), mode=modes.CBC(initialization_vector=iv)
        )
        _decryptor = _cipher.decryptor()
        _plaintext = _decryptor.update(data=ciphertext) + _decryptor.finalize()

        _message = "Successfully decrypted ciphertext using AES-CBC key and iv."
        if warn_mode == WarnEnum.ALWAYS:
            logger.success(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

    except Exception:
        _message = "Failed to decrypt ciphertext using AES-CBC key and iv!"
        if warn_mode == WarnEnum.ALWAYS:
            logger.error(_message)
        elif warn_mode == WarnEnum.DEBUG:
            logger.debug(_message)

        raise

    if as_str:
        _plaintext = _plaintext.decode()

    return _plaintext


__all__ = [
    "decrypt_aes_cbc",
]
