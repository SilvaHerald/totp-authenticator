# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.4.0] - 2026-03-XX
### Added
- **Master Password**: You can now lock the app using a master password.
- **Encrypt at Rest**: Local secrets configuration file is now encrypted using AES-128-CBC (Fernet) if a password is set.
- **Auto-lock**: The application will automatically lock after a configurable period of inactivity.

## [0.3.0] - 2026-03-14

### Added
- System tray integration — minimize app to tray icon instead of closing
- Light and Dark themes — toggleable straight from the UI
- Window state persistence — app remembers its previous screen position between launches
- Global keyboard shortcuts: `Up`/`Down`/`Tab` for navigation, `Enter`/`Ctrl-c` to copy, `Ctrl-a` to add, etc.
- Seamless, zero-downtime config migration to support new preferences schema

### Changed
- Config file now contains `accounts` and `settings` objects  

## [0.2.0] - 2026-03-13

### Added
- Multi-account support — store and manage multiple TOTP accounts
- Account list sidebar with live codes for each account
- Add, rename, and delete accounts via dedicated dialogs
- Automatic migration from v0.1 single-secret config to multi-account format

### Changed
- Redesigned UI with two-panel layout (sidebar + main OTP view)
- Window resized to 620×400 to accommodate account list
- `storage.py` API replaced: `load_secret`/`save_secret` → `load_accounts`/`save_accounts` + `add_account`/`delete_account`/`rename_account`
- Config file format updated: `{"secret": "..."}` → `{"accounts": [...]}`

## [0.1.0] - 2026-03-12

### Added
- Auto-refreshing 6-digit TOTP codes (30-second window)
- Countdown timer with color change when code is expiring
- One-click copy to clipboard
- Persistent secret key storage
- Always-on-top window mode
- Unit tests for core logic and storage
- CI/CD pipeline with GitHub Actions
- Automated release builds with Nuitka

### Security
- Fully offline operation — zero network requests
- Local-only secret storage in user home directory
