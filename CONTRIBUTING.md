# Contributing to TOTP Authenticator

Thank you for your interest in contributing! This guide will help you get started.

## 🛠️ Development Setup

1. **Fork & Clone** the repository:
   ```bash
   git clone https://github.com/SilvaHerald/totp-authenticator.git
   cd totp-authenticator
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dev dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests** to make sure everything works:
   ```bash
   pytest tests/ -v
   ```

## 📝 Making Changes

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write your code** following the project structure:
   - `src/totp_authenticator/core.py` — Pure logic (no UI)
   - `src/totp_authenticator/storage.py` — Config persistence
   - `src/totp_authenticator/app.py` — UI components

3. **Add tests** for new functionality in the `tests/` directory.

4. **Run lint and tests** before committing:
   ```bash
   ruff check src/
   pytest tests/ -v
   ```

## 💬 Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add multi-account support
fix: correct countdown timer off-by-one error
docs: update README with new installation method
test: add edge case tests for invalid secrets
refactor: extract timer logic into separate function
```

## 🔀 Pull Request Process

1. Ensure all tests pass and there are no lint errors.
2. Update the `README.md` if your change affects usage.
3. Add an entry to `CHANGELOG.md` under `[Unreleased]`.
4. Submit a PR against the `main` branch.
5. Wait for review — a maintainer will provide feedback.

## 🐛 Reporting Bugs

Use the [Bug Report template](https://github.com/SilvaHerald/totp-authenticator/issues/new?template=bug_report.md) on GitHub Issues. Include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Windows version and Python version

## 💡 Suggesting Features

Use the [Feature Request template](https://github.com/SilvaHerald/totp-authenticator/issues/new?template=feature_request.md) on GitHub Issues.

## 📋 Code Style

- Follow **PEP 8** conventions.
- Use **type hints** for function signatures.
- Add **docstrings** for public functions and classes.
- Keep imports sorted (enforced by `ruff`).
- Line length: **100 characters max**.

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
