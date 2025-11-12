import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from models import Credential
import auth
import vault

class ShieldBytesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shield-BYTES Password Manager")
        self.key = None
        self.credentials = []
        self.setup_auth_screen()
    
    def setup_auth_screen(self):
        self.clear_root()
        tk.Label(self.root, text="Welcome to Shield-BYTES", font=("Arial", 16)).pack(pady=10)
        if not auth.master_exists():
            tk.Label(self.root, text="Set a master password:").pack()
            self.master_entry = tk.Entry(self.root, show='*')
            self.master_entry.pack()
            tk.Button(self.root, text="Save", command=self.set_master).pack(pady=10)
        else:
            tk.Label(self.root, text="Enter master password:").pack()
            self.master_entry = tk.Entry(self.root, show='*')
            self.master_entry.pack()
            tk.Button(self.root, text="Login", command=self.login_master).pack(pady=10)

    def set_master(self):
        pwd = self.master_entry.get()
        if len(pwd) < 6:
            messagebox.showerror("Error", "Password too short. Use 6+ characters.")
            return
        auth.set_master_password(pwd)
        messagebox.showinfo("Success", "Master password set.")
        self.setup_auth_screen()

    def login_master(self):
        pwd = self.master_entry.get()
        if not auth.verify_master_password(pwd):
            messagebox.showerror("Error", "Incorrect master password.")
            return
        self.key = auth.get_vault_key(pwd)
        try:
            self.credentials = vault.load_vault(self.key)
        except ValueError:
            messagebox.showerror("Error", "Vault is corrupted or wrong password.")
            return
        self.setup_vault_screen()

    def setup_vault_screen(self):
        self.clear_root()
        tk.Label(self.root, text="Shield-BYTES Vault", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=('Site', 'Username', 'Password'), show='headings')
        for col in ('Site', 'Username', 'Password'):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, expand=True, fill='both')
        self.refresh_tree()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add", command=self.add_cred_dialog).pack(side='left', padx=4)
        tk.Button(btn_frame, text="Edit", command=self.edit_cred_dialog).pack(side='left', padx=4)
        tk.Button(btn_frame, text="Delete", command=self.delete_cred).pack(side='left', padx=4)
        tk.Button(btn_frame, text="Logout", command=self.setup_auth_screen).pack(side='left', padx=4)
        tk.Button(btn_frame, text="Save", command=self.save_vault_data).pack(side='left', padx=4)

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, cred in enumerate(self.credentials):
            self.tree.insert('', 'end', iid=str(idx), values=(cred.site, cred.username, cred.password))

    def add_cred_dialog(self):
        dlg = CredDialog(self.root, "Add Credential")
        if dlg.result:
            c = Credential(*dlg.result)
            self.credentials.append(c)
            self.refresh_tree()

    def edit_cred_dialog(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select an entry to edit.")
            return
        idx = int(sel[0])
        cred = self.credentials[idx]
        dlg = CredDialog(self.root, "Edit Credential", cred)
        if dlg.result:
            self.credentials[idx] = Credential(*dlg.result)
            self.refresh_tree()

    def delete_cred(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select an entry to delete.")
            return
        idx = int(sel[0])
        del self.credentials[idx]
        self.refresh_tree()

    def save_vault_data(self):
        if self.key:
            vault.save_vault(self.credentials, self.key)
            messagebox.showinfo("Saved", "Vault saved successfully.")

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

class CredDialog(simpledialog.Dialog):
    def __init__(self, parent, title, cred=None):
        self.cred = cred
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Site/App Name:").grid(row=0, column=0)
        tk.Label(master, text="Username:").grid(row=1, column=0)
        tk.Label(master, text="Password:").grid(row=2, column=0)
        self.site = tk.Entry(master)
        self.username = tk.Entry(master)
        self.password = tk.Entry(master)
        self.site.grid(row=0, column=1)
        self.username.grid(row=1, column=1)
        self.password.grid(row=2, column=1)
        if self.cred:
            self.site.insert(0, self.cred.site)
            self.username.insert(0, self.cred.username)
            self.password.insert(0, self.cred.password)
        return self.site

    def apply(self):
        self.result = (
            self.site.get(),
            self.username.get(),
            self.password.get()
        )