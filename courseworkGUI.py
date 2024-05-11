import tkinter as tk
from tkinter import ttk, messagebox
from coursework import NumberFactory, NumberConverter, DecimalNumber, RomanNumber, DataLogger

class NumberConverterUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Converter")
        self.geometry("800x250")

        self.dark_mode = False  # Initial state is light mode
        self.style = ttk.Style()
        self.set_style()

        self.converter = NumberConverter()
        self.logger = DataLogger()

        self.dark_mode_switch = ttk.Checkbutton(self, text="Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_switch.pack()

        self.input_label = ttk.Label(self, text="Enter a Roman numeral or decimal number:")
        self.input_label.pack(pady=10)

        self.input_entry = ttk.Entry(self, font=("Arial", 14))
        self.input_entry.pack()
        self.input_entry.bind("<Return>", self.convert_on_enter)
        self.input_entry.bind("<space>", self.convert_on_spacebar)

        self.convert_button = ttk.Button(self, text="Convert", command=self.convert_number)
        self.convert_button.pack(pady=10)

        self.result_label = tk.Text(self, width=100, height=3, wrap="word", font=("Arial", 14))
        self.result_label.pack()

        self.command_frame = ttk.Frame(self)
        self.command_frame.pack(pady=10)

        self.clear_button = ttk.Button(self.command_frame, text="Clear", command=self.clear_logs)
        self.clear_button.pack(side="left", padx=5)

        self.data_button = ttk.Button(self.command_frame, text="Data", command=self.print_duomenys)
        self.data_button.pack(side="left", padx=5)

        self.logs_button = ttk.Button(self.command_frame, text="Logs", command=self.display_logs)
        self.logs_button.pack(side="left", padx=5)

        self.rules_button = ttk.Button(self.command_frame, text="Rules", command=self.display_rules)
        self.rules_button.pack(side="left", padx=5)

        self.exit_button = ttk.Button(self.command_frame, text="Exit", command=self.quit)
        self.exit_button.pack(side="left", padx=5)

    def convert_number(self):
        user_input = self.input_entry.get()
        try:
            number = NumberFactory.create_number(user_input)
            converted_result = self.converter.convert(number)

            conversion_type = "decimal_to_roman" if isinstance(number, DecimalNumber) else "roman_to_decimal"

            if isinstance(converted_result, tuple):
                decimal_value, violated_rules = converted_result
                rule_violations = []
                for rule in violated_rules:
                    rule_violations.append(rule[1])

                log_message = f"{user_input.upper()} is a {number.__class__.__name__}," \
                              f" and its converted value is {decimal_value}."
                if rule_violations:
                    log_message += " " + " ".join(rule_violations)

                self.logger.log_data(log_message, conversion_type)
                self.result_label.delete('1.0', 'end')  # Clear the text area
                self.result_label.insert('end', log_message)  # Insert the new log message
            else:
                self.logger.log_data(f"{user_input} is a {number.__class__.__name__},"
                                     f" and its converted value is {converted_result}", conversion_type)
                self.result_label.delete('1.0', 'end')  # Clear the text area
                self.result_label.insert('end', f"{user_input} is a {number.__class__.__name__}, and its converted value is {converted_result}")

        except Exception as e:
            error_message = str(e)
            self.logger.log_data(error_message, "error")
            self.result_label.delete('1.0', 'end')  # Clear the text area
            self.result_label.insert('end', error_message)

    def convert_on_enter(self, event):
        self.convert_number()

    def convert_on_spacebar(self, event):
        self.convert_number()

    def clear_logs(self):
        """Clears the contents of both files and reinitializes duomenys.txt"""
        confirmation = messagebox.askyesno("Clear Logs", "Are you sure you want to clear the log files?")
        if confirmation:
            for file_path in [self.logger.log_file, self.logger.data_file]:
                try:
                    open(file_path, 'w').close()
                    if file_path == self.logger.data_file:
                        self.logger.initialize_datafile()
                except FileNotFoundError:
                    messagebox.showerror("Error", f"Warning: File not found: {file_path}")
            messagebox.showinfo("Logs Cleared", "Log files have been cleared.")

    def print_duomenys(self):
        data_file_path = self.logger.data_file
        try:
            with open(data_file_path, "r") as duomenys_file:
                duomenys_content = duomenys_file.read()
                messagebox.showinfo("Duomenys.txt", f"Contents of duomenys.txt:\n\n{duomenys_content}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Error: duomenys.txt not found.")

    def display_logs(self):
        try:
            with open(self.logger.log_file, "r") as istorija_file:
                log_lines = istorija_file.readlines()

            log_window = tk.Toplevel(self)
            log_window.title("Logs")

            log_frame = ttk.Frame(log_window)
            log_frame.pack(padx=10, pady=10)

            log_table = ttk.Treeview(log_frame, columns=("Log Entry",), show="headings")
            log_table.heading("Log Entry", text="Log Entry")
            log_table.column("Log Entry", width=400)

            for line in log_lines:
                log_table.insert("", "end", values=(line.strip(),))

            log_table.pack(side="left", fill="both", expand=True)

            scroll_bar = ttk.Scrollbar(log_frame, orient="vertical", command=log_table.yview)
            scroll_bar.pack(side="right", fill="y")
            log_table.configure(yscrollcommand=scroll_bar.set)

        except FileNotFoundError:
            messagebox.showerror("Error", "Error: istorija.txt not found.")

    def display_rules(self):
        rules_window = tk.Toplevel(self)
        rules_window.title("Roman Numeral Rules")

        rules_frame = ttk.Frame(rules_window)
        rules_frame.pack(padx=10, pady=10)

        rules_text = "\n".join([f"{rule[0]}: {rule[1]}" for rule in RomanNumber.ROMAN_NUMERAL_RULES])

        rules_label = ttk.Label(rules_frame, text=rules_text, justify="left")
        rules_label.pack()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_style()

    def set_style(self):
        if self.dark_mode:
            self.style.theme_use('clam')  # You can experiment with other dark themes
            self.style.configure('.', background='black', foreground='white')
            self.style.configure('TButton', background='gray20', foreground='white')
            self.style.configure('TLabel', background='black', foreground='white')
            self.style.configure('TEntry', fieldbackground='gray10', foreground='white')
            self.configure(background='black')
        else:
            self.style.theme_use('default')
            self.style.configure('.', background='white', foreground='black')
            self.style.configure('TButton', background='white', foreground='black')
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TEntry', fieldbackground='white', foreground='black')
            self.configure(background='white')

if __name__ == "__main__":
    app = NumberConverterUI()
    app.mainloop()
