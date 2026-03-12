"""Core TOTP logic — pure Python, no UI dependencies."""

import time

import pyotp


def get_code(secret: str) -> str | None:
    """Generate the current TOTP code for a given secret.

    Args:
        secret: Base32-encoded TOTP secret key.

    Returns:
        6-digit TOTP code string, or None if the secret is empty/invalid.
    """
    secret = secret.strip().replace(" ", "")
    if not secret:
        return None
    try:
        return pyotp.TOTP(secret).now()
    except Exception:
        return None


def validate_secret(secret: str) -> bool:
    """Check whether a secret key is valid for TOTP generation.

    Args:
        secret: Base32-encoded TOTP secret key.

    Returns:
        True if the secret can produce a valid TOTP code.
    """
    secret = secret.strip().replace(" ", "")
    if not secret:
        return False
    try:
        pyotp.TOTP(secret).now()
        return True
    except Exception:
        return False


def get_remaining_seconds() -> int:
    """Return seconds remaining until the current TOTP code expires.

    Returns:
        Integer in range [1, 30].
    """
    return 30 - (int(time.time()) % 30)
