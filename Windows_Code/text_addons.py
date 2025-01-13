import tkinter
from tkinter import *
from tkinter import messagebox
import math
import os

class TextAddons:
    def __init__(self, ui):
        self.ui = ui
        self.entry_widget = Entry()

    def edit_mode(self, event):
        self.ui.edit_mode_active = True
        if self.ui.text_widget.tag_ranges(SEL):
            sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(sel_start, sel_end).strip()

            if len(selected_text) == 5:
                place_info = self.ui.text_widget.bbox(SEL_FIRST)
                x, y, width, height = place_info
                x_root = x
                y_root = y
                self.create_entry(sel_start, sel_end, selected_text, x_root, y_root)

        return "break"

    def create_entry(self, start_index, end_index, text, x_root, y_root):
        if self.entry_widget:
            self.entry_widget.destroy()

        self.entry_widget = Entry(self.ui.window, bg="#555", fg="white", highlightthickness=0, bd=0, font=("Courier", 9))
        self.entry_widget.insert(0, text)
        self.entry_widget.place(x=x_root + 14, y=y_root + 37, width=40, height=13)

        self.entry_widget.focus_set()
        self.entry_widget.bind("<Return>", lambda e: self.save_edit(e, start_index, end_index))
        self.ui.window.bind("<Button-1>", lambda event: self.on_outside_click(event, self.entry_widget, start_index, end_index))

    def on_outside_click(self, event, widget, func2, func3):
        if self.ui.edit_mode_active:
            if widget is not None:
                if widget.winfo_exists():
                    try:
                        x1, y1, x2, y2 = widget.bbox("all")
                        if not (x1 <= event.x <= x2 and y1 <= event.y <= y2):
                            self.save_edit(event, func2, func3)
                    except tkinter.TclError:
                        return

    def save_edit(self, event, start_index=None, end_index=None):
        if self.entry_widget:
            new_text = self.entry_widget.get().strip()
            try:
                int(new_text)
            except ValueError:
                self.entry_widget.destroy()
                self.ui.text_widget.tag_remove(SEL, 1.0, END)
                messagebox.showerror("Invalid Number!", "You have entered an invalid number!")
                return
            if len(new_text) <= 5:
                new_text = f"{int(new_text):05}"
                self.ui.text_widget.delete(start_index, end_index)
                self.ui.text_widget.insert(start_index, new_text)

                from maps import Maps_Utility
                maps = Maps_Utility(self.ui)
                maps.reapply_highlight_text()

            self.entry_widget.destroy()
            self.entry_widget = None
            from Utilities import Utility
            self.utility = Utility(self)
            self.utility.check_value_changes(self.ui)
            self.ui.edit_mode_active = False

    def start_selection(self, event):
        self.selection_start = self.ui.text_widget.index(f"@{event.x},{event.y}")

    def stop_drag(self, event):
        end_str = str(self.ui.text_widget.index(f"@{event.x},{event.y}"))
        start_str = str(self.selection_start)
        end = int(end_str.split('.')[1])
        self.end_row = int(end_str.split('.')[0])
        self.start_row = int(start_str.split('.')[0])
        start = int(start_str.split('.')[1])

        end_temp = end / 6
        start_temp = start / 6

        temp1 = math.ceil(end_temp)
        temp2 = math.floor(start_temp)

        self.end = (temp1 * 6) - 1
        self.start = (temp2 * 6)

        self.on_enter()
        self.adjust_selection()

    def adjust_selection(self):
        try:
            sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(sel_start, sel_end)
        except tkinter.TclError:
            return

        row, col = sel_end.split('.')
        col = int(col)

        if selected_text.endswith(' '):
            col -= 1

        self.ui.text_widget.mark_set(INSERT, f"{row}.{col}")

        self.ui.text_widget.tag_remove(SEL, "1.0", END)
        self.ui.text_widget.tag_add(SEL, f"{sel_start}", f"{row}.{col}")

        if len(selected_text.strip()) == 5:
            text = str(sel_start)
            parts = text.split('.')
            row = int(parts[0]) - 1
            col = int(parts[1]) // 6

            index = row * self.ui.columns + col

            self.ui.ori_value_label.configure(text=f"Ori: {self.ui.unpacked[index - self.ui.shift_count]:05}")
        else:
            self.ui.ori_value_label.configure(text="Ori: 00000")

    def on_enter(self):
        self.ui.text_widget.tag_remove(SEL, "1.0", END)
        self.ui.text_widget.tag_add(SEL, f"{self.start_row}.{self.start}", f"{self.end_row}.{self.end}")

    def disable_double_click_selection(self, event):
        return 'break'

    def disable_user_input(self, event):
        if (event.keysym == 'v' or event.keysym == 'V') and event.state & 0x0004:
            file_path = self.ui.window.clipboard_get()
            if os.path.isfile(file_path):
                result = messagebox.askyesno("Open a new file", "Do you really want to open a new file?")
                if result:
                    self.ui.file_path = file_path
                    self.ui.import_allow = True
                    from text_view import TextView
                    text_view_ = TextView(self.ui)
                    text_view_.display_text(self.ui)

        if (event.keysym == 'i' or event.keysym == 'I') and event.state & 0x0004:
            file_path = self.ui.window.clipboard_get()
            if os.path.isfile(file_path):
                result = messagebox.askyesno("Import a new file", "Do you really want to import a new file?")
                if result:
                    from File_Import import FileImport
                    file_import_ = FileImport(self.ui)
                    file_import_.import_file(self.ui, True, file_path)
        if event.keysym == 'k' or event.keysym == 'K':
            from maps import Maps_Utility
            maps = Maps_Utility(self.ui)
            maps.add_map()

        if event.keysym == 'm' or event.keysym == 'M':
            entry_content = self.ui.entry.get()

            try:
                value = int(entry_content)
            except ValueError:
                return

            if not (0 <= value + 1 <= 60):
                return

            self.ui.columns = value + 1

            self.ui.entry.delete(0, END)
            self.ui.entry.insert(END, f"{self.ui.columns:02}")

            from Utilities import Utility
            utility = Utility(self.ui)
            self.ui.window.update_idletasks()
            utility.adjust_columns(self.ui, True)

        if event.keysym == 'w' or event.keysym == 'W':
            entry_content = self.ui.entry.get()

            try:
                value = int(entry_content)
            except ValueError:
                return

            if not (0 <= value - 1 <= 60):
                return

            self.ui.columns = value - 1

            self.ui.entry.delete(0, END)
            self.ui.entry.insert(END, f"{self.ui.columns:02}")

            from Utilities import Utility
            utility = Utility(self.ui)
            self.ui.window.update_idletasks()
            utility.adjust_columns(self.ui, True)

        if event.keysym == "Next" or event.keysym == "Prior":
            return

        return "break"

    def update_selected_count(self, event):
        if self.ui.text_widget.tag_ranges("sel"):
            selected_text = self.ui.text_widget.get("sel.first", "sel.last")
        else:
            selected_text = ""
        self.ui.selected_count = len(selected_text.split())
        self.ui.selected_count_label.configure(text=f"Selected: {self.ui.selected_count}")

    def show_hex_address_menu(self, event):
        try:
            self.sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(self.sel_start, sel_end).strip()
        except tkinter.TclError:
            return
        if len(selected_text) == 5:
            self.ui.hex_address_menu.post(event.x_root, event.y_root)

    def copy_hex_address(self):
        text = str(self.sel_start)
        parts = text.split('.')
        row = int(parts[0]) - 1
        col = int(parts[1]) // 6

        index = (row * self.ui.columns + col) * 2

        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(f"{index:06X}")