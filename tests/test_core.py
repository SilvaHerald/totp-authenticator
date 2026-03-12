"""Tests for totp_authenticator.core module."""

import pyotp

from totp_authenticator.core import get_code, get_remaining_seconds, validate_secret

# A known valid Base32 secret for testing
VALID_SECRET = pyotp.random_base32()
INVALID_SECRET = "NOT-A-VALID-BASE32!!!"


class TestGetCode:
    """Tests for get_code()."""

    def test_valid_secret_returns_6_digit_string(self):
        code = get_code(VALID_SECRET)
        assert code is not None
        assert len(code) == 6
        assert code.isdigit()

    def test_empty_secret_returns_none(self):
        assert get_code("") is None

    def test_whitespace_only_returns_none(self):
        assert get_code("   ") is None

    def test_invalid_secret_returns_none(self):
        assert get_code(INVALID_SECRET) is None

    def test_secret_with_spaces_still_works(self):
        # Secrets sometimes contain spaces for readability
        spaced = " ".join([VALID_SECRET[i:i+4] for i in range(0, len(VALID_SECRET), 4)])
        code = get_code(spaced)
        assert code is not None
        assert len(code) == 6

    def test_code_matches_pyotp_directly(self):
        expected = pyotp.TOTP(VALID_SECRET).now()
        actual = get_code(VALID_SECRET)
        assert actual == expected


class TestValidateSecret:
    """Tests for validate_secret()."""

    def test_valid_secret(self):
        assert validate_secret(VALID_SECRET) is True

    def test_invalid_secret(self):
        assert validate_secret(INVALID_SECRET) is False

    def test_empty_secret(self):
        assert validate_secret("") is False


class TestGetRemainingSeconds:
    """Tests for get_remaining_seconds()."""

    def test_result_within_range(self):
        remaining = get_remaining_seconds()
        assert 1 <= remaining <= 30

    def test_returns_integer(self):
        assert isinstance(get_remaining_seconds(), int)
