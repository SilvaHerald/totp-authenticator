"""URI Parser for otpauth:// links."""

import base64
import urllib.parse
from dataclasses import dataclass


class InvalidURIError(Exception):
    """Raised when the provided URI is not a valid otpauth TOTP link."""
    pass


@dataclass
class ParsedAccount:
    """Represents data extracted from an otpauth URI."""
    name: str
    secret: str


def parse_uri(uri: str) -> ParsedAccount:
    """
    Parse an otpauth:// URI and extract the account name and secret.

    Format: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example

    Args:
        uri: The URI string to parse.

    Returns:
        A ParsedAccount object containing the name and valid secret.

    Raises:
        InvalidURIError: If the URI gets malformed or lacks a valid base32 secret.
    """
    if not uri or not uri.strip():
        raise InvalidURIError("URI cannot be empty.")

    parsed = urllib.parse.urlparse(uri.strip())

    if parsed.scheme != "otpauth":
        raise InvalidURIError("Invalid scheme. Expected 'otpauth://'.")

    if parsed.netloc != "totp":
        raise InvalidURIError("Only 'totp' (Time-based OTP) is supported.")

    # Extract path /Example:alice@google.com -> Example:alice@google.com
    path = urllib.parse.unquote(parsed.path)
    if path.startswith("/"):
        path = path[1:]

    query = urllib.parse.parse_qs(parsed.query)

    # 1. Extract secret
    secrets = query.get("secret")
    if not secrets:
        raise InvalidURIError("URI is missing the 'secret' parameter.")
    secret = secrets[0].replace(" ", "").upper()

    # Validate base32
    try:
        if "=" in secret:
            secret = secret.replace("=", "")
        padding = len(secret) % 8
        if padding != 0:
            secret += "=" * (8 - padding)
        base64.b32decode(secret, casefold=True)
    except Exception as err:
        raise InvalidURIError("The 'secret' parameter is not valid base32.") from err

    # 2. Extract name
    # The name may be in the path, or combination of issuer + path
    name = path
    if not name:
        issuers = query.get("issuer")
        name = issuers[0] if issuers else "Unknown Account"

    return ParsedAccount(name=name, secret=secret.replace("=", ""))
