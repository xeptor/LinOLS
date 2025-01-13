from tkinter import *
import subprocess
import struct
from tkinter import messagebox

class FileImport:
    def __init__(self, ui):
        self.ui = ui

    def temp_safe(self, ui):
        self.ui = ui
        if not self.ui.import_allow:
            messagebox.showerror("Error", "You cannot import a file if there is none open.")
            return
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        new_values = self.ui.current_values[self.ui.shift_count:]
        self.ui.current_values = new_values

        self.ui.new_path = "temp.bin"

        if self.ui.low_high:
            content_to_write = b''.join(struct.pack('<H', int(value)) for value in self.ui.current_values)
        else:
            content_to_write = b''.join(struct.pack('>H', int(value)) for value in self.ui.current_values)

        with open(self.ui.new_path, 'wb') as file:
            file.write(content_to_write)
        with open(self.ui.new_path, 'rb') as file:
            content = file.read()
            if self.ui.low_high:
                self.ui.new_values = struct.unpack('<' + 'H' * (len(content) // 2), content)
            else:
                self.ui.new_values = struct.unpack('>' + 'H' * (len(content) // 2), content)

    def import_file(self, ui, shortcut, path):
        self.ui = ui
        if not shortcut:
            result = subprocess.run(['zenity', '--file-selection'], capture_output=True, text=True)

            if not self.ui.import_allow:
                messagebox.showerror("Error", "You cannot import a file if there is none open.")
                return

            if result.returncode == 0:
                file_path = result.stdout.strip()
            else:
                return
        else:
            file_path = path
        with open(file_path, 'rb') as file:
            content = file.read()
            if self.ui.low_high:
                self.ui.imported_values = struct.unpack('<' + 'H' * (len(content) // 2), content)
            else:
                self.ui.imported_values = struct.unpack('>' + 'H' * (len(content) // 2), content)
            self.ui.text_widget.delete(1.0, END)
            rows = [self.ui.imported_values[i:i + self.ui.columns] for i in range(0, len(self.ui.imported_values), self.ui.columns)]
            for row in rows:
                formatted = ' '.join(f"{value:05}" for value in row)
                self.ui.text_widget.insert(END, formatted + '\n')
            from maps import Maps_Utility
            maps = Maps_Utility(self.ui)
            maps.reapply_highlight_text()
            from Utilities import Utility
            self.utility = Utility(self)
            self.utility.check_difference_values(self.ui.imported_values, True, self.ui)
            from Module_2D import Mode2D
            self.mode_2d = Mode2D(self)
            self.ui.return_text = True
            self.mode_2d.update_2d(ui)