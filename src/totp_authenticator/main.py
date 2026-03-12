"""Entry point for the TOTP Authenticator application."""

import tkinter as tk

from totp_authenticator.app import TOTPApp


def main() -> None:
    """Launch the TOTP Authenticator window."""
    root = tk.Tk()
    TOTPApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
