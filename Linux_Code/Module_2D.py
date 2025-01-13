from tkinter import *
from tkinter import messagebox
import numpy as np
import time

class Mode2D:
    def __init__(self, ui):
        self.ui = ui
        self.last_page_change_time = 0

    def scale_to_fixed_range(self, data, min_val=0, max_val=65535):
        return [min(max(val, min_val), max_val) for val in data]

    def draw_canvas(self, ui):
        self.ui = ui
        self.ui.ax.clear()

        start_index = self.ui.current_frame
        end_index_mod = min(start_index + self.ui.num_rows * self.ui.columns, len(self.ui.new_values))
        data_unpacked_mod = self.ui.new_values[start_index:end_index_mod]

        data_unpacked = self.ui.unpacked[start_index:end_index_mod]

        scaled_data_mod = self.scale_to_fixed_range(data_unpacked_mod)
        scaled_data = self.scale_to_fixed_range(data_unpacked)

        scaled_data_mod = np.array(scaled_data_mod)
        scaled_data = np.array(scaled_data)

        mask = scaled_data_mod != scaled_data

        self.ui.ax.plot(scaled_data_mod, color="white", linewidth=0.5)

        if np.any(mask):
            differing_indices = np.where(mask)[0]
            segments = np.split(differing_indices, np.where(np.diff(differing_indices) != 1)[0] + 1)

            for segment in segments:
                self.ui.ax.plot(segment, scaled_data_mod[segment], color="red", linewidth=0.5)

        if self.ui.red_line is not None:
            self.ui.ax.axvline(self.ui.red_line, color="#bd090e", linestyle='-', label="Clicked Position")

        if self.ui.display_sel:
            self.ui.ax.axvspan(self.ui.sel_start, self.ui.sel_end, color="#555", alpha=0.3, label="Selected Area")

        start_maps = self.ui.start_index_maps
        end_maps = self.ui.end_index_maps

        frame = self.ui.num_rows * self.ui.columns
        for i in range(len(self.ui.start_index_maps)):
            ok = False

            start = start_maps[i]
            end = end_maps[i]

            if (end - start_index) >= 0:
                ok = True
                temp = end - start_index
                if temp <= start_index + frame:
                    end = temp

            if (start - start_index) >= 0 and ok:
                temp = start - start_index
                if temp <= start_index + frame:
                    start = temp
            else:
                start = 0

            if ok:
                self.ui.ax.axvspan(start, end, color="#907900", alpha=0.3, label=f"{self.ui.maps_names[i]}")

        self.ui.ax.set_xlim(0, len(scaled_data_mod))
        self.ui.ax.set_ylim(0, 65535)

        self.ui.ax.axis('off')
        self.ui.ax.grid(True, which='both', color='white', linestyle='-', linewidth=0.5)

        self.ui.canvas.draw()

        if self.ui.return_text:
            self.scroll_to_highlight(self.ui)
            self.ui.return_text = False
        self.ui.display_sel = False

    def highlight_text(self, x):
        if self.ui.current_frame > 0:
            value_index = x + self.ui.current_frame
        else:
            value_index = x
        self.ui.text_widget.tag_remove("highlight", 1.0, END)
        self.ui.text_widget.tag_configure("highlight", background="#907900")

        row = value_index // self.ui.columns
        col = value_index % self.ui.columns

        start = f"{row + 1}.{col * 6}"
        end = f"{row + 1}.{(col + 1) * 6 - 1}"

        self.ui.text_widget.tag_add("highlight", start, end)
        self.ui.text_widget.see(start)

        self.ui.highlight_start = value_index
        value = self.ui.current_values[x + self.ui.current_frame]

        self.ui.text_value.configure(text=f"Value: {value:05}")

        self.ui.window.update_idletasks()

    def on_canvas_click(self, event):
        if not self.ui.unpacked:
            return
        x_pos = event.xdata
        if x_pos is not None:
            self.ui.display_sel = False
            self.ui.red_line = int(x_pos)
            self.highlight_text(self.ui.red_line)
            self.draw_canvas(self.ui)

    def prev_page(self):
        current_time = time.time()
        if current_time - self.last_page_change_time < 0.12:
            return
        if self.ui.current_frame - self.ui.num_rows * self.ui.columns >= 0:
            self.ui.current_frame -= self.ui.num_rows * self.ui.columns
            if self.ui.text_widget.tag_ranges(SEL):
                self.ui.text_widget.tag_remove(SEL, 1.0, END)
            self.draw_canvas(self.ui)

    def next_page(self):
        current_time = time.time()
        if current_time - self.last_page_change_time < 0.12:
            return
        if self.ui.current_frame + self.ui.num_rows * self.ui.columns < len(self.ui.unpacked):
            self.ui.current_frame += self.ui.num_rows * self.ui.columns
            if self.ui.text_widget.tag_ranges(SEL):
                self.ui.text_widget.tag_remove(SEL, 1.0, END)
            self.draw_canvas(self.ui)

    def fast_movement(self, direction):
        current_time = time.time()
        if current_time - self.last_page_change_time < 0.12:
            return
        if self.ui.text_widget.tag_ranges(SEL):
            self.ui.text_widget.tag_remove(SEL, 1.0, END)
        if direction == "right":
            self.ui.current_frame += 200
            self.draw_canvas(self.ui)
        elif direction == "left":
            self.ui.current_frame -= 200
            if self.ui.current_frame > 0:
                self.draw_canvas(self.ui)
            else:
                self.ui.current_frame = 0
                self.draw_canvas(self.ui)

    def percentage(self, entry, arg):
        if entry:
            try:
                num = int(self.ui.percentage_entry.get())
                if num < 0 or num > 100:
                    raise ValueError
                self.ui.percentage_num = num
            except ValueError:
                messagebox.showerror("Error", "Enter a correct value! (0% - 100%)")
                return
        else:
            if arg == "plus" and self.ui.percentage_num < 99:
                self.ui.percentage_num += 1
                num = self.ui.percentage_num
                self.ui.percentage_entry.delete(0, END)
                self.ui.percentage_entry.insert(END, f"{self.ui.percentage_num:02}")
            elif arg == "minus" and self.ui.percentage_num > 0:
                self.ui.percentage_num -= 1
                num = self.ui.percentage_num
                self.ui.percentage_entry.delete(0, END)
                self.ui.percentage_entry.insert(END, f"{self.ui.percentage_num:02}")
            else:
                num = 0
        if 0 < num <= 100:
            self.ui.current_frame = int((len(self.ui.unpacked) - self.ui.num_rows * self.ui.columns) * (num / 100))
            if self.ui.text_widget.tag_ranges(SEL):
                self.ui.text_widget.tag_remove(SEL, 1.0, END)
            self.draw_canvas(self.ui)

    def update_2d(self, ui):
        self.ui = ui
        from File_Import import FileImport
        self.file_import = FileImport(self)
        self.file_import.temp_safe(self.ui)
        self.draw_canvas(self.ui)

    def scroll_to_highlight(self, ui):
        self.ui = ui
        if self.ui.highlight_start is not None:
            self.ui.text_widget.tag_remove("highlight", 1.0, END)
            row = self.ui.highlight_start // self.ui.columns
            col = self.ui.highlight_start % self.ui.columns

            start = f"{row + 1}.{col * 6}"
            end = f"{row + 1}.{(col + 1) * 6 - 1}"

            self.ui.text_widget.tag_add("highlight", start, end)
            self.ui.text_widget.see(start)


    def text_to_2d(self, ui):
        self.ui = ui
        if self.ui.text_widget.tag_ranges(SEL):
            sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(sel_start, sel_end).strip()
            selected_count = len(selected_text.split())

            if len(selected_text) == 5:
                text = str(sel_start)
                parts = text.split('.')
                row = int(parts[0]) - 1
                col = int(parts[1]) // 6

                self.ui.display_sel = False

                index = row * self.ui.columns + col
                frame = self.ui.num_rows * self.ui.columns
                frames_num = index // frame
                self.ui.current_frame = frames_num * frame

                if self.ui.current_frame > 0:
                    self.ui.red_line = int(index) - self.ui.current_frame
                else:
                    self.ui.red_line = int(index)

                self.ui.text_widget.tag_remove("highlight", 1.0, END)
                self.ui.text_widget.tag_configure("highlight", background="#907900")
                self.ui.text_widget.tag_add("highlight", sel_start, sel_end)
                self.ui.text_widget.see(sel_start)

                self.ui.highlight_start = index
                value = self.ui.current_values[index]
                self.ui.text_value.configure(text=f"Value: {value:05}")

            if 1 < selected_count <= 1000:
                text_start = str(sel_start)
                parts_start = text_start.split('.')
                row_start = int(parts_start[0]) - 1
                col_start = int(parts_start[1]) // 6

                index = row_start * self.ui.columns + col_start
                frame = self.ui.num_rows * self.ui.columns
                frames_num = index // frame
                self.ui.current_frame = frames_num * frame

                if self.ui.current_frame > 0:
                    self.ui.sel_start = int(index) - self.ui.current_frame
                else:
                    self.ui.sel_start = int(index)

                self.ui.sel_end = self.ui.sel_start + selected_count - 1

                self.ui.display_sel = True

            self.draw_canvas(self.ui)