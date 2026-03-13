# TOTP Authenticator — Agent Rules

## Project Overview

**TOTP Authenticator** is a lightweight, fully offline Windows desktop app written in Python that generates 2FA codes (TOTP) without needing the user's phone.

- **GitHub**: https://github.com/SilvaHerald/totp-authenticator
- **Current version**: `0.1.0` (Beta)
- **License**: MIT
- **Target platform**: Windows (Python 3.10+)
- **Entry point command**: `totp-auth`

---

## Tech Stack

| Layer         | Technology                        |
|---------------|-----------------------------------|
| Language      | Python 3.10+                      |
| UI            | `tkinter` (standard library)      |
| TOTP logic    | `pyotp >= 2.9`                    |
| Clipboard     | `pyperclip >= 1.8`                |
| Build tool    | `nuitka >= 2.0` (produces `.exe`) |
| Packaging     | `setuptools` + `setuptools-scm`   |
| Linter        | `ruff >= 0.4`                     |
| Test runner   | `pytest >= 7.0`                   |
| CI/CD         | GitHub Actions                    |

---

## Project Structure

```
totp-authenticator/
├── src/totp_authenticator/
│   ├── __init__.py     # Package metadata & version
│   ├── main.py         # Entry point — calls app.run()
│   ├── app.py          # tkinter UI (TotpApp class)
│   ├── core.py         # Pure TOTP logic (no UI deps)
│   └── storage.py      # JSON config persistence (~/.totp_config.json)
├── tests/
│   ├── test_core.py    # Tests for core.py
│   └── test_storage.py # Tests for storage.py
├── .github/
│   ├── workflows/ci.yml       # Lint + test on push/PR
│   ├── workflows/release.yml  # Build .exe & publish on Git tag
│   ├── ISSUE_TEMPLATE/        # Bug report & feature request templates
│   └── pull_request_template.md
├── assets/             # demo.gif and other static assets
├── pyproject.toml      # Project config, deps, tool settings
├── CHANGELOG.md        # Keep a Changelog format (Unreleased → versioned)
├── CONTRIBUTING.md     # Dev setup & contribution guide
├── ROADMAP.md          # Feature milestones (v0.1 → v1.0)
├── SECURITY.md         # Vulnerability reporting policy
└── SECURITY_PRIVACY.md # Privacy & data handling policy
```

---

## Module Responsibilities

### `core.py` — Pure Logic (no UI)
- `get_code(secret: str) -> str | None` — returns current 6-digit TOTP code
- `validate_secret(secret: str) -> bool` — checks if secret is valid Base32
- `get_remaining_seconds() -> int` — seconds until current code expires (1–30)

> **Rule**: Keep `core.py` UI-free. All TOTP computation must stay here.

### `storage.py` — Persistence
- Config stored at `~/.totp_config.json` as `{"secret": "<value>"}`
- `load_secret() -> str` — reads saved secret (returns `""` if missing/corrupt)
- `save_secret(secret: str) -> None` — persists secret to disk

> **Rule**: Storage is local-only. No network calls anywhere in the project.

### `app.py` — UI Layer (tkinter)
- Contains the `TotpApp` class with the main tkinter window
- Calls `core.py` functions for logic, `storage.py` for persistence
- Handles: auto-refresh timer, countdown color changes, copy-to-clipboard

### `main.py` — Entry Point
- Minimal — just bootstraps `tkinter.Tk()` and starts `TotpApp`

---

## Development Workflow

### Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

### Daily Commands
```bash
pytest tests/ -v          # Run tests
ruff check src/           # Lint
ruff check src/ --fix     # Auto-fix lint issues
```

### Build Executable
```bash
python -m nuitka --onedir --windows-console-mode=disable src/totp_authenticator/main.py
```

### Release Process
1. Update `CHANGELOG.md` (move `[Unreleased]` entries under a new version section)
2. Bump version in `pyproject.toml`
3. Commit: `git commit -m "chore: release vX.Y.Z"`
4. Tag: `git tag vX.Y.Z && git push --tags`
5. GitHub Actions `release.yml` auto-builds and publishes the release

---

## Code Style & Conventions

- Follow **PEP 8** and use **type hints** on all function signatures
- Add **docstrings** for all public functions and classes
- **Line length**: 100 characters max (enforced by ruff)
- **Imports**: sorted automatically by ruff
- **Commit messages**: follow [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`
- **Branch naming**: `feature/your-feature-name`, `fix/bug-description`

---

## Testing Guidelines

- Tests live in `tests/` and mirror the module they test (`test_core.py`, `test_storage.py`)
- Every new function in `core.py` or `storage.py` **must** have corresponding tests
- UI code in `app.py` does not require automated tests (manual verification is acceptable)

---

## CI/CD Pipelines

| Workflow      | Trigger                  | Actions                                  |
|---------------|--------------------------|------------------------------------------|
| `ci.yml`      | Push / PR to `main`      | `ruff check` + `pytest`                  |
| `release.yml` | Push of tag `v*.*.*`     | Nuitka build → GitHub Release upload     |

---

## Roadmap Summary

| Milestone | Focus                                      |
|-----------|--------------------------------------------|
| v0.1.0 ✅ | Single-account MVP, CI/CD, build pipeline  |
| v0.2.0    | Multi-account support, QR code import      |
| v0.3.0    | UX polish (tray, themes, shortcuts)        |
| v0.4.0    | Security hardening (PIN, encrypted secrets)|
| v1.0.0    | Stable release, signed installer, macOS    |

---

## Key Design Principles

1. **Offline-first**: Zero network calls. Secrets never leave the machine.
2. **Separation of concerns**: Logic in `core.py`, UI in `app.py`, storage in `storage.py`.
3. **Security-conscious**: Secrets stored locally in plaintext JSON (encryption planned for v0.4).
4. **Minimal dependencies**: Only `pyotp` and `pyperclip` as runtime deps.
5. **Open source friendly**: MIT license, conventional commits, GitHub issue templates.

---

## Important Files to Check Before Making Changes

| File                  | When to read it                                      |
|-----------------------|------------------------------------------------------|
| `CHANGELOG.md`        | Before any release; add entries under `[Unreleased]` |
| `ROADMAP.md`          | Before adding features; check if already planned     |
| `CONTRIBUTING.md`     | Before PRs; ensure process is followed               |
| `pyproject.toml`      | When adding dependencies or changing build config    |
| `.github/workflows/`  | When changing CI triggers or build steps             |
