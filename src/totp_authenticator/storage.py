"""Config file storage for TOTP accounts — fully offline, local-only."""

import json
import os
import uuid
from dataclasses import asdict, dataclass

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".totp_config.json")


@dataclass
class Account:
    """A single TOTP account entry."""

    id: str
    name: str
    secret: str


def _migrate_legacy(data: dict) -> list[dict]:
    """Convert v0.1 single-secret format to multi-account list format.

    Args:
        data: Raw JSON dict that contains a top-level 'secret' key.

    Returns:
        A list of account dicts in the new format.
    """
    return [{"id": str(uuid.uuid4()), "name": "My Account", "secret": data["secret"]}]


def load_accounts() -> list[Account]:
    """Load all saved TOTP accounts from the config file.

    Automatically migrates legacy single-secret config (v0.1) to the new
    multi-account format on first load.

    Returns:
        List of Account objects, or empty list if no config exists.
    """
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)

        # Migrate v0.1 format: {"secret": "..."} → multi-account format
        if "secret" in data and "accounts" not in data:
            accounts = _migrate_legacy(data)
            _write_raw(accounts)
            return [Account(**a) for a in accounts]

        return [Account(**a) for a in data.get("accounts", [])]
    except (json.JSONDecodeError, OSError, TypeError, KeyError):
        return []


def save_accounts(accounts: list[Account]) -> None:
    """Persist the full list of accounts to the config file.

    Args:
        accounts: List of Account objects to save.
    """
    _write_raw([asdict(a) for a in accounts])


def _write_raw(accounts: list[dict]) -> None:
    """Write raw account dicts to disk."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"accounts": accounts}, f, indent=2)


def add_account(name: str, secret: str) -> Account:
    """Create and persist a new TOTP account.

    Args:
        name: Display name for the account.
        secret: Base32-encoded TOTP secret key.

    Returns:
        The newly created Account.
    """
    accounts = load_accounts()
    new_account = Account(id=str(uuid.uuid4()), name=name, secret=secret)
    accounts.append(new_account)
    save_accounts(accounts)
    return new_account


def delete_account(account_id: str) -> None:
    """Remove an account by its ID.

    Args:
        account_id: The unique ID of the account to remove.
                    No-op if the ID does not exist.
    """
    accounts = [a for a in load_accounts() if a.id != account_id]
    save_accounts(accounts)


def rename_account(account_id: str, new_name: str) -> None:
    """Rename an account by its ID.

    Args:
        account_id: The unique ID of the account to rename.
        new_name: The new display name.
    """
    accounts = load_accounts()
    for account in accounts:
        if account.id == account_id:
            account.name = new_name
            break
    save_accounts(accounts)
