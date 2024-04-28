import os
from datetime import datetime


class Singleton(type):
    """Singleton metaclass"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InvalidDecimalError(ValueError):
    """Raised when the decimal input is not a valid integer or is outside the supported range (1-3999)."""
    pass


class RomanNumeralOutOfRangeError(ValueError):
    """Raised when the Roman numeral input represents a value outside the supported range (1-3999)."""
    pass


class NumberFactory:
    """Factory class for creating Number objects"""

    @staticmethod
    def create_number(value):
        """
        Factory method to create a Number object based on the input value.

        Args:
            value (str or int): The input value to create the Number object from.

        Returns:
            Number: A new Number object (either DecimalNumber or RomanNumber).

        Raises:
            ValueError: If the input value is not a valid Roman numeral or decimal number.
        """
        if any(char.isdigit() for char in value) and any(char.isalpha() for char in value):
            raise ValueError("Invalid input. Please enter a valid Roman numeral or decimal number.")

        try:
            # Check if the input is a decimal number
            decimal_value = int(value)
            if decimal_value < 1 or decimal_value > 3999:
                raise InvalidDecimalError(f"Decimal value {value} is outside the supported range (1-3999).")
            return DecimalNumber(decimal_value)
        except ValueError:
            # Assume the input is a Roman numeral
            try:
                roman_num = RomanNumber(value.upper())
                if roman_num.convert()[0] < 1 or roman_num.convert()[0] > 3999:
                    raise RomanNumeralOutOfRangeError(f"Roman numeral {value} represents a value outside the supported range (1-3999).")
                return roman_num
            except (KeyError, ValueError):
                raise ValueError("Invalid input. Please enter a valid Roman numeral or decimal number.")


class Number:
    """Abstract base class for numbers"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def convert(self):
        """Abstract method to convert the number"""
        raise NotImplementedError("convert method must be implemented in subclasses")


class DecimalNumber(Number):
    """Class representing a decimal number"""

    def convert(self):
        """Converts the decimal number to a Roman numeral"""
        decimal_to_roman = {
            1: 'I', 4: 'IV', 5: 'V', 9: 'IX',
            10: 'X', 40: 'XL', 50: 'L', 90: 'XC',
            100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
        }
        roman_num = ''
        decimal_num = self.value
        for value, symbol in sorted(decimal_to_roman.items(), reverse=True):
            while decimal_num >= value:
                roman_num += symbol
                decimal_num -= value
        return RomanNumber(roman_num)


class RomanNumber(Number):
    ROMAN_NUMERAL_RULES = [
        ("Repeats", "ILLEGAL NUMBER DETECTED. A numeral cannot be repeated more than three times. (IIII is illegal)"),
        ("Subtractives", "ILLEGAL NUMBER DETECTED. Only I, X, and C can be used as subtractives."),
        ("Skips", "ILLEGAL NUMBER DETECTED. Only one numeral can be skipped when subtracting (IX is valid, but IC is not)."),
        ("VLD", "ILLEGAL NUMBER DETECTED. The letters V, L, and D cannot be repeated."),
    ]

    def convert(self):
        roman_to_decimal = {
            'I': 1, 'IV': 4, 'V': 5, 'IX': 9,
            'X': 10, 'XL': 40, 'L': 50, 'XC': 90,
            'C': 100, 'CD': 400, 'D': 500, 'CM': 900, 'M': 1000
        }
        decimal_sum = 0
        prev_value = 0

        roman = str(self.value)  # Store string version for analysis
        violated_rules = []

        for char in roman[::-1]:
            value = roman_to_decimal[char]
            if value < prev_value:
                decimal_sum -= value
            else:
                decimal_sum += value
            prev_value = value

        # Rule violation checks
        last_char = None
        repeat_count = 0

        for i, char in enumerate(roman):
            value = roman_to_decimal[char]

            if char == last_char:
                repeat_count += 1

                # Repeats rule
                if repeat_count > 3:
                    violated_rules.append(self.ROMAN_NUMERAL_RULES[0])

            else:
                repeat_count = 1
                last_char = char

            # Subtractives rules
            if i < len(roman) - 1 and value < roman_to_decimal[roman[i + 1]]:
                if char not in 'IXC':
                    violated_rules.append(self.ROMAN_NUMERAL_RULES[1])

            # Skips rule
            if i < len(roman) - 1 and value < roman_to_decimal[roman[i + 1]] and roman_to_decimal[roman[i + 1]] / value > 10:
                violated_rules.append(self.ROMAN_NUMERAL_RULES[2])

            # VLD rule
            if char in 'VLD':
                if repeat_count > 1:
                    violated_rules.append(self.ROMAN_NUMERAL_RULES[3])

        return decimal_sum, violated_rules


class NumberConverter:
    """Class responsible for converting numbers"""

    def convert(self, number):
        """Converts the given number to its corresponding representation"""
        return number.convert()


