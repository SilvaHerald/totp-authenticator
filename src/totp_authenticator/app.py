"""TOTP Authenticator UI — tkinter-based desktop window."""

import tkinter as tk
from tkinter import messagebox

import pyperclip

from totp_authenticator.core import get_code, get_remaining_seconds, validate_secret
from totp_authenticator.storage import load_secret, save_secret


class TOTPApp:
    """Main application window for the TOTP Authenticator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("TOTP Authenticator")
        self.root.geometry("340x220")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.root.attributes("-topmost", True)

        self.secret = load_secret()
        self.running = True

        self._build_ui()
        self._update_loop()

    def _build_ui(self) -> None:
        """Construct the application widget tree."""
        # Title
        tk.Label(
            self.root,
            text="🔐 TOTP Authenticator",
            font=("Segoe UI", 13, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4",
        ).pack(pady=(18, 4))

        # Code display
        self.code_var = tk.StringVar(value="------")
        self.code_label = tk.Label(
            self.root,
            textvariable=self.code_var,
            font=("Courier New", 36, "bold"),
            bg="#1e1e2e",
            fg="#a6e3a1",
        )
        self.code_label.pack(pady=4)

        # Timer bar
        self.timer_var = tk.StringVar(value="")
        tk.Label(
            self.root,
            textvariable=self.timer_var,
            font=("Segoe UI", 9),
            bg="#1e1e2e",
            fg="#6c7086",
        ).pack()

        # Copy button
        self.copy_btn = tk.Button(
            self.root,
            text="📋 Copy Code",
            font=("Segoe UI", 10, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=self._copy_code,
        )
        self.copy_btn.pack(pady=10)

        # Secret key input (small, at bottom)
        bottom = tk.Frame(self.root, bg="#1e1e2e")
        bottom.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(
            bottom,
            text="Secret Key:",
            font=("Segoe UI", 8),
            bg="#1e1e2e",
            fg="#6c7086",
        ).pack(side="left")

        self.secret_entry = tk.Entry(
            bottom,
            font=("Segoe UI", 8),
            width=22,
            bg="#313244",
            fg="#cdd6f4",
            relief="flat",
            insertbackground="white",
            show="*",
        )
        self.secret_entry.pack(side="left", padx=6)
        self.secret_entry.insert(0, self.secret)

        tk.Button(
            bottom,
            text="Save",
            font=("Segoe UI", 8),
            bg="#585b70",
            fg="#cdd6f4",
            relief="flat",
            padx=6,
            cursor="hand2",
            command=self._save_key,
        ).pack(side="left")

    def _copy_code(self) -> None:
        """Copy the current TOTP code to the system clipboard."""
        code = get_code(self.secret)
        if code:
            pyperclip.copy(code)
            self.copy_btn.config(text="✅ Copied!", bg="#a6e3a1")
            self.root.after(
                1500,
                lambda: self.copy_btn.config(text="📋 Copy Code", bg="#89b4fa"),
            )
        else:
            messagebox.showerror(
                "Error",
                "No valid Secret Key!\nPlease enter your Secret Key below.",
            )

    def _save_key(self) -> None:
        """Validate and persist the secret key from the input field."""
        new_secret = self.secret_entry.get().strip()
        if not new_secret:
            messagebox.showwarning("Warning", "Secret Key cannot be empty!")
            return

        if validate_secret(new_secret):
            self.secret = new_secret
            save_secret(new_secret)
            messagebox.showinfo("OK", "Secret Key saved!")
        else:
            messagebox.showerror(
                "Error",
                "Invalid Secret Key!\nPlease check your key and try again.",
            )

    def _update_loop(self) -> None:
        """Refresh the displayed code and countdown timer every second."""
        if not self.running:
            return

        code = get_code(self.secret)
        if code:
            self.code_var.set(code)
            remaining = get_remaining_seconds()
            bar_filled = remaining // 2
            bar_empty = 15 - bar_filled
            self.timer_var.set(f"{remaining}s  {'█' * bar_filled}{'░' * bar_empty}")

            # Turn red when code is about to expire
            if remaining <= 5:
                self.code_label.config(fg="#f38ba8")
            else:
                self.code_label.config(fg="#a6e3a1")
        else:
            self.code_var.set("------")
            self.timer_var.set("Enter Secret Key below")

        self.root.after(1000, self._update_loop)
