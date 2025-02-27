import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from gui import Stegno

class TestStegno(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.stegno = Stegno(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('gui.register_user', return_value=True)
    @patch('tkinter.messagebox.showinfo')
    def test_successful_registration(self, mock_showinfo, mock_register_user):
        self.stegno.process_register(MagicMock(get=MagicMock(return_value='test_user')), 
                                     MagicMock(get=MagicMock(return_value='test_pass')))
        mock_register_user.assert_called_once_with('test_user', 'test_pass')
        mock_showinfo.assert_called_once_with("Success", "Registration successful! Please login.")

    @patch('gui.register_user', return_value=False)
    @patch('tkinter.messagebox.showerror')
    def test_failed_registration(self, mock_showerror, mock_register_user):
        self.stegno.process_register(MagicMock(get=MagicMock(return_value='existing_user')), 
                                     MagicMock(get=MagicMock(return_value='pass')))
        mock_register_user.assert_called_once_with('existing_user', 'pass')
        mock_showerror.assert_called_once_with("Error", "Username already exists!")

    @patch('gui.login_user', return_value=True)
    def test_successful_login(self, mock_login_user):
        self.stegno.process_login(MagicMock(get=MagicMock(return_value='valid_user')), 
                                  MagicMock(get=MagicMock(return_value='valid_pass')))
        mock_login_user.assert_called_once_with('valid_user', 'valid_pass')
        self.assertEqual(self.stegno.login_attempts, 3)

    @patch('gui.login_user', return_value=False)
    @patch('tkinter.messagebox.showerror')
    def test_failed_login(self, mock_showerror, mock_login_user):
        self.stegno.process_login(MagicMock(get=MagicMock(return_value='invalid_user')), 
                                  MagicMock(get=MagicMock(return_value='wrong_pass')))
        mock_login_user.assert_called_once_with('invalid_user', 'wrong_pass')
        self.assertEqual(self.stegno.login_attempts, 2)
        mock_showerror.assert_called_with("Error", "Invalid credentials. Attempts left: 2")

    @patch('gui.login_user', side_effect=[False, False, False])
    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.Tk.destroy')
    def test_login_attempts_exceeded(self, mock_destroy, mock_showerror, mock_login_user):
        for _ in range(2):  # First two failed attempts
            self.stegno.process_login(MagicMock(get=MagicMock(return_value='invalid_user')), 
                                  MagicMock(get=MagicMock(return_value='wrong_pass')))

        # Final (third) failed attempt — should trigger window close
        self.stegno.process_login(MagicMock(get=MagicMock(return_value='invalid_user')), 
                              MagicMock(get=MagicMock(return_value='wrong_pass')))

        mock_login_user.assert_called_with('invalid_user', 'wrong_pass')
        self.assertEqual(self.stegno.login_attempts, 0)  # Ensure attempts hit 0
        mock_showerror.assert_called_with("Error", "Invalid credentials. Attempts left: 0")
        mock_destroy.assert_called_once()  # Ensure window closes


if __name__ == '__main__':
    unittest.main()
