"""Entry point for the TOTP Authenticator application."""

import threading
import tkinter as tk

import pystray
from pystray import MenuItem

from totp_authenticator.app import TOTPApp
from totp_authenticator.icon import create_default_icon


def main() -> None:
    """Launch the TOTP Authenticator window and system tray icon."""
    root = tk.Tk()
    TOTPApp(root)

    # Prepare the tray icon
    icon_image = create_default_icon(64, 64)

    def on_quit(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Fully exit the application."""
        icon.stop()
        # Schedule the destroy in the main tkinter thread
        root.after(0, root.destroy)

    def on_show(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Show the hidden window."""
        root.after(0, root.deiconify)

    tray_icon = pystray.Icon(
        "totp_auth",
        icon_image,
        "TOTP Authenticator",
        menu=pystray.Menu(
            MenuItem("Show", on_show, default=True),
            MenuItem("Quit", on_quit),
        ),
    )

    def withdraw_window() -> None:
        """Hide the window instead of destroying it."""
        root.withdraw()

    # Override the standard Close [X] button behavior
    root.protocol("WM_DELETE_WINDOW", withdraw_window)

    # Start the pystray icon in a separate background thread
    # so it doesn't block the tkinter mainloop
    threading.Thread(target=tray_icon.run, daemon=True).start()

    # Start the UI
    root.mainloop()


if __name__ == "__main__":
    main()
