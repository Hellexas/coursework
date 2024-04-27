import os

class Singleton(type):
    """Singleton metaclass"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


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
        try:
            # Check if the input is a decimal number
            decimal_value = int(value)
            return DecimalNumber(decimal_value)
        except ValueError:
            # Assume the input is a Roman numeral
            try:
                return RomanNumber(value.upper())
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
        ("Repeatable Subtractives", "ILLEGAL NUMBER DETECTED. Only one I, X, and C can be subtracted from two larger numerals."),
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
        subtractive_used = {'I': False, 'X': False, 'C': False}  # For tracking repeatable subtractives
        larger_value_seen = False  # For repeatable subtractives check

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
                subtractive_used = {'I': False, 'X': False, 'C': False}  # Reset subtractive_used on new numeral

            # Subtractives rules
            if i < len(roman) - 1:
                next_value = roman_to_decimal[roman[i + 1]]
                if value < next_value:
                    if char in 'IXC':
                        if subtractive_used[char]:
                            violated_rules.append(self.ROMAN_NUMERAL_RULES[2])  # Repeatable Subtractives rule
                        subtractive_used[char] = True
                        if next_value / value > 10:
                            violated_rules.append(self.ROMAN_NUMERAL_RULES[3])  # Skips rule
                    else:
                        violated_rules.append(self.ROMAN_NUMERAL_RULES[1])  # Subtractives rule
                    if larger_value_seen:
                        violated_rules.append(self.ROMAN_NUMERAL_RULES[2])  # Repeatable Subtractives rule

            # VLD rule and tracking for repeatable subtractives
            if char in 'VLD':
                if repeat_count > 1:
                    violated_rules.append(self.ROMAN_NUMERAL_RULES[4])
            if value > prev_value:
                larger_value_seen = True

            prev_value = value  # Update previous value

        return decimal_sum, violated_rules

class NumberConverter:
    """Class responsible for converting numbers"""

    def convert(self, number):
        """Converts the given number to its corresponding representation"""
        return number.convert()

class DataLogger(metaclass=Singleton):
    def __init__(self):
        # Change file paths to a suitable default, e.g., same folder as the script
        self.history_file = "istorija.txt"
        self.data_file = "duomenys.txt"
        self.create_files()

    def create_files(self):
        for file in [self.history_file, self.data_file]:
            if not os.path.exists(file):  # Check if files exist
                open(file, "w").close()  # Create if not

    def log_data(self, log_message, conversion_type):
        """Logs the conversion data to files"""
        with open("../../Downloads/istorija.txt", "a") as istorija_file:
            istorija_file.write(log_message + "\n")

        with open("../../Downloads/duomenys.txt", "r") as duomenys_file:
            lines = duomenys_file.readlines()

        num_requests = int(lines[1].split(":")[1].strip())
        num_roman_to_decimal = int(lines[2].split(":")[1].strip())
        num_decimal_to_roman = int(lines[3].split(":")[1].strip())

        num_requests += 1
        if conversion_type == "roman_to_decimal":
            num_roman_to_decimal += 1
        elif conversion_type == "decimal_to_roman":
            num_decimal_to_roman += 1

        with open("../../Downloads/duomenys.txt", "w") as duomenys_file:
            duomenys_file.write(f"Number of times code was initiated: {int(lines[0].split(':')[1].strip()) + 1}\n")
            duomenys_file.write(f"Number of requests: {num_requests}\n")
            duomenys_file.write(f"Number of Roman to decimal conversions: {num_roman_to_decimal}\n")
            duomenys_file.write(f"Number of decimal to Roman conversions: {num_decimal_to_roman}\n")

    def print_istorija(self):
        """Prints the contents of istorija.txt on code launch if the file exists"""
        try:
            with open("../../Downloads/istorija.txt", "r") as istorija_file:
                print("Contents of istorija.txt:")
                print(istorija_file.read())
                print()
        except FileNotFoundError:
            pass


class UserInterface:
    """Class responsible for handling user interactions"""

    def __init__(self):
        self.converter = NumberConverter()
        self.logger = DataLogger()

    def run(self):
        """Runs the user interface loop"""
        self.logger.print_istorija()
        while True:
            user_input = input("Enter a Roman numeral or a decimal number (or 'duom' to print duomenys.txt, 'exit' to quit): ").lower()
            if user_input == "exit":
                break
            elif user_input == "duom":
                with open("../../Downloads/duomenys.txt", "r") as duomenys_file:
                    print("Contents of duomenys.txt:")
                    print(duomenys_file.read())
                    print()
            else:
                self.handle_user_input(user_input)

    def handle_user_input(self, user_input):
        """Handles the user input and performs the conversion"""
        try:
            number = NumberFactory.create_number(user_input)
            converted_result = self.converter.convert(number)

            conversion_type = "decimal_to_roman" if isinstance(number, DecimalNumber) else "roman_to_decimal"

            if isinstance(converted_result, tuple):
                decimal_value, violated_rules = converted_result
                rule_violations = ", ".join([rule[1] for rule in violated_rules])
                log_message = f"{user_input} is a {number.__class__.__name__}, and its converted value is {decimal_value}"
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
