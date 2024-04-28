import unittest
from unittest.mock import patch
from io import StringIO
from coursework import UserInterface


class TestUserInputs(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_decimal_input(self, mock_stdout):
        ui = UserInterface()

        # Test valid decimal input
        ui.handle_user_input("123")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "123 is a DecimalNumber, and its converted value is CXXIII")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # Test decimal input at boundary cases
        ui.handle_user_input("1")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "1 is a DecimalNumber, and its converted value is I")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        ui.handle_user_input("3999")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "3999 is a DecimalNumber, and its converted value is MMMCMXCIX")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # Test invalid decimal input
        ui.handle_user_input("4000")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Invalid input. Please enter a valid Roman numeral or decimal number.")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        ui.handle_user_input("-10")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Invalid input. Please enter a valid Roman numeral or decimal number.")

    @patch('sys.stdout', new_callable=StringIO)
    def test_roman_input(self, mock_stdout):
        ui = UserInterface()

        # Test valid Roman input
        ui.handle_user_input("CXXIII")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "CXXIII is a RomanNumber, and its converted value is 123")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # Test Roman input at boundary cases
        ui.handle_user_input("I")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "I is a RomanNumber, and its converted value is 1")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        ui.handle_user_input("MMMCMXCIX")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "MMMCMXCIX is a RomanNumber, and its converted value is 3999")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # Test invalid Roman input
        ui.handle_user_input("MMMM")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Invalid input. Please enter a valid Roman numeral or decimal number.")
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        ui.handle_user_input("IC")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "IC is a RomanNumber, and its converted value is 99, ILLEGAL NUMBER DETECTED. Only one numeral can be skipped when subtracting (IX is valid, but IC is not).")


if __name__ == '__main__':
    unittest.main()