class DataLogger(metaclass=Singleton):
    """Class responsible for logging data to files"""

    def __init__(self, log_file="istorija.txt", data_file="duomenys.txt"):
        self.log_file = log_file
        self.data_file = data_file
        self.validate_and_initialize_datafile()

    def validate_and_initialize_datafile(self):
        """Checks if duomenys.txt has the required structure. Initializes if needed."""
        try:
            with open(self.data_file, "r") as duomenys_file:
                lines = duomenys_file.readlines()
        except FileNotFoundError:
            self.initialize_datafile()
            return

        if len(lines) != 4:
            self.initialize_datafile()

    def initialize_datafile(self):
        """Creates the data file if it doesn't exist or overwrites with initial data."""
        with open(self.data_file, "w") as duomenys_file:
            duomenys_file.write("Number of times code was initiated: 1\n")
            duomenys_file.write("Number of requests: 0\n")
            duomenys_file.write("Number of Roman to decimal conversions: 0\n")
            duomenys_file.write("Number of decimal to Roman conversions: 0\n")

    def log_data(self, log_message, conversion_type=None):
        """Logs data to files and updates statistics in the data file"""
        # Handle potential 'None' or empty value for log_message
        if log_message is None:  # Check for None
            # Get the current date and time
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Application started at {timestamp}"
        elif not log_message:  # Check for empty string
            log_message = "Application started"  # or any other default message

        with open(self.log_file, "a") as istorija_file:
            istorija_file.write(log_message + "\n")

        try:
            with open(self.data_file, "r") as duomenys_file:
                lines = duomenys_file.readlines()
        except FileNotFoundError:
            self.initialize_datafile()
            return

        # Regardless of conversion_type, increment the initiated counter
        num_times_initiated = int(lines[0].split(":")[1].strip()) + 1

        # Update other statistics based on conversion_type (if provided)
        num_requests = int(lines[1].split(":")[1].strip())
        num_roman_to_decimal = int(lines[2].split(":")[1].strip())
        num_decimal_to_roman = int(lines[3].split(":")[1].strip())

        if conversion_type:
            num_requests += 1
            if conversion_type == "roman_to_decimal":
                num_roman_to_decimal += 1
            elif conversion_type == "decimal_to_roman":
                num_decimal_to_roman += 1

        with open(self.data_file, "w") as duomenys_file:
            duomenys_file.write(f"Number of times code was initiated: {num_times_initiated}\n")
            duomenys_file.write(f"Number of requests: {num_requests}\n")
            duomenys_file.write(f"Number of Roman to decimal conversions: {num_roman_to_decimal}\n")
            duomenys_file.write(f"Number of decimal to Roman conversions: {num_decimal_to_roman}\n")

    def print_istorija(self):
        """Prints the contents of the log file (istorija.txt)."""
        try:
            with open(self.log_file, "r") as istorija_file:
                print("Contents of istorija.txt:")
                print(istorija_file.read())
                print()
        except FileNotFoundError:
            pass


class UserInterface:
    def __init__(self):
        self.converter = NumberConverter()
        self.logger = DataLogger()  # Default file names used

    def run(self):
        self.logger.log_data(log_message=None)
        self.logger.print_istorija()

        while True:
            user_input = input("Enter a Roman numeral or a decimal number (or 'duom' to print duomenys.txt, 'logs' to print istorija.txt, 'clear' to clear logs, 'exit' to quit): ").lower()
            if user_input == "exit":
                break
            elif user_input == "duom":
                self.print_duomenys()
            elif user_input == "clear":  # New functionality!
                self.clear_logs()
            elif user_input == "logs":  # New functionality!
                self.logger.print_istorija()
            else:
                self.handle_user_input(user_input)

    def clear_logs(self):
        """Clears the contents of both files and reinitializes duomenys.txt"""
        for file_path in [self.logger.log_file, self.logger.data_file]:
            try:
                open(file_path, 'w').close()
                print(f"Cleared: {file_path}")

                # Reinitialize duomenys.txt if necessary
                if file_path == self.logger.data_file:
                    self.logger.initialize_datafile()

            except FileNotFoundError:
                print(f"Warning: File not found: {file_path}")

    def print_duomenys(self):
        data_file_path = os.path.join(os.getcwd(), "duomenys.txt")  # Relative to current directory
        try:
            with open(data_file_path, "r") as duomenys_file:
                print("Contents of duomenys.txt:")
                print(duomenys_file.read())
                print()
        except FileNotFoundError:
            print("Error: duomenys.txt not found.")

    def handle_user_input(self, user_input):
        """Handles the user input and performs the conversion"""
        try:
            number = NumberFactory.create_number(user_input)
            converted_result = self.converter.convert(number)

            conversion_type = "decimal_to_roman" if isinstance(number, DecimalNumber) else "roman_to_decimal"

            if isinstance(converted_result, tuple):
                decimal_value, violated_rules = converted_result
                rule_violations = ", ".join([rule[1] for rule in violated_rules])
                log_message = f"{user_input.upper()} is a {number.__class__.__name__}, and its converted value is {decimal_value}"
                if rule_violations:
                    log_message += f", {rule_violations}"
                self.logger.log_data(log_message, conversion_type)
                print(log_message)
            else:
                self.logger.log_data(f"{user_input} is a {number.__class__.__name__}, and its converted value is {converted_result}", conversion_type)
                print(f"{user_input} is a {number.__class__.__name__}, and its converted value is {converted_result}")

        except ValueError as e:
            self.logger.log_data(f"Invalid input: {user_input}", "error")
            print(e)


# Run the user interface
UserInterface().run()
