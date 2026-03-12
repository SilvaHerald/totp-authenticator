# Roadmap

This document outlines the planned features and improvements for TOTP Authenticator.
Items are loosely prioritized within each milestone.

> **Note:** This roadmap is aspirational. Timelines are not guaranteed.
> Have a feature idea? [Open an issue](https://github.com/SilvaHerald/totp-authenticator/issues)!

---

## ✅ v0.1.0 — Initial Release (Current)

- [x] Auto-refreshing 6-digit TOTP codes (30-second window)
- [x] Countdown timer with color change when expiring
- [x] One-click copy to clipboard
- [x] Persistent secret key storage
- [x] Always-on-top window mode
- [x] Unit tests for core logic and storage
- [x] CI/CD pipeline with GitHub Actions
- [x] Automated release builds with Nuitka

---

## 🔭 v0.2.0 — Multi-Account Support

- [ ] Store and manage multiple TOTP accounts
- [ ] Display a list of accounts with their live codes
- [ ] Add / rename / delete accounts
- [ ] Import accounts via QR code scan or `otpauth://` URI

---

## 🎨 v0.3.0 — UX Polish

- [ ] System tray integration (minimize to tray)
- [ ] Light / dark theme toggle
- [ ] Custom window size and position persistence
- [ ] Keyboard shortcuts (copy code, switch account)

---

## 🔒 v0.4.0 — Security Hardening

- [ ] Optional PIN / password lock on app open
- [ ] Encrypt stored secrets at rest
- [ ] Auto-lock after inactivity timeout

---

## 📦 v1.0.0 — Stable Release

- [ ] Full multi-account support stabilized
- [ ] Comprehensive documentation and user guide
- [ ] Signed Windows installer (`.exe`)
- [ ] macOS build support

---

## 💡 Ideas Backlog (No ETA)

These are ideas that have been raised but not yet scheduled:

- Backup & restore accounts (encrypted export)
- Browser extension integration
- TOTP token search / filter
- Localization / i18n support
