import unittest
import sqlite3
from auth import register_user, login_user, get_db_connection

class TestIntegrationAuth(unittest.TestCase):
    def setUp(self):
        # Set up a clean test database
        self.conn = get_db_connection()
        self.conn.execute("DROP TABLE IF EXISTS users")
        self.conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        self.conn.commit()

    def tearDown(self):
        # Clean up database after each test
        self.conn.close()

    def test_register_and_login_user(self):
        # Test successful registration and login
        username = "testuser"
        password = "testpass"

        # Register user
        registration_result = register_user(username, password)
        self.assertTrue(registration_result, "User registration failed")

        # Try logging in
        login_result = login_user(username, password)
        self.assertTrue(login_result, "User login failed")

    def test_login_with_invalid_credentials(self):
        # Ensure login fails for unregistered user
        login_result = login_user("invaliduser", "wrongpass")
        self.assertFalse(login_result, "Login should fail for invalid credentials")

    def test_register_duplicate_user(self):
        # Register a user and attempt to register the same user again
        username = "testuser"
        password = "testpass"

        register_user(username, password)  # First registration
        duplicate_registration = register_user(username, password)  # Second registration

        self.assertFalse(duplicate_registration, "Duplicate user registration should fail")

if __name__ == "__main__":
    unittest.main()
