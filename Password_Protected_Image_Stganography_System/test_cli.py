import unittest
from unittest.mock import patch
from cli import start_cli

class TestCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '3'])
    @patch('cli.encode_message_cli')
    @patch('builtins.print')
    def test_encode_message_option(self, mock_print, mock_encode, mock_input):
        start_cli()
        mock_encode.assert_called_once()
        mock_print.assert_called_with('👋 Exiting CLI mode. Goodbye!')

    @patch('builtins.input', side_effect=['2', '3'])
    @patch('cli.decode_message_cli')
    @patch('builtins.print')
    def test_decode_message_option(self, mock_print, mock_decode, mock_input):
        start_cli()
        mock_decode.assert_called_once()
        mock_print.assert_called_with('👋 Exiting CLI mode. Goodbye!')

    @patch('builtins.input', side_effect=['invalid', '3'])
    @patch('builtins.print')
    def test_invalid_choice(self, mock_print, mock_input):
        start_cli()
        mock_print.assert_any_call('❌ Invalid choice! Please enter 1, 2, or 3.')
        mock_print.assert_called_with('👋 Exiting CLI mode. Goodbye!')

    @patch('builtins.input', side_effect=['3'])
    @patch('builtins.print')
    def test_exit_option(self, mock_print, mock_input):
        start_cli()
        mock_print.assert_called_with('👋 Exiting CLI mode. Goodbye!')

if __name__ == "__main__":
    unittest.main()
