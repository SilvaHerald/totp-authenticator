# 🔒 Security & Privacy

This application is **completely offline**. It:

- Makes **zero network requests** — no telemetry, no analytics, no updates
- Stores secrets **locally only** in `~/.totp_config.json`
- Uses the industry-standard [pyotp](https://github.com/pyauth/pyotp) library for TOTP generation
- Is fully open-source — audit the code yourself
