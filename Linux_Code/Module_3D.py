import math
from tkinter import *
from tkinter import messagebox
import re
import numpy as np

class Mode3D:
    def __init__(self, ui):
        self.ui = ui
        self.map_precision = 0

    def check_difference_3d(self, i, j):
        try:
            if not self.ui.map_decimal:
                current_value = int(self.ui.entry_widgets[i][j].get())
                original_value = int(self.ui.original[i][j])
            else:
                current_value = float(self.ui.entry_widgets[i][j].get())
                original_value = float(self.ui.original[i][j])
        except ValueError:
            return "break"

        difference = current_value - original_value
        self.ui.label_diff_3d.configure(text=f"Diff: {difference}")

    def copy_selected_cells(self):
        selected_content = ""
        for i in range(self.ui.rows_3d):
            row_content = ""
            for j in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[i][j]
                if entry.cget('bg') == 'lightblue':
                    row_content += entry.get() + "\t"
            if row_content:
                selected_content += row_content.strip() + "\n"
        selected_content = selected_content.strip()
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(selected_content)

    def start_interaction(self, event, i, j):
        x, y = event.x_root, event.y_root
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.selected_cells = {(i, j)}
        self.toggle_selection(i, j)
        self.highlight_cells()

    def start_interaction_x(self, event, j):
        x, y = event.x_root, event.y_root
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.selected_cells = {(None, j)}
        self.highlight_cells()

    def start_interaction_y(self, event, i):
        x, y = event.x_root, event.y_root
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.selected_cells = {(i, None)}
        self.highlight_cells()

    def end_interaction(self, event):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def drag_to_select(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        self.highlight_cells()

        if self.start_x == self.end_x and self.start_y == self.end_y:
            i, j = self.get_cell_index(self.start_x, self.start_y)
            if i is not None and j is not None:
                self.toggle_selection(i, j)

    def highlight_cells(self):
        if self.start_x is not None and self.start_y is not None:
            start_i, start_j = self.get_cell_index(self.start_x, self.start_y)
            if start_i is not None and start_j is not None:
                end_i, end_j = self.get_cell_index(self.end_x, self.end_y)
                if end_i is not None and end_j is not None:
                    min_i = min(start_i, end_i)
                    max_i = max(start_i, end_i)
                    min_j = min(start_j, end_j)
                    max_j = max(start_j, end_j)

                    for i in range(self.ui.rows_3d):
                        for j in range(self.ui.columns_3d):
                            entry = self.ui.entry_widgets[i][j]

                            if min_i <= i <= max_i and min_j <= j <= max_j:
                                if (i, j) not in self.selected_cells:
                                    entry.configure(bg="lightblue")
                            else:
                                if (i, j) in self.selected_cells:
                                    entry.configure(bg="lightblue")
                                else:
                                    entry.configure(bg="white")

    def toggle_selection(self, i, j):
        if (i, j) in self.selected_cells:
            self.selected_cells.remove((i, j))
            self.ui.entry_widgets[i][j].configure(bg="white")
        else:
            self.selected_cells.add((i, j))
            self.ui.entry_widgets[i][j].configure(bg="lightblue")

    def get_cell_index(self, x, y):
        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[i][j]
                entry_x = entry.winfo_rootx()
                entry_y = entry.winfo_rooty()
                entry_width = entry.winfo_width()
                entry_height = entry.winfo_height()
                if entry_x <= x <= entry_x + entry_width and entry_y <= y <= entry_y + entry_height:
                    return i, j
        return None, None

    def increase_selected_text(self, int_value):
        try:
            increase_value = int_value
            for i in range(self.ui.rows_3d):
                for j in range(self.ui.columns_3d):
                    entry = self.ui.entry_widgets[i][j]
                    if entry.cget('bg') == 'lightblue':
                        if not self.ui.map_decimal:
                            current_value = int(entry.get())
                        else:
                            current_value = float(entry.get().strip())
                        new_value = current_value + increase_value
                        if 0 > new_value or new_value > 65535:
                            raise ValueError
                        entry.delete(0, END)
                        if not self.ui.map_decimal:
                            new_value_str = '{:05d}'.format(new_value)
                            entry.insert(END, new_value_str)
                        else:
                            new_data = float(round(new_value, self.map_precision))
                            parts = str(new_data).split('.')
                            decimal_length = len(parts[1])
                            str_data = str(new_data)
                            if decimal_length < self.map_precision:
                                for x in range(self.map_precision - decimal_length):
                                    str_data += "0"
                            parts = str_data.split('.')
                            self.ui.entry_widgets[i][j].insert(0, f"{int(parts[0]):05}.{parts[1]} ")
                        self.check_difference(event=None, i=i, j=j)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

        self.update_3d_view()

    def increase_selected_text_per(self, float_value):
        try:
            percentage_increase = float_value / 100.0
            for i in range(self.ui.rows_3d):
                for j in range(self.ui.columns_3d):
                    entry = self.ui.entry_widgets[i][j]
                    if entry.cget('bg') == 'lightblue':
                        if not self.ui.map_decimal:
                            current_value = int(entry.get())
                            increase_value = int(current_value * percentage_increase)
                        else:
                            current_value = float(entry.get())
                            increase_value = float(current_value * percentage_increase)
                        new_value = current_value + increase_value
                        if 0 > new_value or new_value > 65535:
                            raise ValueError
                        entry.delete(0, END)
                        if not self.ui.map_decimal:
                            new_value_str = '{:05d}'.format(math.ceil(new_value))
                            entry.insert(END, new_value_str)
                        else:
                            new_data = float(round(math.ceil(new_value), self.map_precision))
                            parts = str(new_data).split('.')
                            decimal_length = len(parts[1])
                            str_data = str(new_data)
                            if decimal_length < self.map_precision:
                                for x in range(self.map_precision - decimal_length):
                                    str_data += "0"
                            parts = str_data.split('.')
                            self.ui.entry_widgets[i][j].insert(0, f"{int(parts[0]):05}.{parts[1]} ")
                        self.check_difference(event=None, i=i, j=j)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid percentage.")
        self.update_3d_view()

    def set_text(self, int_value):
        try:
            set_text = int_value
            for i in range(self.ui.rows_3d):
                for j in range(self.ui.columns_3d):
                    entry = self.ui.entry_widgets[i][j]
                    if entry.cget('bg') == 'lightblue':
                        entry.delete(0, END)
                        if not self.ui.map_decimal:
                            new_value = set_text
                            new_value_str = '{:05d}'.format(new_value)
                            entry.insert(END, new_value_str)
                        else:
                            new_data = float(round(set_text, self.map_precision))
                            parts = str(new_data).split('.')
                            decimal_length = len(parts[1])
                            str_data = str(new_data)
                            if decimal_length < self.map_precision:
                                for x in range(self.map_precision - decimal_length):
                                    str_data += "0"
                            parts = str_data.split('.')
                            entry.insert(0, f"{int(parts[0]):05}.{parts[1]} ")
                        self.check_difference(event=None, i=i, j=j)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        self.update_3d_view()

    def resize_grid(self, new_columns, new_rows):
        from y_axis_properties_window import y_axis_properties
        self.y_axis_properties = y_axis_properties(self.ui)
        from x_axis_properties_window import x_axis_properties
        self.x_axis_properties = x_axis_properties(self.ui)
        from map_properties_window import Map_properties
        self.map_properties = Map_properties(self.ui)
        if new_rows > len(self.ui.entry_y_widgets):
            for x in range(len(self.ui.entry_y_widgets), new_rows):
                entry = Entry(self.ui.y_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=x, column=0)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>', lambda event, i=x: self.check_difference_y(event, i))
                entry.bind("<FocusOut>", lambda event, i=x: (self.on_focus_out(event, i, 0, "y")))
                entry.bind("<ButtonPress-1>", lambda event, i=x: self.start_interaction_y(event, i))
                entry.bind("<B1-Motion>", self.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.end_interaction)
                entry.bind("<Control-a>", lambda event, i=x: self.select_all(event, i, 0, "y"))
                entry.bind("<Tab>", self.clear_highlight_on_tab)
                entry.bind("<Button-3>", self.y_axis_properties.show_context_menu)
                self.ui.entry_y_widgets.append(entry)
                self.ui.original_Y.append("00000")
        elif new_rows < len(self.ui.entry_y_widgets):
            for i in range(len(self.ui.entry_y_widgets) - 1, new_rows - 1, -1):
                entry = self.ui.entry_y_widgets.pop()
                entry.destroy()
                self.ui.original_Y.pop()

        for i in range(new_rows):
            entry = self.ui.entry_y_widgets[i]
            entry.grid(row=i, column=0)

        if new_columns > len(self.ui.entry_x_widgets[0]):
            for x in range(len(self.ui.entry_x_widgets[0]), new_columns):
                entry = Entry(self.ui.x_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=0, column=x)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>', lambda event, j=x: self.check_difference_x(event, j))
                entry.bind("<FocusOut>", lambda event, j=x: (self.on_focus_out(event, 0, j, "x")))
                entry.bind("<ButtonPress-1>", lambda event, j=x: self.start_interaction_x(event, j))
                entry.bind("<B1-Motion>", self.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.end_interaction)
                entry.bind("<Control-a>", lambda event, j=x: self.select_all(event, 0, j, "x"))
                entry.bind("<Tab>", self.clear_highlight_on_tab)
                entry.bind("<Button-3>", self.x_axis_properties.show_context_menu)
                self.ui.entry_x_widgets[0].append(entry)
                self.ui.original_X[0].append("00000")
        elif new_columns < len(self.ui.entry_x_widgets[0]):
            for j in range(len(self.ui.entry_x_widgets[0]) - 1, new_columns - 1, -1):
                entry = self.ui.entry_x_widgets[0].pop()
                entry.destroy()
                self.ui.original_X[0].pop()

        if new_rows > len(self.ui.entry_widgets):
            for x in range(len(self.ui.entry_widgets), new_rows):
                row = []
                original_row = []
                for y in range(new_columns):
                    entry = Entry(self.ui.main_frame, width=5, font=("Comfortaa", 10))
                    entry.grid(row=x, column=y)
                    entry.insert(END, "00000")
                    entry.bind('<KeyRelease>',
                               lambda event, i=x, j=y: (
                               self.check_difference(event, i, j), self.check_difference_3d(i, j)))
                    entry.bind("<FocusOut>", lambda event, i=x, j=y: (self.on_focus_out(event, i, j, "map")))
                    entry.bind("<ButtonPress-1>", lambda event, i=x, j=y: (
                        self.start_interaction(event, i, j), self.check_difference_3d(i, j)))
                    entry.bind("<B1-Motion>", self.drag_to_select)
                    entry.bind("<ButtonRelease-1>", self.end_interaction)
                    entry.bind("<Control-a>", lambda event, i=x, j=y: self.select_all(event, i, j, "map"))
                    entry.bind("<Tab>", self.clear_highlight_on_tab)
                    entry.bind("<Button-3>", self.map_properties.show_context_menu)
                    row.append(entry)
                    original_row.append("00000")
                self.ui.entry_widgets.append(row)
                self.ui.original.append(original_row)
        elif new_rows < len(self.ui.entry_widgets):
            for i in range(len(self.ui.entry_widgets) - 1, new_rows - 1, -1):
                row = self.ui.entry_widgets.pop()
                for entry in row:
                    entry.destroy()
                self.ui.original.pop()

        for x in range(len(self.ui.entry_widgets)):
            row = self.ui.entry_widgets[x]
            original_row = self.ui.original[x]
            for y in range(len(row), new_columns):
                entry = Entry(self.ui.main_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=x, column=y)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>',
                           lambda event, i=x, j=y: (
                               self.check_difference(event, i, j), self.check_difference_3d(i, j)))
                entry.bind("<FocusOut>", lambda event, i=x, j=y: (self.on_focus_out(event, i, j, "map")))
                entry.bind("<ButtonPress-1>", lambda event, i=x, j=y: (
                    self.start_interaction(event, i, j), self.check_difference_3d(i, j)))
                entry.bind("<B1-Motion>", self.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.end_interaction)
                entry.bind("<Control-a>", lambda event, i=x, j=y: self.select_all(event, i, j, "map"))
                entry.bind("<Tab>", self.clear_highlight_on_tab)
                entry.bind("<Button-3>", self.map_properties.show_context_menu)
                row.append(entry)
                original_row.append("00000")
            for j in range(len(row) - 1, new_columns - 1, -1):
                entry = row.pop()
                entry.destroy()
                original_row.pop()

        self.ui.columns_3d = new_columns
        self.ui.rows_3d = new_rows

    def update_3d_view(self):
        x = np.arange(self.ui.columns_3d)
        y = np.arange(self.ui.rows_3d)
        x, y = np.meshgrid(x, y)

        values = np.array([[float(self.ui.entry_widgets[i][j].get()) for j in range(self.ui.columns_3d)]
                           for i in range(self.ui.rows_3d)])

        if self.ui.signed_values:
            for i in range(values.shape[0]):
                for j in range(values.shape[1]):
                    if values[i, j] > 55000:
                        values[i, j] = 0

        self.ui.ax_3d.clear()
        surf = self.ui.ax_3d.plot_surface(x, y, values, cmap='viridis', edgecolor='none')
        self.ui.ax_3d.set_xlabel('X')
        self.ui.ax_3d.set_ylabel('Y')
        self.ui.ax_3d.set_zlabel('Value')

        if all(entry.get() == "00000" for entry in self.ui.entry_x_widgets[0]) and \
                all(entry.get() == "00000" for entry in self.ui.entry_y_widgets):
            self.ui.ax_3d.set_xticks([])
            self.ui.ax_3d.set_yticks([])
        else:
            self.ui.ax_3d.set_xticks(np.arange(0, self.ui.columns_3d, 1))
            self.ui.ax_3d.set_yticks(np.arange(0, self.ui.rows_3d, 1))

        self.ui.canvas_3d.draw()

    def paste_data(self, maps_sel, data, row, col, new, name):
        if maps_sel:
            from maps import Maps_Utility
            maps = Maps_Utility(self.ui)
            with open(maps.file_path, 'r') as file:
                content = file.read().split('\n')
                for i in range(len(content)):
                    if content[i] == name:
                     map_factor = float(content[i + 4])
                     self.map_precision = int(content[i + 5])
                     break

            self.resize_grid(col, row)
            index = 0
            str_data = ""
            self.ui.map_values = []
            for i in range(row):
                for j in range(col):
                    self.ui.entry_widgets[i][j].delete(0, END)
                    data = list(data)
                    data[index] = int(data[index])
                    if map_factor != 1.0:
                        data[index] *= map_factor
                    self.ui.map_values.append(data[index])
                    if self.map_precision != 0:
                        new_data = float(round(data[index], self.map_precision))
                        parts = str(new_data).split('.')
                        decimal_length = len(parts[1])
                        str_data = str(new_data)
                        if decimal_length < self.map_precision:
                            for x in range(self.map_precision - decimal_length):
                                str_data += "0"
                        map_decimal = True
                    else:
                        data[index] = int(round(data[index]))
                        map_decimal = False
                    self.ui.entry_widgets[i][j].delete(0, END)
                    self.ui.map_decimal = map_decimal
                    if not map_decimal:
                        self.ui.entry_widgets[i][j].insert(0, f"{int(data[index]):05}")
                        if not new:
                            self.ui.original[i][j] = data[index]
                    else:
                        parts = str_data.split('.')
                        self.ui.entry_widgets[i][j].insert(0, f"{int(parts[0]):05}.{parts[1]} ")
                        self.ui.new_width = len(self.ui.entry_widgets[i][j].get()) - 1
                        self.ui.entry_widgets[i][j].configure(width=self.ui.new_width)
                        if not new:
                            self.ui.original[i][j] = float(self.ui.entry_widgets[i][j].get().strip())
                    index += 1
                    self.ui.entry_widgets[i][j].configure(fg="black")
            self.ui.rows_entry.configure(state="normal")
            self.ui.columns_entry.configure(state="normal")
            self.ui.rows_entry.delete(0, END)
            self.ui.rows_entry.insert(0, f"{row:02}")
            self.ui.columns_entry.delete(0, END)
            self.ui.columns_entry.insert(0, f"{col:02}")
            self.ui.rows_entry.configure(state="disabled")
            self.ui.columns_entry.configure(state="disabled")
        else:
            data = self.ui.window.clipboard_get()
            lines = data.strip().split('\n')
            num_rows = len(lines)
            num_columns = max(len(line.strip().split('\t')) for line in lines)
            try:
                self.ui.rows_entry.configure(state="normal")
                self.ui.columns_entry.configure(state="normal")
                self.ui.rows_entry.delete(0, END)
                self.ui.rows_entry.insert(0, f"{num_rows:02}")
                self.ui.columns_entry.delete(0, END)
                self.ui.columns_entry.insert(0, f"{num_columns:02}")
                self.ui.rows_entry.configure(state="disabled")
                self.ui.columns_entry.configure(state="disabled")

                self.clear_highlighting()

                self.resize_grid(num_columns, num_rows)

                for i, line in enumerate(lines):
                    numbers = line.strip().split('\t')
                    for j, num in enumerate(numbers):
                        if i < self.ui.rows_3d and j < self.ui.columns_3d:
                            new_value = '{:05d}'.format(int(num))
                            self.ui.entry_widgets[i][j].delete(0, END)
                            self.ui.entry_widgets[i][j].insert(0, new_value)
                            if not new:
                                self.ui.original[i][j] = new_value
                            self.ui.entry_widgets[i][j].configure(fg="black")

                last_row_values = [entry.get() for entry in self.ui.entry_widgets[-1]]
                if not any(last_row_values) and self.ui.rows_3d > 1:
                    last_row = self.ui.entry_widgets.pop()
                    for entry in last_row:
                        entry.destroy()
                    num_rows -= 1
                    self.ui.rows_entry.configure(state="normal")
                    self.ui.rows_entry.delete(0, END)
                    self.ui.rows_entry.insert(0, f"{num_rows:02}")
                    self.ui.rows_entry.configure(state="disabled")

            except TclError:
                messagebox.showerror("Error", "Clipboard operation failed. Please try again.")

        self.update_3d_view()

    def paste_x_data(self, maps, data, new):
        if maps:
            from maps import Maps_Utility
            maps = Maps_Utility(self.ui)
            with open(maps.file_path, 'r') as file:
                content = file.read().split('\n')
            index = maps.last_map_index
            index *= 10

            x_factor = float(content[index + 6])
            x_precision = int(content[index + 7])

            str_data = ""

            for i in range(len(data)):
                self.ui.entry_x_widgets[0][i].delete(0, END)
                data = list(data)
                data[i] = int(data[i])

                if x_factor != 1.0:
                    data[i] *= x_factor
                self.ui.x_values.append(data[i])
                if x_precision != 0:
                    new_data = float(round(data[i], x_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < x_precision:
                        for x in range(x_precision - decimal_length):
                            str_data += "0"
                    x_decimal = True
                else:
                    data[i] = int(round(data[i]))
                    x_decimal = False

                self.ui.x_axis_decimal = x_decimal

                if self.ui.map_decimal:
                    self.ui.entry_x_widgets[0][i].configure(width=self.ui.new_width)

                if not x_decimal:
                    self.ui.entry_x_widgets[0][i].insert(0, f"{int(data[i]):05}")
                    if not new:
                        self.ui.original_X[0][i] = data[i]
                else:
                    parts = str_data.split('.')
                    self.ui.entry_x_widgets[0][i].insert(0, f"{int(parts[0]):05}.{parts[1]}  ")
                    if not new:
                        self.ui.original_X[0][i] = float(self.ui.entry_x_widgets[0][i].get().strip())

        else:
            data = self.ui.window.clipboard_get()
            try:
                numbers = data.strip().split('\t')

                self.clear_highlighting()

                for j, num in enumerate(numbers):
                    if j < self.ui.columns_3d:
                        new_value = '{:05d}'.format(int(num))
                        self.ui.entry_x_widgets[0][j].delete(0, END)
                        self.ui.entry_x_widgets[0][j].insert(0, new_value)
                        if not new:
                            self.ui.original_X[0][j] = new_value

            except TclError:
                messagebox.showerror("Error", "Clipboard operation failed. Please try again.")

            self.update_3d_view()

    def paste_y_data(self, maps, data, new):
        if maps:
            from maps import Maps_Utility
            maps = Maps_Utility(self.ui)
            with open(maps.file_path, 'r') as file:
                content = file.read().split('\n')
            index = maps.last_map_index
            index *= 10

            y_factor = float(content[index + 8])
            y_precision = int(content[index + 9])

            str_data = ""

            for i in range(len(data)):
                data = list(data)
                data[i] = int(data[i])
                self.ui.entry_y_widgets[i].delete(0, END)

                if y_factor != 1.0:
                    data[i] *= y_precision
                self.ui.y_values.append(data[i])
                if y_precision != 0.0:
                    new_data = float(round(data[i], y_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < y_precision:
                        for x in range(y_precision - decimal_length):
                            str_data += "0"
                    y_decimal = True
                else:
                    data[i] = int(round(data[i]))
                    y_decimal = False
                self.ui.y_axis_decimal = y_decimal
                if not y_decimal:
                    self.ui.entry_y_widgets[i].insert(0, f"{int(data[i]):05}")
                    if not new:
                        self.ui.original_Y[i] = data[i]
                else:
                    parts = str_data.split('.')
                    self.ui.entry_y_widgets[i].insert(0, f"{int(parts[0]):05}.{parts[1]}  ")
                if self.ui.map_decimal:
                    self.ui.entry_y_widgets[i].configure(width=self.ui.new_width)
                    if not new:
                        self.ui.original_X[0][i] = float(self.ui.entry_x_widgets[0][i].get().strip())
        else:
            data = self.ui.window.clipboard_get()
            try:
                numbers = re.split(r'\s+', data.strip())

                self.clear_highlighting()

                for i, num in enumerate(numbers):
                    if i < len(self.ui.entry_y_widgets):
                        try:
                            new_value = '{:05d}'.format(int(num))
                            self.ui.entry_y_widgets[i].delete(0, END)
                            self.ui.entry_y_widgets[i].insert(0, new_value)
                            if i < len(self.ui.original_Y):
                                if not new:
                                    self.ui.original_Y[i] = new_value
                        except ValueError:
                            messagebox.showerror("Error", f"Invalid value '{num}' found in clipboard data.")
                            continue
                    else:
                        messagebox.showwarning("Warning", "More data in clipboard than available entry widgets.")


            except TclError:
                messagebox.showerror("Error", "Clipboard operation failed. Please try again.")

        self.update_3d_view()

    def clear_highlighting(self):
        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[i][j]
                entry.configure(bg="white")
                self.ui.window.update_idletasks()

    def check_difference(self, event, i, j):
        entry = self.ui.entry_widgets[i][j]
        original_value = float(self.ui.original[i][j])

        if len(entry.get()) > 5 and not self.ui.map_decimal:
            entry.configure(width = 5)
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)

        try:
            current_value = float(entry.get())
            if current_value > 65535 or current_value < 0:
                raise ValueError
        except ValueError:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)
            return

        if current_value > original_value:
            entry.configure(fg="red")
        elif current_value < original_value:
            entry.configure(fg="blue")
        else:
            entry.configure(fg="black")

        self.update_3d_view()

    def check_difference_x(self, event, j):
        entry = self.ui.entry_x_widgets[0][j]
        original_value = float(self.ui.original_X[0][j])

        if len(entry.get()) > 5 and not self.ui.x_axis_decimal:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)

        try:
            current_value = float(entry.get())
            if current_value > 65535 or current_value < 0:
                raise ValueError
        except ValueError:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)
            return

        if current_value > original_value:
            entry.configure(fg="red")
        elif current_value < original_value:
            entry.configure(fg="blue")
        else:
            entry.configure(fg="black")

        self.update_3d_view()

    def check_difference_y(self, event, i):
        entry = self.ui.entry_y_widgets[i]
        original_value = float(self.ui.original_Y[i])

        if len(entry.get()) > 5 and not self.ui.y_axis_decimal:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)

        try:
            current_value = float(entry.get())
            if current_value > 65535 or current_value < 0:
                raise ValueError
        except ValueError:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)
            return

        if current_value > original_value:
            entry.configure(fg="red")
        elif current_value < original_value:
            entry.configure(fg="blue")
        else:
            entry.configure(fg="black")

        self.update_3d_view()

    def copy_map_values(self):
        map_values = ""
        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                map_values += self.ui.entry_widgets[i][j].get() + "\t"
            map_values += "\n"
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(map_values)

    def copy_x_axis(self):
        x_axis_values = "\t".join(entry.get() for entry in self.ui.entry_x_widgets[0])
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(x_axis_values)

    def copy_y_axis(self):
        y_axis_values = "\n".join(entry.get() for entry in self.ui.entry_y_widgets)
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(y_axis_values)

    def check_all(self):
        rows = self.ui.rows_3d
        cols = self.ui.columns_3d

        for row in range(rows):
            for col in range(cols):
                self.check_difference(None, row, col)

        for col in range(cols):
            self.check_difference_x(None, col)

        for row in range(rows):
            self.check_difference_y(None, row)

    def on_focus_out(self, event, row, col, mode):
        if mode == "map":
            entry = self.ui.entry_widgets[row][col]
            if len(entry.get()) == 0 and not self.ui.map_decimal:
                entry.insert(END, f"{self.ui.original[row][col]:05}")
            elif len(entry.get()) == 0 and self.ui.map_decimal:
                parts = str(self.ui.original[row][col]).split('.')
                entry.insert(END, f"{int(parts[0]):05}.{parts[1]}")
            else:
                if not self.ui.map_decimal:
                    value = int(entry.get())
                    entry.delete(0, END)
                    entry.insert(END, f"{value:05}")
                else:
                    parts = entry.get().split('.')
                    entry.delete(0, END)
                    entry.insert(END, f"{int(parts[0]):05}.{parts[1]}")
                self.check_difference(None, row, col)
            if entry.selection_present():
                entry.selection_clear()
        if mode == "x":
            entry = self.ui.entry_x_widgets[row][col]
            if len(entry.get()) == 0 and not self.ui.x_axis_decimal:
                entry.insert(END, f"{self.ui.original_X[row][col]:05}")
            elif len(entry.get()) == 0 and self.ui.x_axis_decimal:
                parts = str(self.ui.original_X[row][col]).split('.')
                entry.insert(END, f"{int(parts[0]):05}.{parts[1]}")
            else:
                if not self.ui.x_axis_decimal:
                    value = int(entry.get())
                    entry.delete(0, END)
                    entry.insert(END, f"{value:05}")
                else:
                    parts = entry.get().split('.')
                    entry.delete(0, END)
                    entry.insert(END, f"{int(parts[0]):05}.{parts[1]}")
                self.check_difference_x(None, col)
            if entry.selection_present():
                entry.selection_clear()
        if mode == "y":
            entry = self.ui.entry_y_widgets[row]
            if len(entry.get()) == 0 and self.ui.y_axis_decimal:
                entry.insert(END, f"{self.ui.original_Y[row]:05}")
            elif len(entry.get()) == 0 and self.ui.y_axis_decimal:
                parts = str(self.ui.original_Y[row][col]).split('.')
                entry.insert(END, f"{int(parts[0]):05}.{parts[1]}")
            else:
                if not self.ui.y_axis_decimal:
                    value = int(entry.get())
                    entry.delete(0, END)
                    entry.insert(END, f"{value:05}")
                else:
                    parts = entry.get().split('.')
                    entry.delete(0, END)
                    entry.insert(END, f"{int(parts[0]):05}.{parts[1]}")
                self.check_difference_y(None, row)
            if entry.selection_present():
                entry.selection_clear()

    def select_all(self, event, row, col, mode):
        if mode in ("map", "x", "y"):
            if mode == "map":
                entry = self.ui.entry_widgets[row][col]
            elif mode == "x":
                entry = self.ui.entry_x_widgets[row][col]
            else:
                entry = self.ui.entry_y_widgets[row]

            entry.select_range(0, END)
            entry.icursor(END)
        return "break"

    def clear_highlight_on_tab(self, event):
        self.clear_highlighting()

    def set_default(self):
        self.resize_grid(10, 10)
        for row in range(self.ui.rows_3d):
            for col in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[row][col]
                entry.delete(0, END)
                entry.insert(END, "00000")
                self.ui.original[row][col] = 0

        for col in range(self.ui.columns_3d):
            entry = self.ui.entry_x_widgets[0][col]
            entry.delete(0, END)
            entry.insert(END, "00000")
            self.ui.original_X[0][col] = 0

        for row in range(self.ui.rows_3d):
            entry = self.ui.entry_y_widgets[row]
            entry.delete(0, END)
            entry.insert(END, "00000")
            self.ui.original_Y[row] = 0

        self.ui.columns_entry.configure(state="normal")
        self.ui.rows_entry.configure(state="normal")

        self.ui.rows_entry.delete(0, END)
        self.ui.columns_entry.delete(0, END)
        self.ui.rows_entry.insert(END, str(self.ui.rows_3d))
        self.ui.columns_entry.insert(END, str(self.ui.columns_3d))

        self.ui.columns_entry.configure(state="disabled")
        self.ui.rows_entry.configure(state="disabled")

        self.update_3d_view()

    def paste_selected(self):
        selected_counter = 0
        start_row, start_col = None, None

        for row in range(self.ui.rows_3d):
            for col in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[row][col]
                if entry.cget("bg") == "lightblue":
                    selected_counter += 1
                    if start_row is None and start_col is None:
                        start_row, start_col = row, col

        if selected_counter != 1:
            messagebox.showerror("Error", "Please select one value where pasting should start from!")
            return

        data = self.ui.window.clipboard_get()
        lines = data.strip().split('\n')
        num_rows = len(lines)
        num_columns = max(len(line.strip().split('\t')) for line in lines)

        if (start_row + num_rows > self.ui.rows_3d) or (start_col + num_columns > self.ui.columns_3d):
            messagebox.showerror("Error", "Not enough space to paste the values!")
            return

        for i, line in enumerate(lines):
            numbers = line.strip().split('\t')
            for j, num in enumerate(numbers):
                if i < self.ui.rows_3d and j < self.ui.columns_3d:
                    new_value = '{:05d}'.format(int(num))
                    self.ui.entry_widgets[start_row + i][start_col + j].delete(0, END)
                    self.ui.entry_widgets[start_row + i][start_col + j].insert(0, new_value)
                    self.ui.entry_widgets[start_row + i][start_col + j].configure(fg="black")
                    self.check_difference(None, start_row + i, start_col + j)