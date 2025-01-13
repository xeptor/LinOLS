import struct
from tkinter import *
import subprocess
from tkinter import messagebox, simpledialog
import os

class TextView:
    def __init__(self, ui):
        self.ui = ui

    def open_file(self, ui):
        self.ui = ui
        self.ui.open = True
        self.ui.import_allow = True
        self.display_text(self.ui)

    def display_text(self, ui):
        self.ui = ui
        if self.ui.open:
            result = subprocess.run(['zenity', '--file-selection'], capture_output=True, text=True)

            if result.returncode == 0:
                self.ui.file_path = result.stdout.strip()
        self.ui.open = False
        self.ui.update_counter = 0
        if self.ui.file_path:
            with open(self.ui.file_path, 'rb') as file:
                self.ui.text_widget.delete(1.0, END)
                content = file.read()
                if self.ui.low_high:
                    self.ui.unpacked = struct.unpack('<' + 'H' * (len(content) // 2), content)
                else:
                    self.ui.unpacked = struct.unpack('>' + 'H' * (len(content) // 2), content)
                self.ui.new_values =self.ui.unpacked
                self.ui.total_rows = len(self.ui.unpacked) // self.ui.columns
                if (len(self.ui.unpacked) % self.ui.columns) != 0:
                    self.ui.total_rows += 1
                self.ui.differences = []
                self.ui.ori_values = []
                self.ui.clean_up()
                self.ui.map_list.delete(0, END)
                self.ui.map_list_counter = 0
                self.show_all_data()
                from Module_2D import Mode2D
                self.mode2d = Mode2D(self)
                self.mode2d.draw_canvas(self.ui)

    def show_all_data(self):
        self.ui.text_widget.delete(1.0, END)
        for i in range(self.ui.total_rows):
            row = self.ui.unpacked[i * self.ui.columns:(i + 1) * self.ui.columns]
            formatted = ' '.join(f"{value:05}" for value in row)
            self.ui.text_widget.insert(END, formatted + '\n')
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        new_values = self.ui.current_values[self.ui.shift_count:]
        self.ui.current_values = new_values

        from maps import Maps_Utility
        maps = Maps_Utility(self.ui)
        maps.reapply_highlight_text()

    def change_display_mode(self, mode):
        answer = messagebox.askyesno("Change Display Mode", "Do you really want to change the display mode. This will remove any changes made!")
        if answer:
            if mode == "low_high":
                self.ui.low_high = True
            elif mode == "high_low":
                self.ui.low_high = False
            self.display_text(self.ui)

    def save_file(self, file_name=None):
        if not self.ui.file_path:
            messagebox.showwarning("Warning", "No file is currently open. Please open a file first.")
            return
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        new_values = self.ui.current_values[self.ui.shift_count:]
        self.ui.current_values = new_values
        manufacturer = simpledialog.askstring("Input", "Enter Manufacturer:")
        model = simpledialog.askstring("Input", "Enter Model:")
        modification = simpledialog.askstring("Input", "Enter Modification:")

        if not (manufacturer and model and modification):
            messagebox.showwarning("Warning", "Manufacturer, Model, and Modification are required.")
            return

        if not file_name:
            file_name = f"LinOLS_{manufacturer}_{model}_{modification}.bin"

        try:
            initial_dir = os.path.expanduser('~')
            file_path = self.linux_asksaveasfilename(initial_dir=initial_dir, defaultextension=".bin", initialfile=file_name)

            if not file_path:
                messagebox.showinfo("Info", "File save canceled.")
                return

            if self.ui.low_high:
                content_to_write = b''.join(struct.pack('<H', int(value)) for value in self.ui.current_values)
            else:
                content_to_write = b''.join(struct.pack('>H', int(value)) for value in self.ui.current_values)
            with open(file_path, 'wb') as file:
                file.write(content_to_write)

            messagebox.showinfo("Success", f"File saved successfully at {file_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")

    def linux_asksaveasfilename(self, initial_dir="", defaultextension=".bin", filetypes=[("Binary Files", "*.bin")],
                                initialfile=""):
        try:
            filter_string = ' '.join([f'--file-filter={ftype[0]} | {ftype[1]}' for ftype in filetypes])

            command = ['zenity', '--file-selection', '--save', '--confirm-overwrite',
                       '--filename=' + initialfile, '--file-filter=*.bin']

            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                file_path = result.stdout.strip()
                if not file_path.endswith(defaultextension):
                    file_path += defaultextension
                return file_path
            else:
                return None

        except FileNotFoundError:
            messagebox.showerror("Error", "You don't have zenity installed!")