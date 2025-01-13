from tkinter import *
from tkinter import messagebox
import time
from text_view import TextView

class Utility:
    def __init__(self, ui):
        self.ui = ui
        self.text_view = TextView(self)
        self.nothing_selected = False
        self.start_selection = 0
        self.end_selection = 0

    def calculate_start_and_end(self):
        if self.ui.text_widget.tag_ranges(SEL):
            sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(sel_start, sel_end).strip()
            selected_count = len(selected_text.split())

            text_start = str(sel_start)
            parts_start = text_start.split('.')
            row_start = int(parts_start[0]) - 1
            col_start = int(parts_start[1]) // 6

            index = row_start * self.ui.columns + col_start

            self.start_selection = int(index)

            self.end_selection = self.start_selection + selected_count - 1

    def copy_values(self):
        selected_text = self.ui.text_widget.selection_get()
        self.calculate_start_and_end()
        if not selected_text:
            messagebox.showwarning("Nothing Selected", "No values are selected to copy.")
            self.nothing_selected = True
            return
        self.nothing_selected = False

        selected_values = selected_text.strip().split()

        num_rows = len(selected_values) // self.ui.columns
        if len(selected_values) % self.ui.columns != 0:
            num_rows += 1

        copied_content = ""
        for i in range(num_rows):
            self.start_index = i * self.ui.columns
            self.end_index = min((i + 1) * self.ui.columns, len(selected_values))
            row_values = selected_values[self.start_index:self.end_index]
            copied_content += "\t".join(row_values) + "\n"

        try:
            self.ui.window.clipboard_clear()
            self.ui.window.clipboard_append(copied_content)
        except Exception as e:
            messagebox.showerror("Copy Error", f"An error occurred while copying: {e}")

    def paste_values(self, ui):
        self.ui = ui
        selected_text = self.ui.window.clipboard_get()
        cleaned_values = selected_text.strip().split()

        cursor_index = self.ui.text_widget.index(INSERT)
        cursor_row, cursor_col = map(int, cursor_index.split('.'))

        current_content = self.ui.text_widget.get(1.0, END)
        current_lines = current_content.strip().split('\n')

        row_index = cursor_row - 1
        col_index = cursor_col // 6

        differences = []

        for value in cleaned_values:
            try:
                num_value = int(value)
                if num_value < 0 or num_value > 65535:
                    raise ValueError("Value out of range")
            except ValueError:
                return

            formatted_value = f"{num_value:05}"

            if row_index >= len(current_lines):
                break

            current_line = current_lines[row_index]
            values = current_line.split()

            if col_index >= len(values):
                row_index += 1
                col_index = 0
                if row_index >= len(current_lines):
                    break
                current_line = current_lines[row_index]
                values = current_line.split()

            if values[col_index] != formatted_value:
                differences.append((values[col_index], formatted_value, row_index, col_index))

            values[col_index] = formatted_value

            current_lines[row_index] = ' '.join(values)

            col_index += 1

        updated_content = '\n'.join(current_lines)
        self.ui.text_widget.delete(1.0, END)
        self.ui.text_widget.insert(END, updated_content)

        from maps import Maps_Utility
        maps = Maps_Utility(self.ui)
        maps.reapply_highlight_text()

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        int_values = [int(x) for x in self.ui.current_values]
        self.check_difference_values(int_values, True, self.ui)
        self.ui.text_widget.see(cursor_index)

    def check_difference_values(self, new_values, importing, ui):
        self.ui = ui
        self.ui.differences = {}
        self.ui.differences_color = {}
        self.ui.ori_values = {}
        self.ui.index_differences = {}

        if len(self.ui.unpacked) != len(new_values):
            messagebox.showerror("Caution",
                                 "Size of the file is not the same!\nContact the developer & Reopen the LinOLS!")
            return

        if importing:
            first_visible_row = 0
            last_visible_row = len(self.ui.unpacked) // self.ui.columns
        else:
            first_visible_row = int(self.ui.text_widget.yview()[0] * self.ui.total_rows)
            last_visible_row = int(self.ui.text_widget.yview()[1] * self.ui.total_rows)

        index = (self.ui.columns * first_visible_row) - 1
        counter = -1

        self.ui.text_widget.tag_configure("changed_red", foreground="#ed7d80")
        self.ui.text_widget.tag_configure("changed_blue", foreground="#65a1e6")

        tag_changes = {}

        for row in range(first_visible_row, last_visible_row):
            for col in range(self.ui.columns):
                index += 1
                shifted_col = (col + self.ui.shift_count) % self.ui.columns
                row_shift = (col + self.ui.shift_count) // self.ui.columns
                current_row = row + row_shift

                start_index = f"{current_row + 1}.{shifted_col * 6}"
                end_index = f"{current_row + 1}.{(shifted_col + 1) * 6 - 1}"

                if self.ui.unpacked[index] < new_values[index]:
                    counter += 1
                    tag_changes[(start_index, end_index)] = "changed_red"
                    self.ui.differences[counter] = new_values[index]
                    self.ui.ori_values[counter] = self.ui.unpacked[index]
                    self.ui.differences_color[counter] = "red"
                    self.ui.index_differences[counter] = index
                elif self.ui.unpacked[index] > new_values[index]:
                    counter += 1
                    tag_changes[(start_index, end_index)] = "changed_blue"
                    self.ui.differences[counter] = new_values[index]
                    self.ui.ori_values[counter] = self.ui.unpacked[index]
                    self.ui.differences_color[counter] = "blue"
                    self.ui.index_differences[counter] = index

        for (start_index, end_index) in tag_changes.keys():
            self.ui.text_widget.tag_remove("changed_red", start_index, end_index)
            self.ui.text_widget.tag_remove("changed_blue", start_index, end_index)

        for (start_index, end_index), tag in tag_changes.items():
            self.ui.text_widget.tag_add(tag, start_index, end_index)

    def adjust_columns(self, ui, shortcut=False):
        self.ui = ui
        if not shortcut:
            entry_content = self.ui.entry.get()

            try:
                value = int(entry_content)
            except ValueError:
                return

            if not (0 <= value <= 60):
                return

            self.ui.columns = value

            self.ui.entry.delete(0, END)
            self.ui.entry.insert(END, f"{self.ui.columns:02}")

        max_frame = max(0, len(self.ui.unpacked) - self.ui.num_rows * self.ui.columns)
        self.ui.current_frame = min(self.ui.current_frame, max_frame)

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()

        self.ui.text_widget.delete(1.0, END)

        total_values = len(self.ui.unpacked)
        self.ui.total_rows = (total_values + self.ui.columns - 1) // self.ui.columns

        formatted_rows = '\n'.join(
            ' '.join(f"{self.ui.current_values[i * self.ui.columns + j]:05}"
                     for j in range(self.ui.columns)
                     if i * self.ui.columns + j < total_values)
            for i in range(self.ui.total_rows)
        )

        self.ui.text_widget.insert(END, formatted_rows + '\n')

        from maps import Maps_Utility
        maps = Maps_Utility(self.ui)
        maps.reapply_highlight_text()

        new_values = self.ui.current_values[self.ui.shift_count:]
        self.ui.current_values = new_values

        int_values = list(map(int, self.ui.current_values))
        self.check_difference_values(int_values, True, self.ui)

        from text_view import TextView
        from Module_2D import Mode2D
        self.text_view = TextView(self)
        self.mode2d = Mode2D(self)

        self.ui.return_text = True

        self.mode2d.draw_canvas(self.ui)

    def check_value_changes(self, ui):
        self.ui = ui
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        int_values = [int(x) for x in self.ui.current_values]
        new_values = int_values[self.ui.shift_count:]
        self.check_difference_values(new_values, False, self.ui)

    def move_items(self, ui):
        self.ui = ui
        self.ui.end_time = time.time()

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        int_values = list(map(int, self.ui.current_values))
        new_values = int_values[self.ui.shift_count:]

        if (self.ui.end_time - self.ui.start_time) > 0.2:
            try:
                value = int(self.ui.entry_position.get())
            except ValueError:
                return

            if not (0 <= value <= 60):
                return

            self.ui.shift_count = value
            self.ui.entry_position.delete(0, END)
            self.ui.entry_position.insert(0, f"{self.ui.shift_count:02}")

            if self.ui.shift_count < self.ui.columns:
                self.ui.values = [0] * self.ui.shift_count + new_values

                formatted_rows = '\n'.join(
                    ' '.join(
                        f"{self.ui.values[i + j]:05}" for j in range(self.ui.columns) if i + j < len(self.ui.values))
                    for i in range(0, len(self.ui.values), self.ui.columns)
                )

                self.ui.text_widget.delete(1.0, END)
                self.ui.text_widget.insert(END, formatted_rows + '\n')

                from maps import Maps_Utility
                maps = Maps_Utility(self.ui)
                maps.reapply_highlight_text()

            self.ui.start_time = time.time()

        self.check_difference_values(new_values, True, self.ui)

        from Module_2D import Mode2D
        self.mode2d = Mode2D(self)
        self.ui.return_text = True
        self.mode2d.draw_canvas(self.ui)

    def undo(self):
        self.ui.text_widget.edit_undo()
        self.check_value_changes(self.ui)

    def redo(self):
        self.ui.text_widget.edit_redo()
        self.check_value_changes(self.ui)

    def on_key_press_2d(self, event):
        if event.key == 'n' or event.key == 'N':
            self.value_changes_skipping(True)
        if event.key == 'v' or event.key == 'V':
            self.value_changes_skipping(False)
        if event.key == "pagedown":
            from Module_2D import Mode2D
            mode2d = Mode2D(self.ui)
            self.ui.red_line = 0
            self.ui.window.update_idletasks()
            mode2d.highlight_text(self.ui.red_line)
            mode2d.next_page()
        if event.key == "pageup":
            from Module_2D import Mode2D
            mode2d = Mode2D(self.ui)
            self.ui.red_line = 0
            self.ui.window.update_idletasks()
            mode2d.highlight_text(self.ui.red_line)
            mode2d.prev_page()

    def value_changes_skipping(self, forward):
        current_index = self.ui.current_frame + self.ui.red_line

        next_value = 0

        if forward:
            for i in range(len(self.ui.index_differences)):
                if self.ui.index_differences[i] > current_index:
                    next_value = self.ui.index_differences[i]
                    break
        else:
            for i in range(len(self.ui.index_differences) - 1, -1, -1):
                if self.ui.index_differences[i] < current_index:
                    next_value = self.ui.index_differences[i]
                    break

        if next_value == 0:
            return

        frame = 0
        while frame < next_value:
            temp = frame + self.ui.num_rows * self.ui.columns
            if temp < next_value:
                frame += self.ui.num_rows * self.ui.columns
            else:
                break

        self.ui.current_frame = frame

        self.ui.red_line = next_value - frame

        from Module_2D import Mode2D
        mode2d = Mode2D(self.ui)

        mode2d.highlight_text(self.ui.red_line)

        mode2d.draw_canvas(self.ui)