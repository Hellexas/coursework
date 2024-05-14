# Coursework "Decimal and roman number converter"
Python coursework by Dovydas Bubulas EDiF-23/1


## Code Structure Overview

   ### Number Representation:
   Number (Abstract Base Class): Defines the core attributes and behavior of numbers, providing the template for subclasses.

![image](https://github.com/Hellexas/coursework/assets/164019473/aecc3288-096e-4d7d-a93d-8e83cced9784)

   DecimalNumber: Represents numbers in decimal (base-10) format.
   
![image](https://github.com/Hellexas/coursework/assets/164019473/c1d021a4-66dc-4407-875c-d0ff843ab757)

   RomanNumber: Represents numbers in Roman numeral format.
   
![image](https://github.com/Hellexas/coursework/assets/164019473/275eaf32-3e37-4e05-913e-cbf13e12aa57)
![image](https://github.com/Hellexas/coursework/assets/164019473/1ffd9449-6ac9-46f3-9a68-aa46a8b6c15c)

   ### Conversion and Logic:
   NumberConverter: Responsible for orchestrating the conversion process between number representations.

![image](https://github.com/Hellexas/coursework/assets/164019473/ec0aa2dc-2218-4de1-a0d9-24f0b502c954)

   NumberFactory: Uses the Factory Method pattern to create appropriate Number objects based on input (decimal or Roman).

![image](https://github.com/Hellexas/coursework/assets/164019473/ebfa679e-7a1c-45ad-b421-9dcb59b73d3d)


   DataLogger: A Singleton for logging interactions and conversions.

![image](https://github.com/Hellexas/coursework/assets/164019473/64ccb43e-b51f-4533-8fc8-3067b8f36e4c)


   ### Error Handling: 
Custom exceptions are defined for invalid inputs and out-of-range values.

![image](https://github.com/Hellexas/coursework/assets/164019473/da929552-f10e-438b-966f-a283bb3ab339)

   ### User Interface: 
Facilitates interaction with the user, taking input, displaying results, and managing logging. User intefrace is available in both CLI and GUI

## Design Patterns and Principles

   ### Singleton (DataLogger): 
Ensures that only one instance of the DataLogger exists, providing a central point for data collection.

![image](https://github.com/Hellexas/coursework/assets/164019473/70186b95-dd5c-4177-9478-85b27a3c1385)

   ### Factory Method (NumberFactory): 
Encapsulates the logic of creating specific number objects (DecimalNumber or RomanNumber), promoting flexibility and extensibility.

![image](https://github.com/Hellexas/coursework/assets/164019473/323206dd-1815-4bb5-af32-58171ef8499a)
![image](https://github.com/Hellexas/coursework/assets/164019473/39605e69-9fbd-423a-9c96-b6c78dc2c5e4)

   ### Abstract Base Class (Number): 
Defines a common interface for numbers, establishing a contract for subclasses and enabling polymorphic behavior.

![image](https://github.com/Hellexas/coursework/assets/164019473/5de42a84-6de6-4540-8319-d8e8b110bb81)

    
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
