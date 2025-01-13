from tkinter import *
from tkinter import messagebox

class ValueDialog:
    def __init__(self, ui):
        self.ui = ui

    def value_dialog(self, ui, event=None):
        self.ui = ui
        self.value_dialog_window = Toplevel(bg="#333")

        self.value_dialog_window.resizable(False, False)

        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()

        width = 250
        height = 125
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.value_dialog_window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.value_dialog_window.title("Value Changer")

        self.selected_value = ""

        if self.ui.text_widget.tag_ranges("sel"):
            self.selected = True
            self.ori_selected = self.ui.text_widget.get("sel.first", "sel.last")
            self.selected_text = self.ui.text_widget.get("sel.first", "sel.last").strip().split()
        else:
            self.selected = False
            self.selected_text = ""

        self.new_text = ""

        self.entry = Entry(self.value_dialog_window, bg="#555", fg="white", highlightthickness=0, font=('Arial', 11))
        self.entry.grid(row=0, column=0, columnspan=4, padx=40, pady=10)

        button1 = Button(self.value_dialog_window, text="=", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("="))
        button2 = Button(self.value_dialog_window, text="+", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("+"))
        button3 = Button(self.value_dialog_window, text="-", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("-"))
        button4 = Button(self.value_dialog_window, text="%", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("%"))

        button1.grid(row=1, column=0, padx=5, pady=5)
        button2.grid(row=1, column=1, padx=5, pady=5)
        button3.grid(row=1, column=2, padx=5, pady=5)
        button4.grid(row=1, column=3, padx=5, pady=5)

        ok_button = Button(self.value_dialog_window, text="Ok", command= lambda: self.calculate(self.ui), font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", width=6)
        ok_button.grid(row=2, column=0, columnspan=4, pady=10)
        self.entry.focus_set()

        return "break"

    def change_value(self, value):
        self.selected_value = value

    def calculate(self, ui):
        self.ui = ui
        if self.selected:
            start = self.ui.text_widget.index(SEL_FIRST)
            end = self.ui.text_widget.index(SEL_LAST)

            new_lines_pos = []
            new_value = 0
            counter = 0

            for i in range(len(self.ori_selected)):
                if self.ori_selected[i] == "\n":
                    new_lines_pos.append(i)

            new_text = ""

            for item in self.selected_text:
                counter += 1
                try:
                    float(self.entry.get())
                except ValueError:
                    messagebox.showerror("Invalid Number!", "You have entered an invalid number!")
                    return

                if self.selected_value == "=":
                    new_value = int(self.entry.get())
                elif self.selected_value == "+":
                    new_value = (int(item) + int(self.entry.get()))
                elif self.selected_value == "-":
                    new_value = (int(item) + (int(self.entry.get())) * -1)
                elif self.selected_value == "%":
                    percentage = int(item) * (float(self.entry.get()) / 100)
                    new_value = int(item) + percentage
                else:
                    messagebox.showerror("Select Operator!", "Please select an operator!")
                    return

                if not float(new_value) <= 65535 or not float(new_value) >= 0:
                    messagebox.showerror("Invalid Number!", "You have entered an invalid number!")
                    return

                new_value = f"{int(round(float(new_value))):05}"

                if counter == len(self.selected_text):
                    new_text += str(new_value)
                else:
                    new_text += str(new_value) + " "

            new_text = self.insert_newlines(new_text, new_lines_pos)

            self.ui.text_widget.replace(start, end, new_text)

            self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
            int_values = [int(x) for x in self.ui.current_values]
            from Utilities import Utility
            self.utility = Utility(self)
            self.utility.check_difference_values(int_values, False, self.ui)

            from maps import Maps_Utility
            maps = Maps_Utility(self.ui)
            maps.reapply_highlight_text()
        else:
            messagebox.showerror("Selection", "Please select something in text widget!")
        self.value_dialog_window.destroy()

    def insert_newlines(self, text, positions):
        new_text = list(text)
        for pos in positions:
            if pos < len(new_text):
                new_text[pos] = '\n'
        return ''.join(new_text)