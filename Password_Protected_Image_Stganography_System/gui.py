from tkinter import *
from tkinter import ttk, messagebox
from auth import register_user, login_user
from encoder_decoder import encode_message_gui, decode_message_gui

class Stegno:
    def __init__(self, root):
        self.root, self.login_attempts = root, 3
        self.root.title("Login/Register"), self.root.geometry("800x600"), self.root.configure(bg="#808e75")
        self.apply_styles(), self.login()

    def apply_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14), padding=10)
        style.configure("TLabel", font=("Helvetica", 18, "bold"), background="#808e75", foreground="white")

    def register(self):
        self.clear_window("Register")
        user_entry, pass_entry = self.create_form()
        ttk.Button(self.root, text="Register", command=lambda: self.process_register(user_entry, pass_entry)).pack(pady=15)
        ttk.Button(self.root, text="Back to Login", command=self.login).pack(pady=10)

    def process_register(self, user_entry, pass_entry):
        if register_user(user_entry.get(), pass_entry.get()):
            messagebox.showinfo("Success", "Registration successful! Please login."); self.login()
        else:
            messagebox.showerror("Error", "Username already exists!")

    def login(self):
        self.clear_window("Login")
        user_entry, pass_entry = self.create_form()
        ttk.Button(self.root, text="Login", command=lambda: self.process_login(user_entry, pass_entry)).pack(pady=15)
        ttk.Button(self.root, text="Register", command=self.register).pack(pady=10)

    def process_login(self, user_entry, pass_entry):
        if login_user(user_entry.get(), pass_entry.get()):
            self.login_attempts = 3
            self.main_screen()
        else:
            self.login_attempts -= 1
            messagebox.showerror("Error", f"Invalid credentials. Attempts left: {self.login_attempts}")
            if self.login_attempts == 0:
               self.root.destroy()

    def main_screen(self):
        self.clear_window("Image Steganography")
        ttk.Button(self.root, text="Encode", command=encode_message_gui).pack(pady=20)
        ttk.Button(self.root, text="Decode", command=decode_message_gui).pack(pady=20)

    def clear_window(self, title):
        for widget in self.root.winfo_children(): widget.destroy()
        self.root.title(title), self.root.geometry("800x600")

    def create_form(self):
        Label(self.root, text="Username:", font=("Helvetica", 18, "bold"), bg="#808e75", fg="white").pack(pady=10)
        user_entry = ttk.Entry(self.root); user_entry.pack(pady=10)
        Label(self.root, text="Password:", font=("Helvetica", 18, "bold"), bg="#808e75", fg="white").pack(pady=10)
        pass_entry = ttk.Entry(self.root, show="*"); pass_entry.pack(pady=10)
        return user_entry, pass_entry

def start_gui():
    root = Tk(); Stegno(root); root.mainloop()

