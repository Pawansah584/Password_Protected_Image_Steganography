import sqlite3
import bcrypt
import re

# Database Setup
def get_db_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)"""
    )
    return conn

# Password Validation
def is_valid_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[a-z]', password):
        return False, "Password must include a lowercase letter."
    if not re.search(r'[A-Z]', password):
        return False, "Password must include an uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must include a digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must include a special symbol."
    return True, ""

# Hash & Verify Passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

# Registration (includes password confirmation)
def register_user(username, password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match."

    is_valid, msg = is_valid_password(password)
    if not is_valid:
        return False, msg

    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

# Login
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."
    if check_password(user[0], password):
        return True, "Login successful!"
    return False, "Incorrect password."

# Password Reset
def reset_password(username, new_password, confirm_password):
    if new_password != confirm_password:
        return False, "Passwords do not match."

    is_valid, msg = is_valid_password(new_password)
    if not is_valid:
        return False, msg

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False, "Username not found."
    
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (hash_password(new_password), username)
    )
    conn.commit()
    conn.close()
    return True, "Password reset successful!"
