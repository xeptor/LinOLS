from tkinter import *

class DifferenceDialog:
    def __init__(self, ui):
        self.ui = ui

    def differences_dialog(self, ui):
        self.ui = ui
        dialog_difference = Toplevel(bg="#333")
        dialog_difference.resizable(False, False)
        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()
        width = 305
        height = 335
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        dialog_difference.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        dialog_difference.title("Differences")
        label1 = Label(dialog_difference, text="New Values:", bg="#333", fg="white")
        label1.grid(row=0, column=0, padx=7, sticky=W, pady=5)
        self.list_box = Listbox(dialog_difference, height=18, width=20, bg="#333", fg="white", highlightthickness=0)
        self.list_box.grid(row=1, column=0, padx=5, sticky=W)
        label2 = Label(dialog_difference, text="Ori Values:", bg="#333", fg="white")
        label2.grid(row=0, column=1, padx=7, sticky=W, pady=5)
        self.list_box_ori = Listbox(dialog_difference, height=18, width=20, bg="#333", fg="white", highlightthickness=0)
        self.list_box_ori.grid(row=1, column=1, padx=5, sticky=W)

        self.difference_counter = Label(dialog_difference, bg="#333", fg="white", text=f"Differences: {len(self.ui.differences)}")
        self.difference_counter.grid(row=2, column=0, padx=25, pady=10, sticky=NSEW, columnspan=2)

        dialog_difference.grid_rowconfigure(2, weight=1)
        dialog_difference.grid_columnconfigure(2, weight=1)

        self.list_box.bind('<Double-Button-1>', self.highlight_difference)

        self.list_box.bind("<Button-4>", self.on_scroll_up)
        self.list_box.bind("<Button-5>", self.on_scroll_down)

        self.list_box_ori.bind("<Button-4>", self.on_scroll_up)
        self.list_box_ori.bind("<Button-5>", self.on_scroll_down)

        self.list_box.delete(0, END)
        self.list_box_ori.delete(0, END)

        for i in range(0, len(self.ui.differences), 1):
            value = f"{self.ui.differences[i]:05}"
            self.list_box.insert(END, value)
            self.list_box.itemconfig(i, fg=self.ui.differences_color[i])

        for i in range(0, len(self.ui.ori_values), 1):
            value = f"{self.ui.ori_values[i]:05}"
            self.list_box_ori.insert(END, value)

    def highlight_difference(self, event):
        selection = self.list_box.curselection()
        item = selection[0]
        index_sel = self.ui.index_differences[item] + self.ui.shift_count

        self.ui.current_frame = index_sel
        self.ui.red_line = 0

        from Module_2D import Mode2D
        self.mode2d = Mode2D(self)
        self.mode2d.draw_canvas(self.ui)
        self.mode2d.highlight_text(self.ui.x)

        self.ui.text_widget.tag_remove("highlight", 1.0, END)
        self.ui.text_widget.tag_configure("highlight", background="#907900")
        row = int(index_sel / self.ui.columns)
        col = index_sel - (self.ui.columns * (row + 1)) + self.ui.columns

        start = f"{row + 1}.{col * 6}"
        end = f"{row + 1}.{col * 6 + 5}"

        self.ui.text_widget.tag_add("highlight", start, end)
        self.ui.text_widget.see(start)
        self.ui.window.update_idletasks()

    def on_scroll_up(self, event):
        self.list_box.yview_scroll(-1, "units")
        self.list_box_ori.yview_scroll(-1, "units")
        return "break"

    def on_scroll_down(self, event):
        self.list_box.yview_scroll(1, "units")
        self.list_box_ori.yview_scroll(1, "units")
        return "break"