"""Config file storage for TOTP secrets — fully offline, local-only."""

import json
import os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".totp_config.json")


def load_secret() -> str:
    """Load the saved TOTP secret from the config file.

    Returns:
        The saved secret string, or empty string if no config exists.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("secret", "")
        except (json.JSONDecodeError, OSError):
            return ""
    return ""


def save_secret(secret: str) -> None:
    """Persist a TOTP secret to the config file.

    Args:
        secret: The Base32-encoded secret key to save.
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"secret": secret}, f)
