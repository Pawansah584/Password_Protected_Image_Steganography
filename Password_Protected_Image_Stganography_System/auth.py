import sqlite3
import bcrypt
import re

# Database Setup
def get_db_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    return conn

# Password Validation
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

# Hash & Verify Passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

# Register & Login Functions
def register_user(username, password):
    if not is_valid_password(password):
        print("Password must be at least 8 characters long and include lowercase, uppercase, digit, and special symbol.")
        return False

    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit(), conn.close()
        return True
    except sqlite3.IntegrityError:
        print("Username already exists.")
        return False

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user and check_password(user[0], password)
