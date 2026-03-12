# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
