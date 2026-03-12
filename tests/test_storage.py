"""Tests for totp_authenticator.storage module."""

import json
import os

from totp_authenticator.storage import load_secret, save_secret


class TestStorage:
    """Tests for save_secret() and load_secret()."""

    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        """Saved secret should be retrievable via load_secret."""
        config_file = tmp_path / ".totp_config.json"
        monkeypatch.setattr("totp_authenticator.storage.CONFIG_FILE", str(config_file))

        save_secret("JBSWY3DPEHPK3PXP")
        assert load_secret() == "JBSWY3DPEHPK3PXP"

    def test_load_missing_file_returns_empty(self, tmp_path, monkeypatch):
        """load_secret should return empty string if config doesn't exist."""
        config_file = tmp_path / "nonexistent.json"
        monkeypatch.setattr("totp_authenticator.storage.CONFIG_FILE", str(config_file))

        assert load_secret() == ""

    def test_load_corrupted_file_returns_empty(self, tmp_path, monkeypatch):
        """load_secret should handle corrupted JSON gracefully."""
        config_file = tmp_path / ".totp_config.json"
        config_file.write_text("NOT VALID JSON{{{", encoding="utf-8")
        monkeypatch.setattr("totp_authenticator.storage.CONFIG_FILE", str(config_file))

        assert load_secret() == ""

    def test_load_missing_key_returns_empty(self, tmp_path, monkeypatch):
        """load_secret should return empty if JSON has no 'secret' key."""
        config_file = tmp_path / ".totp_config.json"
        config_file.write_text('{"other_key": "value"}', encoding="utf-8")
        monkeypatch.setattr("totp_authenticator.storage.CONFIG_FILE", str(config_file))

        assert load_secret() == ""

    def test_save_overwrites_existing(self, tmp_path, monkeypatch):
        """Saving a new secret should overwrite the previous one."""
        config_file = tmp_path / ".totp_config.json"
        monkeypatch.setattr("totp_authenticator.storage.CONFIG_FILE", str(config_file))

        save_secret("FIRST_SECRET")
        save_secret("SECOND_SECRET")
        assert load_secret() == "SECOND_SECRET"

    def test_config_file_is_valid_json(self, tmp_path, monkeypatch):
        """The saved config file should be valid JSON."""
        config_file = tmp_path / ".totp_config.json"
        monkeypatch.setattr("totp_authenticator.storage.CONFIG_FILE", str(config_file))

        save_secret("TESTSECRET")
        data = json.loads(config_file.read_text(encoding="utf-8"))
        assert data == {"secret": "TESTSECRET"}
