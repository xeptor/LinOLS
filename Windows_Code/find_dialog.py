from tkinter import *

class Find_Dialog:
    def __init__(self, ui):
        self.ui = ui

    def find_dialog(self):
        dialog_find = Toplevel(bg="#333")
        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()
        width = 200
        height = 100
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        dialog_find.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        dialog_find.title("Find")
        label = Label(dialog_find, text="Enter the value:", bg="#333", fg="white")
        label.pack(pady=5)
        self.find_entry = Entry(dialog_find, bg="#333", fg="white", highlightthickness=0)
        self.find_entry.pack(pady=5)
        button_find = Button(dialog_find, text="Find", command=self.find, bg="#444", fg="white", highlightthickness=0)
        button_find.pack(side=RIGHT, pady=5, padx=5)
        button_previous = Button(dialog_find, text="Previous", command=self.find_previous, bg="#444", fg="white", highlightthickness=0)
        button_previous.pack(side=LEFT, pady=5, padx=5)
        button_next = Button(dialog_find, text="Next", command=self.find_next, bg="#444", fg="white", highlightthickness=0)
        button_next.pack(side=LEFT, pady=5)

    def find(self):
        self.ui.found_values_counter = 0
        row = 1
        col = 0
        counter = 1
        from File_Import import FileImport
        self.file_import = FileImport(self)
        self.file_import.temp_safe(self.ui)

        try:
            value = int(self.find_entry.get())
        except ValueError:
            return

        self.ui.text_widget.tag_remove("highlight", "1.0", "end")
        self.ui.text_widget.tag_configure("highlight", background="#907900")

        self.ui.found_values.clear()

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        new_values = self.ui.current_values[self.ui.shift_count:]
        int_values = [int(x) for x in new_values]
        self.ui.current_values = int_values
        self.ui.new_values = self.ui.current_values

        for i in range(len(self.ui.new_values)):
            if counter > self.ui.columns:
                row += 1
                counter = 1
                col = 1
            else:
                col += 1
            if value == self.ui.new_values[i]:
                start = f"{row}.{(col - 1) * 6}"
                end = f"{row}.{(col - 1) * 6 + 5}"
                self.ui.found_values.append((start, end))
            counter += 1
        if self.ui.found_values:
            self.ui.text_widget.tag_add("highlight", self.ui.found_values[0][0], self.ui.found_values[0][1])
            self.ui.text_widget.see(self.ui.found_values[0][0])
            self.sync_text_to_2d()

    def find_next(self):
        if self.ui.found_values_counter < len(self.ui.found_values) - 1:
            self.ui.found_values_counter += 1
            self.ui.text_widget.tag_remove("highlight", "1.0", "end")
            self.ui.text_widget.tag_configure("highlight", background="#907900")
            if self.ui.found_values:
                self.ui.text_widget.tag_add("highlight", self.ui.found_values[self.ui.found_values_counter][0], self.ui.found_values[self.ui.found_values_counter][1])
                self.ui.text_widget.see(self.ui.found_values[self.ui.found_values_counter][0])
                self.sync_text_to_2d()

    def find_previous(self):
        if self.ui.found_values_counter > 0:
            self.ui.found_values_counter -= 1
            self.ui.text_widget.tag_remove("highlight", "1.0", "end")
            self.ui.text_widget.tag_configure("highlight", background="#907900")
            if self.ui.found_values:
                self.ui.text_widget.tag_add("highlight", self.ui.found_values[self.ui.found_values_counter][0], self.ui.found_values[self.ui.found_values_counter][1])
                self.ui.text_widget.see(self.ui.found_values[self.ui.found_values_counter][0])
                self.sync_text_to_2d()

    def sync_text_to_2d(self):
        if self.ui.found_values:
            row_index = int(self.ui.found_values[self.ui.found_values_counter][0].split('.')[0]) - 1
            col_index = int(self.ui.found_values[self.ui.found_values_counter][0].split('.')[1]) // 6

            start_index = row_index * self.ui.columns + col_index

            self.ui.current_frame = start_index
            from Module_2D import Mode2D
            self.mode2d = Mode2D(self)
            self.mode2d.draw_canvas(self.ui)
            self.mode2d.highlight_text(self.ui.x)