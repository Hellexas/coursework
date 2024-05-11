import unittest
from coursework import *  # Import all classes and functions from coursework.py

class CourseworkTest(unittest.TestCase):

    def test_invalid_input(self):
        """Test if ValueError is raised for invalid inputs (decimals, Romans, mixed)"""
        with self.assertRaises(ValueError):
            NumberFactory.create_number("IIII")  # Invalid Roman
        with self.assertRaises(ValueError):
            NumberFactory.create_number("IM")  # Skips
        with self.assertRaises(ValueError):
            NumberFactory.create_number("IXIXI")  # Nonsense
        with self.assertRaises(ValueError):
            NumberFactory.create_number("MMMM")  # Out of range

    def setUp(self):
        self.converter = NumberConverter()
        self.logger = DataLogger()

    def test_decimal_to_roman_conversion(self):
        """Test various decimal to Roman numeral conversions"""
        test_cases = [(1, 'I'), (9, 'IX'), (49, 'XLIX'), (444, 'CDXLIV'), (999, 'CMXCIX'), (3999, 'MMMCMXCIX')]
        for decimal, expected_roman in test_cases:
            decimal_num = DecimalNumber(decimal)
            converted_roman = self.converter.convert(decimal_num)
            self.assertEqual(str(converted_roman), expected_roman)

    def test_roman_to_decimal_conversion(self):
        """Test various Roman numeral to decimal conversions"""
        test_cases = [('I', 1), ('IX', 9), ('XLIX', 49), ('CDXLIV', 444), ('CMXCIX', 999), ('MMMCMXCIX', 3999)]
        for roman, expected_decimal in test_cases:
            roman_num = RomanNumber(roman)
            converted_decimal = self.converter.convert(roman_num)
            self.assertEqual(converted_decimal, expected_decimal)

    def test_invalid_roman_numeral_conversion(self):
        """Test conversions with invalid Roman numerals"""
        invalid_romans = ['IIII', 'IM', 'VX', 'MMMM', 'IXIX']  # Examples of invalid numerals
        for roman in invalid_romans:
            with self.assertRaises(ValueError):
                RomanNumber(roman).convert()

    def test_data_logger_singleton(self):
        """Ensure DataLogger is a singleton"""
        logger1 = DataLogger()
        logger2 = DataLogger()
        self.assertIs(logger1, logger2)

    def test_data_logger_logging(self):
        """Test logging of conversions and errors"""
        self.logger.log_data("Test log message", "roman_to_decimal")
        with open(self.logger.log_file, "r") as log_file:
            last_log_entry = log_file.readlines()[-1].strip()
        self.assertIn("Test log message", last_log_entry)

    def test_data_logger_datafile(self):
        """Ensure the data file is created and updated correctly. Data file must be cleared prior to running this test"""
        self.logger.log_data("Test log message", "decimal_to_roman")
        with open(self.logger.data_file, "r") as data_file:
            num_decimal_to_roman = int(data_file.readlines()[3].split(":")[1].strip())
        self.assertEqual(num_decimal_to_roman, 1)


if __name__ == '__main__':
    unittest.main()
