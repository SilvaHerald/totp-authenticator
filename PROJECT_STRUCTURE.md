# 📦 Project Structure

```text
totp-authenticator/
├── src/totp_authenticator/
│   ├── __init__.py     # Package metadata
│   ├── main.py         # Entry point
│   ├── app.py          # UI (tkinter)
│   ├── core.py         # TOTP logic
│   └── storage.py      # Config persistence
├── tests/
│   ├── test_core.py    # Core logic tests
│   └── test_storage.py # Storage tests
├── .github/workflows/
│   ├── ci.yml          # Lint + test on push/PR
│   └── release.yml     # Build & publish on tag
└── pyproject.toml      # Project config
```
