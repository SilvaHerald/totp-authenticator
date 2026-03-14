"""Cryptography utilities for TOTP Authenticator."""

import base64
import os

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class InvalidPasswordError(Exception):
    """Raised when decryption fails due to an invalid password."""
    pass


def generate_salt() -> bytes:
    """Generate a random 16-byte salt for key derivation."""
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte url-safe base64 key using PBKDF2HMAC.

    480,000 iterations is the OWASP recommended minimum for PBKDF2-HMAC-SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def encrypt_data(plaintext: str, key: bytes) -> str:
    """
    Encrypt a plaintext string using Fernet (AES-128-CBC + HMAC-SHA256).
    Returns a url-safe base64 encoded string.
    """
    f = Fernet(key)
    # Fernet returns bytes, we decode it to str for JSON storage
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_data(ciphertext: str, key: bytes) -> str:
    """
    Decrypt a Fernet encrypted string.
    Raises InvalidPasswordError if the key is incorrect or data is corrupted.
    """
    f = Fernet(key)
    try:
        # Fernet expects bytes, and returns bytes
        decrypted = f.decrypt(ciphertext.encode("utf-8"))
        return decrypted.decode("utf-8")
    except (InvalidToken, InvalidSignature) as err:
        raise InvalidPasswordError("Invalid password or corrupted data.") from err
