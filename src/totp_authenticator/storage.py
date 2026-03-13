"""Config file storage for TOTP accounts — fully offline, local-only."""

import base64
import json
import os
import uuid
from dataclasses import asdict, dataclass

from totp_authenticator.crypto import (
    InvalidPasswordError,
    decrypt_data,
    derive_key,
    encrypt_data,
    generate_salt,
)

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".totp_config.json")


@dataclass
class Account:
    """A single TOTP account entry."""

    id: str
    name: str
    secret: str


@dataclass
class Settings:
    """Application preferences and window state."""

    theme: str = "dark"
    window_x: int | None = None
    window_y: int | None = None
    lock_timeout_minutes: int = 5


def read_raw_config() -> dict:
    """Read the raw JSON data from the config file."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, TypeError):
        return {}


def is_config_encrypted() -> bool:
    """Check if the config file is currently password protected."""
    return read_raw_config().get("is_encrypted", False)


def verify_password(password: str) -> bytes:
    """Verify the password against the stored salt and encrypted data.

    Returns: The valid encryption key if successful.
    Raises: InvalidPasswordError if the password is wrong or config is missing/corrupted.
    """
    data = read_raw_config()
    if not data.get("is_encrypted"):
        raise InvalidPasswordError("Config is not encrypted.")

    salt_b64 = data.get("salt")
    encrypted_data = data.get("encrypted_data")
    if not salt_b64 or not encrypted_data:
        raise InvalidPasswordError("Config is corrupted: missing salt or encrypted_data.")

    salt = base64.urlsafe_b64decode(salt_b64.encode("utf-8"))
    key = derive_key(password, salt)

    # Try to decrypt the data to verify the key
    decrypt_data(encrypted_data, key)
    return key


def set_encryption(password: str, current_key: bytes | None = None) -> bytes:
    """Change or enable password protection."""
    accounts = load_accounts(current_key)
    salt = generate_salt()
    new_key = derive_key(password, salt)

    data = read_raw_config()
    data["is_encrypted"] = True
    data["salt"] = base64.urlsafe_b64encode(salt).decode("utf-8")

    accounts_json = json.dumps([asdict(a) for a in accounts])
    data["encrypted_data"] = encrypt_data(accounts_json, new_key)
    if "accounts" in data:
        del data["accounts"]

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return new_key


def remove_encryption(current_key: bytes) -> None:
    """Disable password protection and save accounts in plaintext."""
    accounts = load_accounts(current_key)
    data = read_raw_config()

    data["is_encrypted"] = False
    if "salt" in data:
        del data["salt"]
    if "encrypted_data" in data:
        del data["encrypted_data"]

    data["accounts"] = [asdict(a) for a in accounts]

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _migrate_legacy(data: dict) -> list[dict]:
    """Convert v0.1 single-secret format to multi-account list format.

    Args:
        data: Raw JSON dict that contains a top-level 'secret' key.

    Returns:
        A list of account dicts in the new format.
    """
    return [{"id": str(uuid.uuid4()), "name": "My Account", "secret": data["secret"]}]


def load_accounts(key: bytes | None = None) -> list[Account]:
    """Load all saved TOTP accounts from the config file.

    Automatically migrates legacy single-secret config (v0.1) to the new
    multi-account format on first load.

    Args:
        key: The decryption key. Must be provided if is_config_encrypted() is True.

    Returns:
        List of Account objects, or empty list if no config exists.

    Raises:
        InvalidPasswordError: If the config is encrypted and key is missing/invalid.
    """
    data = read_raw_config()
    if not data:
        return []

    if data.get("is_encrypted", False):
        if not key:
            raise InvalidPasswordError("No decryption key provided for encrypted config.")
        encrypted_data = data.get("encrypted_data")
        if not encrypted_data:
            return []
        accounts_json_str = decrypt_data(encrypted_data, key)
        try:
            accounts_list = json.loads(accounts_json_str)
            return [Account(**a) for a in accounts_list]
        except json.JSONDecodeError as err:
            raise InvalidPasswordError("Decrypted data is not valid JSON.") from err

    # Plaintext mode
    # Migrate v0.1 format: {"secret": "..."} → multi-account format
    if "secret" in data and "accounts" not in data:
        accounts = _migrate_legacy(data)
        _write_raw(accounts, key=None)
        return [Account(**a) for a in accounts]

    return [Account(**a) for a in data.get("accounts", [])]


def save_accounts(accounts: list[Account], key: bytes | None = None) -> None:
    """Persist the full list of accounts to the config file.

    Args:
        accounts: List of Account objects to save.
        key: The decryption key. Must be provided if is_config_encrypted() is True.
    """
    _write_raw([asdict(a) for a in accounts], key=key)


def load_settings() -> Settings:
    """Load the application settings from the config file.

    Returns:
        Settings object with loaded or default values.
    """
    data = read_raw_config()
    settings_dict = data.get("settings", {})
    return Settings(
        theme=settings_dict.get("theme", "dark"),
        window_x=settings_dict.get("window_x"),
        window_y=settings_dict.get("window_y"),
        lock_timeout_minutes=settings_dict.get("lock_timeout_minutes", 5),
    )


def save_settings(settings: Settings) -> None:
    """Persist the application settings to the config file.

    This function updates the 'settings' key without modifying 'accounts',
    nor does it mess up encryption structure since settings are left plaintext.
    """
    data = read_raw_config()
    data["settings"] = asdict(settings)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _write_raw(accounts: list[dict], key: bytes | None = None) -> None:
    """Write raw account dicts to disk, preserving settings and encryption."""
    data = read_raw_config()

    if "secret" in data:
        del data["secret"]

    if data.get("is_encrypted", False):
        if not key:
            raise InvalidPasswordError("No decryption key provided to save encrypted accounts.")
        accounts_json = json.dumps(accounts)
        data["encrypted_data"] = encrypt_data(accounts_json, key)
    else:
        data["accounts"] = accounts

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_account(name: str, secret: str, key: bytes | None = None) -> Account:
    """Create and persist a new TOTP account.

    Args:
        name: Display name for the account.
        secret: Base32-encoded TOTP secret key.
        key: The decryption key.

    Returns:
        The newly created Account.
    """
    accounts = load_accounts(key)
    new_account = Account(id=str(uuid.uuid4()), name=name, secret=secret)
    accounts.append(new_account)
    save_accounts(accounts, key)
    return new_account


def delete_account(account_id: str, key: bytes | None = None) -> None:
    """Remove an account by its ID.

    Args:
        account_id: The unique ID of the account to remove.
                    No-op if the ID does not exist.
        key: The decryption key.
    """
    accounts = [a for a in load_accounts(key) if a.id != account_id]
    save_accounts(accounts, key)


def rename_account(account_id: str, new_name: str, key: bytes | None = None) -> None:
    """Rename an account by its ID.

    Args:
        account_id: The unique ID of the account to rename.
        new_name: The new display name.
        key: The decryption key.
    """
    accounts = load_accounts(key)
    for account in accounts:
        if account.id == account_id:
            account.name = new_name
            break
    save_accounts(accounts, key)
