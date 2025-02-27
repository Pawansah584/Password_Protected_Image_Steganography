import unittest
from unittest.mock import patch, MagicMock
from encoder_decoder import encode_message, decode_message, store_password, get_stored_password
from PIL import Image
import hashlib
import sqlite3

class TestEncoderDecoder(unittest.TestCase):

    @patch('encoder_decoder.Image.open')
    @patch('encoder_decoder.simpledialog.askstring')
    @patch('encoder_decoder.filedialog.asksaveasfilename')
    @patch('encoder_decoder.messagebox.showinfo')
    def test_encode_message_success(self, mock_showinfo, mock_save, mock_password, mock_image_open):
        mock_image = MagicMock()
        mock_image.size = (100, 100)
        mock_image.width = 100
        mock_image.height = 100
        mock_image_open.return_value = mock_image
        mock_save.return_value = "encoded_image.png"
        mock_password.return_value = "testpass"

        mock_pixels = MagicMock()
        mock_pixels.__getitem__.return_value = [0, 0, 0]
        mock_image.load.return_value = mock_pixels

        message = "hidden msg"
        encode_message("test_image.png", message, is_gui=True)

        mock_image.save.assert_called_with("encoded_image.png")
        mock_showinfo.assert_called_with("Success", "Message encoded successfully!")

    @patch('encoder_decoder.Image.open')
    @patch('encoder_decoder.simpledialog.askstring')
    @patch('encoder_decoder.messagebox.showerror')
    def test_decode_message_failure_incorrect_password(self, mock_showerror, mock_password, mock_image_open):
        mock_image = MagicMock()
        mock_image.size = (100, 100)
        mock_pixels = MagicMock()
        mock_pixels.__getitem__.return_value = [0, 0, 0]
        mock_image.load.return_value = mock_pixels
        mock_image_open.return_value = mock_image
        mock_password.return_value = "wrongpass"

        with patch('encoder_decoder.get_stored_password', return_value=hashlib.sha256("testpass".encode()).hexdigest()):
            decode_message("encoded_image.png", is_gui=True)
            mock_showerror.assert_called_with("Error", "Incorrect password!")

    @patch('encoder_decoder.Image.open')
    @patch('encoder_decoder.simpledialog.askstring')
    @patch('encoder_decoder.messagebox.showerror')
    def test_decode_message_failure_file_not_found(self, mock_showerror, mock_password, mock_image_open):
        mock_image_open.side_effect = FileNotFoundError("File not found")
        mock_password.return_value = "testpass"

        with patch('encoder_decoder.get_stored_password', return_value=None):
            try:
                decode_message("nonexistent_image.png", is_gui=True)
            except FileNotFoundError:
                mock_showerror.assert_called_with("Error", "File not found!")

    @patch('encoder_decoder.sqlite3.connect')
    def test_store_password(self, mock_db):
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn

        store_password("test_image.png", "testpass")
        mock_conn.execute.assert_any_call("CREATE TABLE IF NOT EXISTS messages (file_path TEXT UNIQUE, password_hash TEXT)")
        mock_conn.execute.assert_any_call("INSERT OR REPLACE INTO messages VALUES (?, ?)", ("test_image.png", hashlib.sha256("testpass".encode()).hexdigest()))

    @patch('encoder_decoder.sqlite3.connect')
    def test_get_stored_password(self, mock_db):
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = (hashlib.sha256("testpass".encode()).hexdigest(),)
        mock_db.return_value = mock_conn

        result = get_stored_password("test_image.png")
        self.assertEqual(result, hashlib.sha256("testpass".encode()).hexdigest())

if __name__ == "__main__":
    unittest.main()
