from tkinter import messagebox
from customtkinter import *

class x_axis_properties:
    def __init__(self, ui):
        self.ui = ui

    def x_axis_properties_dialog(self):
        self.value_dialog_window = CTkToplevel(fg_color="#333")

        self.value_dialog_window.resizable(False, False)

        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()

        width = 300
        height = 165
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.value_dialog_window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.value_dialog_window.title("X-Axis Properties")

        property_frame = CTkFrame(self.value_dialog_window, fg_color="#333", border_color="#555", border_width=1)
        property_frame.pack(fill=BOTH, expand=YES, pady=10, padx=15)

        factor_frame = CTkFrame(property_frame, fg_color="#333")
        factor_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        label_factor = CTkLabel(factor_frame, fg_color="#333", bg_color="white", text="Factor:  ", font=("Roboto", 12))
        label_factor.grid(row=0, column=0, padx=5)

        self.factor_entry = CTkEntry(factor_frame, fg_color="#555", text_color="white", width=140)
        self.factor_entry.grid(row=0, column=1)

        precision_frame = CTkFrame(property_frame, fg_color="#333")
        precision_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=20)

        label_precision = CTkLabel(precision_frame, fg_color="#333", bg_color="white", text="Decimals:  ", font=("Roboto", 12))
        label_precision.grid(row=0, column=0, padx=6)

        self.precision_entry = CTkEntry(precision_frame, fg_color="#555", text_color="white", width=100)
        self.precision_entry.grid(row=0, column=1)
        self.precision_entry.configure(state="disabled")

        precision_plus = CTkButton(precision_frame, fg_color="#444", text_color="white", width=6, hover_color="#555", text="+",
                                   command=lambda: self.precision_increase("+"))
        precision_plus.grid(row=0, column=2, padx=5)

        precision_minus = CTkButton(precision_frame, fg_color="#444", text_color="white", width=6, hover_color="#555", text="-",
                                   command=lambda: self.precision_increase("-"))
        precision_minus.grid(row=0, column=3, padx=5)

        apply_btn = CTkButton(property_frame, text="Apply", hover_color="#555", width=60, fg_color="#444", text_color="white", command=self.apply_changes)
        apply_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=20)

        self.insert_all_info()

    def insert_all_info(self):
        from maps import Maps_Utility
        maps = Maps_Utility(self.ui)

        if not os.path.exists(maps.file_path):
            return

        file_path = maps.file_path
        index = maps.last_map_index

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Please open a map first!")
            self.value_dialog_window.destroy()
            return

        with open(file_path, 'r') as file:
            content = file.read().split('\n')
            map_factor = content[(index * 10) + 6]
            map_precision = content[(index * 10) + 7]

            self.factor_entry.delete(0, END)
            self.factor_entry.insert(END, f"{map_factor}")
            self.precision_entry.configure(state="normal")
            self.precision_entry.delete(0, END)
            self.precision_entry.insert(END, f"{map_precision}")
            self.precision_entry.configure(state="disabled")

    def apply_changes(self):
        from maps import Maps_Utility
        maps = Maps_Utility(self.ui)

        file_path = maps.file_path
        index = maps.last_map_index

        try:
            new_map_factor = float(self.factor_entry.get())
            if 0 > new_map_factor > 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid map factor!")
            return
        try:
            new_map_precision = int(self.precision_entry.get())
            if 0 > new_map_precision > 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid map factor!")
            return


        with open(file_path, 'r') as file:
            content = file.read().split('\n')

        index *= 10

        content[index + 6] = str(new_map_factor)
        content[index + 7] = str(new_map_precision)

        with open(file_path, 'w') as file:
            for i in range(len(content)):
                file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])

        maps.update_3d_from_text()
        self.value_dialog_window.destroy()

    def show_context_menu(self, event):
        self.ui.right_click_x_axis.post(event.x_root, event.y_root)

    def precision_increase(self, mode):
        value = int(self.precision_entry.get())

        if mode == "+" and value + 1 <= 6:
            value += 1
        if mode == "-" and value - 1 >= 0:
            value -= 1

        self.precision_entry.configure(state="normal")
        self.precision_entry.delete(0, END)
        self.precision_entry.insert(END, str(value))
        self.precision_entry.configure(state="disabled")