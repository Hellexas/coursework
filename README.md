# Coursework "Decimal and roman number converter"
Python coursework by Dovydas Bubulas EDiF-23/1


## Code Structure Overview

   ### Number Representation:
   Number (Abstract Base Class): Defines the core attributes and behavior of numbers, providing the template for subclasses.

   DecimalNumber: Represents numbers in decimal (base-10) format.

   RomanNumber: Represents numbers in Roman numeral format.

   ### Conversion and Logic:
   NumberConverter: Responsible for orchestrating the conversion process between number representations.

   NumberFactory: Uses the Factory Method pattern to create appropriate Number objects based on input (decimal or Roman).

   DataLogger: A Singleton for logging interactions and conversions.

   ### Error Handling: 
Custom exceptions are defined for invalid inputs and out-of-range values.

   ### User Interface: 
Facilitates interaction with the user, taking input, displaying results, and managing logging.

## Design Patterns and Principles

   ### Singleton (DataLogger): 
Ensures that only one instance of the DataLogger exists, providing a central point for data collection.
   ### Factory Method (NumberFactory): 
Encapsulates the logic of creating specific number objects (DecimalNumber or RomanNumber), promoting flexibility and extensibility.
   ### Abstract Base Class (Number): 
Defines a common interface for numbers, establishing a contract for subclasses and enabling polymorphic behavior.
    
## OOP Principles
   ### Polymorphism: 
The convert() method is implemented differently in DecimalNumber and RomanNumber, allowing for varying conversion logic depending on the number type.
   ### Abstraction: 
The Number class abstracts away the underlying implementation details of different number formats. The user interacts with the general concept of a "number" without needing to worry about how it's specifically represented.
   ### Inheritance:
 DecimalNumber and RomanNumber inherit from Number, inheriting its properties and methods. This promotes code reuse and a hierarchical structure.
   ### Encapsulation: 
Each class encapsulates its own data and behavior. For example, RomanNumber hides the complex conversion logic within its class, exposing only a simple interface to the user.

## Additional Notes

Robust Error Handling: The code incorporates extensive error handling to ensure valid input, correct conversion, and appropriate range checks.

Logging: The DataLogger provides a way to track the application's usage, which can be helpful for debugging or analysis.

Clear Separation of Concerns: The code is well-structured according to PEP 8, with each class having a distinct responsibility, making it easier to understand, maintain, and extend.
