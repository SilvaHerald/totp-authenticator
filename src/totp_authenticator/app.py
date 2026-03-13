"""TOTP Authenticator UI — tkinter-based desktop window (v0.2.0 multi-account)."""

import tkinter as tk
from tkinter import messagebox, simpledialog

import pyperclip

from totp_authenticator.core import get_code, get_remaining_seconds, validate_secret
from totp_authenticator.storage import (
    Account,
    add_account,
    delete_account,
    load_accounts,
    rename_account,
)

# ── Colour palette (Catppuccin Mocha) ─────────────────────────────────────────
BG = "#1e1e2e"
BG_SIDEBAR = "#181825"
BG_ENTRY = "#313244"
FG = "#cdd6f4"
FG_DIM = "#6c7086"
FG_SELECTED = "#89b4fa"
GREEN = "#a6e3a1"
RED = "#f38ba8"
BLUE = "#89b4fa"
SURFACE = "#45475a"


class TOTPApp:
    """Main application window for the TOTP Authenticator (multi-account)."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("TOTP Authenticator")
        self.root.geometry("620x400")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)

        self._accounts: list[Account] = load_accounts()
        self._selected_id: str | None = (
            self._accounts[0].id if self._accounts else None
        )

        self._build_ui()
        self._refresh_sidebar()
        self._update_loop()

    # ── Build ──────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Construct the two-panel widget tree."""
        # ── Sidebar (left) ─────────────────────────────────────────────────────
        sidebar = tk.Frame(self.root, bg=BG_SIDEBAR, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="Accounts",
            font=("Segoe UI", 10, "bold"),
            bg=BG_SIDEBAR,
            fg=FG_DIM,
        ).pack(pady=(16, 6), padx=12, anchor="w")

        # Account listbox
        list_frame = tk.Frame(sidebar, bg=BG_SIDEBAR)
        list_frame.pack(fill="both", expand=True, padx=8)

        self.listbox = tk.Listbox(
            list_frame,
            bg=BG_SIDEBAR,
            fg=FG,
            selectbackground=BG_ENTRY,
            selectforeground=FG_SELECTED,
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
            cursor="hand2",
        )
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # Sidebar action buttons
        btn_bar = tk.Frame(sidebar, bg=BG_SIDEBAR)
        btn_bar.pack(fill="x", padx=8, pady=(6, 12))

        for text, cmd in [
            ("+ Add", self._open_add_dialog),
            ("Rename", self._open_rename_dialog),
            ("Delete", self._open_delete_dialog),
        ]:
            tk.Button(
                btn_bar,
                text=text,
                font=("Segoe UI", 9),
                bg=SURFACE,
                fg=FG,
                relief="flat",
                padx=8,
                pady=4,
                cursor="hand2",
                command=cmd,
            ).pack(side="left", padx=2)

        # ── Main panel (right) ─────────────────────────────────────────────────
        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Account name label
        self.account_name_var = tk.StringVar(value="")
        tk.Label(
            main,
            textvariable=self.account_name_var,
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=FG_DIM,
        ).pack(pady=(28, 0))

        # OTP code display
        self.code_var = tk.StringVar(value="------")
        self.code_label = tk.Label(
            main,
            textvariable=self.code_var,
            font=("Courier New", 42, "bold"),
            bg=BG,
            fg=GREEN,
        )
        self.code_label.pack(pady=(4, 0))

        # Countdown timer bar
        self.timer_var = tk.StringVar(value="")
        tk.Label(
            main,
            textvariable=self.timer_var,
            font=("Segoe UI", 9),
            bg=BG,
            fg=FG_DIM,
        ).pack()

        # Copy button
        self.copy_btn = tk.Button(
            main,
            text="📋  Copy Code",
            font=("Segoe UI", 11, "bold"),
            bg=BLUE,
            fg=BG,
            relief="flat",
            padx=24,
            pady=8,
            cursor="hand2",
            command=self._copy_code,
        )
        self.copy_btn.pack(pady=20)

        # Empty-state hint
        self.hint_var = tk.StringVar(value="")
        tk.Label(
            main,
            textvariable=self.hint_var,
            font=("Segoe UI", 9),
            bg=BG,
            fg=FG_DIM,
            wraplength=360,
            justify="center",
        ).pack()

    # ── Sidebar helpers ────────────────────────────────────────────────────────

    def _refresh_sidebar(self) -> None:
        """Rebuild the listbox from in-memory accounts list."""
        self.listbox.delete(0, "end")
        for account in self._accounts:
            self.listbox.insert("end", f"  {account.name}")

        # Re-select previously selected account
        if self._selected_id:
            idx = self._index_of(self._selected_id)
            if idx is not None:
                self.listbox.selection_set(idx)
                self.listbox.activate(idx)
            else:
                # Selected account was deleted; fall back to first
                self._selected_id = self._accounts[0].id if self._accounts else None
                if self._selected_id:
                    self.listbox.selection_set(0)

        self._refresh_main_panel()

    def _on_select(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        """Handle listbox selection change."""
        sel = self.listbox.curselection()
        if not sel:
            return
        self._selected_id = self._accounts[sel[0]].id
        self._refresh_main_panel()

    def _selected_account(self) -> Account | None:
        """Return the currently selected Account, or None."""
        if self._selected_id is None:
            return None
        idx = self._index_of(self._selected_id)
        return self._accounts[idx] if idx is not None else None

    def _index_of(self, account_id: str) -> int | None:
        """Return the list index of an account by id, or None."""
        for i, a in enumerate(self._accounts):
            if a.id == account_id:
                return i
        return None

    # ── Main panel helpers ─────────────────────────────────────────────────────

    def _refresh_main_panel(self) -> None:
        """Update main panel labels to reflect the selected account."""
        account = self._selected_account()
        if account:
            self.account_name_var.set(account.name)
            self.hint_var.set("")
            self.copy_btn.config(state="normal")
        else:
            self.account_name_var.set("")
            self.code_var.set("------")
            self.timer_var.set("")
            self.hint_var.set('Click "+ Add" to add your first account.')
            self.copy_btn.config(state="disabled")

    # ── Dialogs ────────────────────────────────────────────────────────────────

    def _open_add_dialog(self) -> None:
        """Open a dialog to add a new account."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Account")
        dialog.geometry("360x180")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.attributes("-topmost", True)

        for row, (label_text, _) in enumerate(
            [("Account Name:", ""), ("Secret Key:", "*")]
        ):
            tk.Label(
                dialog, text=label_text, font=("Segoe UI", 10), bg=BG, fg=FG
            ).grid(row=row, column=0, padx=16, pady=(18 if row == 0 else 8, 4), sticky="w")

        name_entry = tk.Entry(
            dialog, font=("Segoe UI", 10), bg=BG_ENTRY, fg=FG,
            relief="flat", insertbackground="white", width=28,
        )
        name_entry.grid(row=0, column=1, padx=(0, 16), pady=(18, 4))
        name_entry.focus_set()

        secret_entry = tk.Entry(
            dialog, font=("Segoe UI", 10), bg=BG_ENTRY, fg=FG,
            relief="flat", insertbackground="white", width=28, show="*",
        )
        secret_entry.grid(row=1, column=1, padx=(0, 16), pady=(0, 4))

        def _save() -> None:
            name = name_entry.get().strip()
            secret = secret_entry.get().strip().replace(" ", "")
            if not name:
                messagebox.showwarning("Warning", "Account name cannot be empty.", parent=dialog)
                return
            if not validate_secret(secret):
                messagebox.showerror(
                    "Error",
                    "Invalid Secret Key.\nPlease check and try again.",
                    parent=dialog,
                )
                return
            new_account = add_account(name, secret)
            self._accounts = load_accounts()
            self._selected_id = new_account.id
            self._refresh_sidebar()
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg=BG)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=14)
        tk.Button(
            btn_frame, text="Save", font=("Segoe UI", 10, "bold"),
            bg=BLUE, fg=BG, relief="flat", padx=20, pady=5,
            cursor="hand2", command=_save,
        ).pack(side="left", padx=6)
        tk.Button(
            btn_frame, text="Cancel", font=("Segoe UI", 10),
            bg=SURFACE, fg=FG, relief="flat", padx=12, pady=5,
            cursor="hand2", command=dialog.destroy,
        ).pack(side="left", padx=6)

        dialog.bind("<Return>", lambda _: _save())
        dialog.bind("<Escape>", lambda _: dialog.destroy())

    def _open_rename_dialog(self) -> None:
        """Open a simple dialog to rename the selected account."""
        account = self._selected_account()
        if not account:
            messagebox.showinfo("Info", "Please select an account first.")
            return
        new_name = simpledialog.askstring(
            "Rename Account",
            f'New name for "{account.name}":',
            initialvalue=account.name,
            parent=self.root,
        )
        if new_name and new_name.strip():
            rename_account(account.id, new_name.strip())
            self._accounts = load_accounts()
            self._refresh_sidebar()

    def _open_delete_dialog(self) -> None:
        """Ask for confirmation, then delete the selected account."""
        account = self._selected_account()
        if not account:
            messagebox.showinfo("Info", "Please select an account first.")
            return
        confirmed = messagebox.askyesno(
            "Delete Account",
            f'Delete "{account.name}"?\nThis cannot be undone.',
            icon="warning",
            parent=self.root,
        )
        if confirmed:
            delete_account(account.id)
            self._accounts = load_accounts()
            self._selected_id = self._accounts[0].id if self._accounts else None
            self._refresh_sidebar()

    # ── Copy & update loop ─────────────────────────────────────────────────────

    def _copy_code(self) -> None:
        """Copy the current OTP code for the selected account to clipboard."""
        account = self._selected_account()
        if not account:
            return
        code = get_code(account.secret)
        if code:
            pyperclip.copy(code)
            self.copy_btn.config(text="✅  Copied!", bg=GREEN)
            self.root.after(
                1500,
                lambda: self.copy_btn.config(text="📋  Copy Code", bg=BLUE),
            )
        else:
            messagebox.showerror(
                "Error",
                "Could not generate a code.\nThe secret key may be invalid.",
            )

    def _update_loop(self) -> None:
        """Refresh the OTP code and countdown timer every second."""
        account = self._selected_account()
        if account:
            code = get_code(account.secret)
            if code:
                self.code_var.set(code)
                remaining = get_remaining_seconds()
                bar_filled = remaining // 2
                bar_empty = 15 - bar_filled
                self.timer_var.set(f"{remaining}s  {'█' * bar_filled}{'░' * bar_empty}")
                self.code_label.config(fg=RED if remaining <= 5 else GREEN)
            else:
                self.code_var.set("INVALID")
                self.timer_var.set("Secret key is invalid")
                self.code_label.config(fg=RED)

        self.root.after(1000, self._update_loop)
