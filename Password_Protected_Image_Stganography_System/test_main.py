import unittest
from unittest.mock import patch
from main import main

class TestMain(unittest.TestCase):

    @patch('main.start_gui')
    @patch('builtins.input', side_effect=['1', '3'])
    @patch('builtins.print')
    def test_gui_mode(self, mock_print, mock_input, mock_start_gui):
        with self.assertRaises(SystemExit):
            main()
        mock_start_gui.assert_called_once()
        mock_print.assert_any_call("👋 Exiting. Goodbye!")

    @patch('main.start_cli')
    @patch('builtins.input', side_effect=['2', '3'])
    @patch('builtins.print')
    def test_cli_mode(self, mock_print, mock_input, mock_start_cli):
        with self.assertRaises(SystemExit):
            main()
        mock_start_cli.assert_called_once()
        mock_print.assert_any_call("👋 Exiting. Goodbye!")

    @patch('builtins.input', side_effect=['3'])
    @patch('builtins.print')
    def test_exit_option(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        mock_print.assert_called_with("👋 Exiting. Goodbye!")

    @patch('builtins.input', side_effect=['invalid', '3'])
    @patch('builtins.print')
    def test_invalid_choice(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        mock_print.assert_any_call("❌ Invalid choice! Please enter 1, 2, or 3.")
        mock_print.assert_any_call("👋 Exiting. Goodbye!")

if __name__ == '__main__':
    unittest.main()

