from tkinter import *
from tkinter import ttk, messagebox
from auth import register_user, login_user, reset_password, is_valid_password
from encoder_decoder import encode_message_gui, decode_message_gui

class Stegno:
    def __init__(self, root):
        self.root, self.login_attempts = root, 3
        self.root.title("Login/Register")
        self.root.geometry("800x600")
        self.root.configure(bg="#808e75")
        self.apply_styles()
        self.login()

    def apply_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10)
        style.configure("TLabel", font=("Helvetica", 18, "bold"), background="#808e75", foreground="white")

    def register(self):
        self.clear_window("Register")
        user_entry, pass_entry, confirm_entry = self.create_form(include_confirm=True)
        ttk.Button(self.root, text="Register", command=lambda: self.process_register(user_entry, pass_entry, confirm_entry)).pack(pady=15)
        ttk.Button(self.root, text="Back to Login", command=self.login).pack(pady=10)

    def process_register(self, user_entry, pass_entry, confirm_entry):
        username, password, confirm_password = user_entry.get(), pass_entry.get(), confirm_entry.get()
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        is_valid, msg = is_valid_password(password)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return

        success, msg = register_user(username, password, confirm_password)
        if success:
            messagebox.showinfo("Success", msg)
            self.login()
        else:
            messagebox.showerror("Error", msg)

    def login(self):
        self.clear_window("Login")
        user_entry, pass_entry = self.create_form()
        ttk.Button(self.root, text="Login", command=lambda: self.process_login(user_entry, pass_entry)).pack(pady=15)
        ttk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        ttk.Button(self.root, text="Reset Password", command=self.reset_password).pack(pady=10)

    def process_login(self, user_entry, pass_entry):
        username, password = user_entry.get(), pass_entry.get()
        success, msg = login_user(username, password)
        if success:
            self.login_attempts = 3
            self.main_screen()
        else:
            self.login_attempts -= 1
            messagebox.showerror("Error", f"{msg} Attempts left: {self.login_attempts}")
            if self.login_attempts == 0:
                self.root.destroy()

    def reset_password(self):
        self.clear_window("Reset Password")
        user_entry, new_pass_entry, confirm_pass_entry = self.create_form(include_confirm=True)
        ttk.Button(self.root, text="Reset", command=lambda: self.process_reset(user_entry, new_pass_entry, confirm_pass_entry)).pack(pady=15)
        ttk.Button(self.root, text="Back to Login", command=self.login).pack(pady=10)

    def process_reset(self, user_entry, new_pass_entry, confirm_pass_entry):
        username, new_password, confirm_password = user_entry.get(), new_pass_entry.get(), confirm_pass_entry.get()
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        is_valid, msg = is_valid_password(new_password)
        if not is_valid:
            messagebox.showerror("Error", msg)
            return

        success, msg = reset_password(username, new_password, confirm_password)
        if success:
            messagebox.showinfo("Success", msg)
            self.login()
        else:
            messagebox.showerror("Error", msg)

    def main_screen(self):
        self.clear_window("Image Steganography")
        ttk.Button(self.root, text="Encode", command=encode_message_gui).pack(pady=20)
        ttk.Button(self.root, text="Decode", command=decode_message_gui).pack(pady=20)

    def clear_window(self, title):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title(title)
        self.root.geometry("800x600")

    def create_form(self, include_confirm=False):
        Label(self.root, text="Username:", font=("Helvetica", 18, "bold"), bg="#808e75", fg="white").pack(pady=10)
        user_entry = ttk.Entry(self.root)
        user_entry.pack(pady=10)
        Label(self.root, text="Password:", font=("Helvetica", 18, "bold"), bg="#808e75", fg="white").pack(pady=10)
        pass_entry = ttk.Entry(self.root, show="*")
        pass_entry.pack(pady=10)
        if include_confirm:
            Label(self.root, text="Confirm Password:", font=("Helvetica", 18, "bold"), bg="#808e75", fg="white").pack(pady=10)
            confirm_entry = ttk.Entry(self.root, show="*")
            confirm_entry.pack(pady=10)
            return user_entry, pass_entry, confirm_entry
        return user_entry, pass_entry

def start_gui():
    root = Tk()
    Stegno(root)
    root.mainloop()
