from PIL import Image
import hashlib
import sqlite3
import os
import pwinput  # ✅ Import pwinput for password masking in CLI
from tkinter import filedialog, simpledialog, messagebox, Toplevel, Text, Scrollbar, Button

# ---------------------- Database Functions ---------------------- #
def get_db_connection():
    """Returns a database connection & ensures the table exists."""
    conn = sqlite3.connect("encoded_messages.db", check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS messages (file_path TEXT UNIQUE, password_hash TEXT)")
    return conn

def store_password(file_path, password):
    """Hashes and stores the password for an image."""
    conn = get_db_connection()
    conn.execute("INSERT OR REPLACE INTO messages VALUES (?, ?)", (file_path, hashlib.sha256(password.encode()).hexdigest()))
    conn.commit(), conn.close()

def get_stored_password(file_path):
    """Retrieves stored password hash for an image."""
    conn = get_db_connection()
    result = conn.execute("SELECT password_hash FROM messages WHERE file_path = ?", (file_path,)).fetchone()
    conn.close()
    return result[0] if result else None

# ---------------------- Encoding & Decoding Functions ---------------------- #
def encode_message(file_path, message, is_gui=True):
    """Encodes a hidden message into an image."""
    try:
        img = Image.open(file_path)
        max_bits = img.width * img.height

        message += "#####STOP#####"
        encoded_data = ''.join(format(ord(i), '08b') for i in message)
        if len(encoded_data) > max_bits:
            if is_gui:
                messagebox.showerror("Error", f"Message too long! Max capacity: {max_bits // 8} characters.")
            else:
                print(f"❌ Error: Message too long! Max capacity: {max_bits // 8} characters.")
            return

        password = (
            simpledialog.askstring("Password", "Set a password:", show="*") 
            if is_gui else pwinput.pwinput("Set a password: ", mask="*")  # ✅ Password now shows *
        )
        if not password:
            if is_gui:
                messagebox.showerror("Error", "Password is required!")
            else:
                print("❌ Error: Password is required!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png") if is_gui else input("Enter save path: ").strip()
        if not save_path:
            return

        store_password(save_path, password)
        pixels, data_index = img.load(), 0

        for y in range(img.height):
            for x in range(img.width):
                if data_index < len(encoded_data):
                    pixel = list(pixels[x, y])
                    pixel[0] = pixel[0] & ~1 | int(encoded_data[data_index])
                    pixels[x, y], data_index = tuple(pixel), data_index + 1
                else:
                    break

        img.save(save_path)
        if is_gui:
            messagebox.showinfo("Success", "Message encoded successfully!")
        else:
            print("✅ Message encoded successfully!")
    except Exception as e:
        if is_gui:
            messagebox.showerror("Error", f"Encoding Error: {str(e)}")
        else:
            print(f"❌ Encoding Error: {str(e)}")

def decode_message(file_path, is_gui=True):
    """Decodes a hidden message from an image."""
    try:
        stored_password = get_stored_password(file_path)
        if not stored_password:
            if is_gui:
                messagebox.showerror("Error", "No password found for this image.")
            else:
                print("❌ Error: No password found for this image.")
            return

        password = (
            simpledialog.askstring("Password", "Enter password:", show="*") 
            if is_gui else pwinput.pwinput("Enter password: ", mask="*")  # ✅ Password now shows *
        )
        if hashlib.sha256(password.encode()).hexdigest() != stored_password:
            if is_gui:
                messagebox.showerror("Error", "Incorrect password!")
            else:
                print("❌ Error: Incorrect password!")
            return

        if not os.path.exists(file_path):
            if is_gui:
                messagebox.showerror("Error", "File not found!")
            else:
                print("❌ Error: File not found!")
            return

        try:
            img = Image.open(file_path)
        except Exception as e:
            if is_gui:
                messagebox.showerror("Error", f"Cannot open image: {str(e)}")
            else:
                print(f"❌ Error: Cannot open image: {str(e)}")
            return

        binary_data = "".join(str(img.load()[x, y][0] & 1) for y in range(img.height) for x in range(img.width))
        hidden_message = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)).split("#####STOP#####")[0]

        if not hidden_message.strip():
            if is_gui:
                messagebox.showerror("Error", "No hidden message found!")
            else:
                print("❌ Error: No hidden message found!")
            return

        show_large_hidden_message(hidden_message) if is_gui else print("\n🔐 Hidden Message:\n" + hidden_message)
    except Exception as e:
        if is_gui:
            messagebox.showerror("Error", f"Decoding Error: {str(e)}")
        else:
            print(f"❌ Decoding Error: {str(e)}")

# ---------------------- CLI Encoding & Decoding ---------------------- #
def encode_message_cli():
    """CLI function to encode a message into an image."""
    file_path = input("Enter the path to the image file: ").strip()
    if os.path.exists(file_path):
        message = input("Enter the message to hide: ").strip()
        encode_message(file_path, message, is_gui=False)

def decode_message_cli():
    """CLI function to decode a message from an image."""
    file_path = input("Enter encoded image path: ").strip()
    if os.path.exists(file_path):
        decode_message(file_path, is_gui=False)

# ---------------------- GUI Encoding & Decoding ---------------------- #
def encode_message_gui():
    """GUI function to encode a message into an image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    encode_message(file_path, get_large_message_input())

def decode_message_gui():
    """GUI function to decode a message from an image."""
    file_path = filedialog.askopenfilename(
        title="Select an Encoded Image",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    decode_message(file_path)
# ---------------------- GUI Large Input & Output Windows ---------------------- #
def get_large_message_input():
    """Opens a large input window for entering a long message."""
    global entered_message
    entered_message = ""

    input_window = Toplevel()
    input_window.title("Enter Message")
    input_window.geometry("1000x600")

    text_area = Text(input_window, wrap="word", font=("Helvetica", 14))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    def submit():
        global entered_message
        entered_message = text_area.get("1.0", "end-1c").strip()
        input_window.destroy()

    Button(input_window, text="Submit", font=("Helvetica", 14), command=submit).pack(pady=10)
    input_window.wait_window()
    return entered_message

def show_large_hidden_message(hidden_message):
    """Opens a large window to display the decoded hidden message."""
    output_window = Toplevel()
    output_window.title("Hidden Message")
    output_window.geometry("1000x600")

    text_area = Text(output_window, wrap="word", font=("Helvetica", 14))
    text_area.insert("1.0", hidden_message)
    text_area.config(state="disabled")  # Make the text area read-only
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    scrollbar = Scrollbar(output_window, command=text_area.yview)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)
    Button(output_window, text="Close", font=("Helvetica", 14), command=output_window.destroy).pack(pady=10)
