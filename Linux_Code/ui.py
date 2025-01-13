from tkinter import *
from tkinter import ttk
from customtkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LinOLS:
    def __init__(self, window):
        from text_view import TextView
        from Module_2D import Mode2D
        from Utilities import Utility
        from find_dialog import Find_Dialog
        from File_Import import FileImport
        from difference_dialog import DifferenceDialog
        from value_dialog import ValueDialog
        from text_addons import TextAddons
        from Module_3D import Mode3D
        from maps import Maps_Utility
        from value_dialog_3d import Value_Dialog_3D
        from hex_address_dialog import HexAddressDialog
        from map_properties_window import Map_properties
        from x_axis_properties_window import x_axis_properties
        from y_axis_properties_window import y_axis_properties

        self.window = window
        window.title("LinOLS")

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.width = 1500
        window.height = 600

        x = (screen_width / 2) - (window.width / 2)
        y = (screen_height / 2) - (window.height / 2)
        window.geometry(f"{window.width}x{window.height}+{int(x)}+{int(y)}")

        self.text_view_ = TextView(self)
        self.mode2d = Mode2D(self)
        self.utility = Utility(self)
        self.find_dialog = Find_Dialog(self)
        self.file_import = FileImport(self)
        self.diff_dialog = DifferenceDialog(self)
        self.value_dial = ValueDialog(self)
        self.text_addons = TextAddons(self)
        self.mode3d = Mode3D(self)
        self.maps = Maps_Utility(self)
        self.value_dialog_3d = Value_Dialog_3D(self)
        self.hex_address_dial = HexAddressDialog(self)
        self.map_properties = Map_properties(self)
        self.x_axis_properties = x_axis_properties(self)
        self.y_axis_properties = y_axis_properties(self)

        self.file_path = ""
        self.columns = 20
        self.num_rows = 55
        self.unpacked = []
        self.current_frame = 0
        self.x = 0
        self.percentage_num = 0
        self.total_rows = 0
        self.low_high = True
        self.open = False
        self.import_allow = False
        self.current_values = []
        self.found_values = []
        self.found_values_counter = 0
        self.new_path = ""
        self.imported_values = []
        self.differences = []
        self.differences_color = []
        self.ori_values = []
        self.index_differences = []
        self.start_time = 0
        self.running = True
        self.hold_time = 0.5
        self.new_values = []
        self.selected_count = 0
        self.values = []
        self.shift_count = 0
        self.end_time = 0
        self.edit_mode_active = False
        self.display_sel = False
        self.sel_start = 0
        self.sel_end = 0
        self.highlight_start = None
        self.return_text = False
        self.red_line = None
        self.difference_index = -1
        self.map_list_counter = 0
        self.start_index_maps = []
        self.end_index_maps = []
        self.maps_names = []
        self.signed_values = False
        self.map_values = []
        self.x_values = []
        self.y_values = []
        self.map_decimal = False
        self.x_axis_decimal = False
        self.y_axis_decimal = False
        self.new_width = 0

        window.config(bg="#333")

        window.option_add("*Font", "Nimbus_Sans 9")

        self.notebook = ttk.Notebook(window)
        style = ttk.Style()
        style.configure("TNotebook", background="#333")
        style.configure("TNotebook.Tab", background="#333", foreground="white")
        style.map("TNotebook.Tab", background=[('selected', '#555')])
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.setup_ui()

    def setup_ui(self):
        tab1 = Frame(self.notebook, bg="#333")
        self.notebook.add(tab1, text=" Text ")

        text_frame = Frame(tab1, bg="#333")
        text_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        self.text_widget = Text(text_frame, bg="#333333", bd=0, highlightthickness=0, fg="white", font=("Courier", 9))
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_widget.configure(insertbackground='white', undo=True)

        self.scroll_bar = CTkScrollbar(text_frame, command=self.text_widget.yview, fg_color="#333")
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        self.hex_address_menu = Menu(tab1, tearoff=0, bg="#333", fg="white")
        self.hex_address_menu.add_command(label="Copy Hex Address", command=self.text_addons.copy_hex_address)

        self.text_widget.bind("<Button-3>", self.text_addons.show_hex_address_menu)

        center_frame = CTkFrame(tab1, fg_color="#333")
        center_frame.grid(row=1, column=0, pady=5)

        buttons_frame = CTkFrame(tab1, fg_color="#333")
        buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        dec16_low_high = CTkButton(buttons_frame, text="16-bit Lo-Hi", width=6, hover_color="#555", fg_color="#444", text_color="white", command=lambda: self.text_view_.change_display_mode("low_high"))
        dec16_low_high.grid(row=0, column=0, padx=5, sticky="w")

        dec16_high_low = CTkButton(buttons_frame, text="16-bit Hi-Lo", width=6, hover_color="#555", fg_color="#444", text_color="white", command=lambda: self.text_view_.change_display_mode("high_low"))
        dec16_high_low.grid(row=0, column=1, padx=5)

        add_map_btn = CTkButton(buttons_frame, text="Add Map", width=6, hover_color="#555", fg_color="#444", text_color="white", command=self.maps.add_map)
        add_map_btn.grid(row=0, column=2, padx=5)

        button_2d = CTkButton(buttons_frame, text="Text to 2D", hover_color="#555", width=6, command=lambda: self.mode2d.text_to_2d(self), fg_color="#444", text_color="white")
        button_2d.grid(row=0, column=3, padx=5)

        self.selected_count_label = CTkButton(center_frame, text="Selected: 0", width=100, hover_color="#555", fg_color="#444", text_color="white")
        self.selected_count_label.grid(row=0, column=0, padx=10)

        '''COLUMNS FRAME'''
        columns_frame = CTkFrame(center_frame, border_color="#555", border_width=1, fg_color="#333")
        columns_frame.grid(row=0, column=1, padx=5)

        label_col = CTkLabel(columns_frame, text="Col:", width=3, height=2, fg_color="#333", text_color="white")
        label_col.grid(row=0, column=0, padx=5, pady=3)

        self.entry = CTkEntry(columns_frame, fg_color="#555", text_color="white", width=28)
        self.entry.grid(row=0, column=1, padx=5, pady=3)
        self.entry.insert(END, str(self.columns))

        apply_columns = CTkButton(columns_frame, text="Apply", width=6, hover_color="#555", command=lambda: self.utility.adjust_columns(self), fg_color="#444", text_color="white")
        apply_columns.grid(row=0, column=2, padx=5, pady=3)

        '''SHIFT FRAME'''
        shift_frame = CTkFrame(center_frame, border_color="#555", border_width=1, fg_color="#333")
        shift_frame.grid(row=0, column=2, padx=5)

        label_shift = CTkLabel(shift_frame, text="Shift:", width=3, height=2, fg_color="#333", text_color="white")
        label_shift.grid(row=0, column=0, padx=5, pady=3)

        self.entry_position = CTkEntry(shift_frame, fg_color="#555", text_color="white", width=28)
        self.entry_position.grid(row=0, column=1, padx=5, pady=3)
        self.entry_position.insert(0, "00")

        apply_position = CTkButton(shift_frame, text="Apply", width=6, hover_color="#555", fg_color="#444", text_color="white", command=lambda: self.utility.move_items(self))
        apply_position.grid(row=0, column=2, padx=5, pady=3)

        self.ori_value_label = CTkButton(center_frame, text="Ori: 00000", width=100, hover_color="#555", fg_color="#444", text_color="white")
        self.ori_value_label.grid(row=0, column=3, padx=10)

        '''EDIT BUTTONS'''
        edit_buttons = CTkFrame(tab1, fg_color="#333")
        edit_buttons.grid(row=1, column=0, padx=5, pady=5, sticky=E)

        copy_button = CTkButton(edit_buttons, text="Copy", hover_color="#555", width=6, command=self.utility.copy_values,  fg_color="#444", text_color="white")
        copy_button.grid(row=0, column=1, padx=5, sticky=E)

        paste_button = CTkButton(edit_buttons, text="Paste", hover_color="#555", width=6, command=lambda: self.utility.paste_values(self), fg_color="#444", text_color="white")
        paste_button.grid(row=0, column=2, padx=5, sticky=E)

        undo = CTkButton(edit_buttons, text="Undo", hover_color="#555", width=6, command=self.utility.undo, fg_color="#444", text_color="white")
        undo.grid(row=0, column=3, padx=5, sticky=E)

        redo = CTkButton(edit_buttons, text="Redo", hover_color="#555", width=6, command=self.utility.redo, fg_color="#444", text_color="white")
        redo.grid(row=0, column=4, padx=5, sticky=E)

        tab2 = Frame(self.notebook, bg="#333")
        self.notebook.add(tab2, text=" 2D ")

        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)

        self.fig.patch.set_facecolor('#333')
        self.ax.set_facecolor('#333')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=tab2)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, padx=0, pady=0, sticky='nsew')

        self.canvas.get_tk_widget().config(highlightthickness=0)

        self.canvas.mpl_connect("button_press_event", self.mode2d.on_canvas_click)

        self.canvas.mpl_connect("key_press_event", self.utility.on_key_press_2d)

        tab2.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure(0, weight=1)

        navigation_buttons_frame = CTkFrame(tab2, fg_color="#333")
        navigation_buttons_frame.grid(row=1, column=0, columnspan=6, pady=5, sticky=W)

        update_frame = CTkFrame(tab2, fg_color="#333")
        update_frame.grid(row=1, column=0, padx=5)

        center_frame_2d_spacing = CTkFrame(tab2, fg_color="#333")
        center_frame_2d_spacing.grid(row=1, column=0, padx=5, pady=5)

        center_frame_2d = CTkFrame(tab2, fg_color="#333")
        center_frame_2d.grid(row=1, column=0, padx=5, pady=5)

        right_frame_2d = CTkFrame(tab2, fg_color="#333")
        right_frame_2d.grid(row=1, column=0, padx=5, pady=5, sticky=E)

        prev_button = CTkButton(navigation_buttons_frame, text="<", hover_color="#555", width=60, command=self.mode2d.prev_page, fg_color="#444", text_color="white")
        prev_button.grid(row=0, column=0, padx=5)

        fast_backwards_button = CTkButton(navigation_buttons_frame, text="<<", hover_color="#555", width=60, command=lambda: self.mode2d.fast_movement("left"), fg_color="#444", text_color="white")
        fast_backwards_button.grid(row=0, column=1, padx=5)

        next_button = CTkButton(right_frame_2d, text=">", hover_color="#555", width=60, command=self.mode2d.next_page, fg_color="#444", text_color="white")
        next_button.grid(row=0, column=1, padx=5)

        fast_forward_button = CTkButton(right_frame_2d, text=">>", hover_color="#555", width=60, command=lambda: self.mode2d.fast_movement("right"), fg_color="#444", text_color="white")
        fast_forward_button.grid(row=0, column=0, padx=5)

        load_and_update_button = CTkButton(update_frame, text="Update", hover_color="#555", width=100, command=lambda: self.mode2d.update_2d(self), fg_color="#444", text_color="white")
        load_and_update_button.grid(row=0, column=0, padx=148)

        self.text_value = CTkButton(update_frame, text="Value: 00000", hover_color="#555", width=100, fg_color="#444", text_color="white")
        self.text_value.grid(row=0, column=2, padx=150)

        update_percentage = CTkButton(center_frame_2d_spacing, text="%", hover_color="#555", width=6, command=lambda: self.mode2d.percentage(True, "set"), fg_color="#444", text_color="white")
        update_percentage.grid(row=0, column=0, padx=58)

        update_percentage_1 = CTkButton(center_frame_2d_spacing, text="%", hover_color="#555", width=6, command=lambda: self.mode2d.percentage(True, "set"), fg_color="#444", text_color="white")
        update_percentage_1.grid(row=0, column=1, padx=60)

        percent_minus = CTkButton(center_frame_2d, text="-", width=3, hover_color="#555", command=lambda: self.mode2d.percentage(False, "minus"), fg_color="#444", text_color="white")
        percent_minus.grid(row=0, column=0, padx=5)

        self.percentage_entry = CTkEntry(center_frame_2d, width=28, fg_color="#555", text_color="white")
        self.percentage_entry.grid(row=0, column=1, padx=5)
        self.percentage_entry.insert(END, "00")

        percent_plus = CTkButton(center_frame_2d, text="+", width=3, hover_color="#555", command=lambda: self.mode2d.percentage(False, "plus"), fg_color="#444", text_color="white")
        percent_plus.grid(row=0, column=2, padx=5)

        tab1.grid_rowconfigure(0, weight=1)
        tab1.grid_columnconfigure(0, weight=1)

        tab3 = Frame(self.notebook, bg="#333")
        self.notebook.add(tab3, text=" 3D ")

        tab3.grid_rowconfigure(0, weight=1)
        tab3.grid_columnconfigure(0, weight=1)

        self.boxes = Frame(tab3, bg="#333")
        self.boxes.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        sign_btn = CTkButton(self.boxes, text="Sign", fg_color="#444", text_color="white", hover_color="#555", width=10, command=self.maps.sign_values)
        sign_btn.grid(row=0, column=0)

        self.main_frame = Frame(self.boxes, bg="#333")
        self.main_frame.grid(row=1, column=1, padx=10, sticky='nw')

        self.x_frame = Frame(self.boxes, bg="#333")
        self.x_frame.grid(row=0, column=1, padx=10, pady=8, sticky='nw')

        self.y_frame = Frame(self.boxes, bg="#333")
        self.y_frame.grid(row=1, column=0, sticky='nw')

        self.right_frame_3d = Frame(tab3, bg="#333")
        self.right_frame_3d.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.right_frame_3d.grid_rowconfigure(0, weight=1)
        self.right_frame_3d.grid_columnconfigure(0, weight=1)

        self.columns_3d = 10
        self.rows_3d = 10

        self.entry_x_widgets = []
        self.original_X = []
        row_x = []
        original_row_x = []
        for x in range(self.columns_3d):
            entry = Entry(self.x_frame, width=5, font=("Comfortaa", 10))
            entry.grid(row=0, column=x)
            entry.insert(END, "00000")
            entry.bind('<KeyRelease>', lambda event, j=x: self.mode3d.check_difference_x(event, j))
            entry.bind("<FocusOut>", lambda event, j=x: (self.mode3d.on_focus_out(event, 0, j, "x")))
            entry.bind("<ButtonPress-1>", lambda event, j=x: self.mode3d.start_interaction_x(event, j))
            entry.bind("<B1-Motion>", self.mode3d.drag_to_select)
            entry.bind("<ButtonRelease-1>", self.mode3d.end_interaction)
            entry.bind("<Control-a>", lambda event, j=x: self.mode3d.select_all(event, 0, j, "x"))
            entry.bind("<Tab>", self.mode3d.clear_highlight_on_tab)
            entry.bind("<Button-3>", self.x_axis_properties.show_context_menu)
            row_x.append(entry)
            original_row_x.append("00000")
        self.entry_x_widgets.append(row_x)
        self.original_X.append(original_row_x)

        self.right_click_map_menu = Menu(tab3, tearoff=0, bg="#333", fg="white")
        self.right_click_map_menu.add_command(label="Map Properties", command=self.map_properties.map_properties_dialog)

        self.right_click_x_axis = Menu(tab3, tearoff=0, bg="#333", fg="white")
        self.right_click_x_axis.add_command(label="X-Axis Properties", command=self.x_axis_properties.x_axis_properties_dialog)

        self.right_click_y_axis = Menu(tab3, tearoff=0, bg="#333", fg="white")
        self.right_click_y_axis.add_command(label="Y-Axis Properties", command=self.y_axis_properties.y_axis_properties_dialog)

        self.entry_widgets = []
        self.original = []
        for k in range(self.rows_3d):
            row = []
            original_row = []
            for x in range(self.columns_3d):
                entry = Entry(self.main_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=k, column=x)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>',
                           lambda event, i=k, j=x: (self.mode3d.check_difference(event, i, j), self.mode3d.check_difference_3d(i, j)))
                entry.bind("<FocusOut>", lambda event, i=k, j=x: (self.mode3d.on_focus_out(event, i, j, "map")))
                entry.bind("<ButtonPress-1>", lambda event, i=k, j=x: (
                    self.mode3d.start_interaction(event, i, j), self.mode3d.check_difference_3d(i, j)))
                entry.bind("<B1-Motion>", self.mode3d.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.mode3d.end_interaction)
                entry.bind("<Control-a>", lambda event, i=k, j=x: self.mode3d.select_all(event, i, j, "map"))
                entry.bind("<Tab>", self.mode3d.clear_highlight_on_tab)
                entry.bind("<Button-3>", self.map_properties.show_context_menu)
                row.append(entry)
                original_row.append("00000")
            self.entry_widgets.append(row)
            self.original.append(original_row)

        self.entry_y_widgets = []
        self.original_Y = []
        for x in range(self.rows_3d):
            entry = Entry(self.y_frame, width=5, font=("Comfortaa", 10))
            entry.grid(row=x, column=0)
            entry.insert(END, "00000")
            entry.bind('<KeyRelease>', lambda event, i=x: self.mode3d.check_difference_y(event, i))
            entry.bind("<FocusOut>", lambda event, i=x: (self.mode3d.on_focus_out(event, i, 0, "y")))
            entry.bind("<ButtonPress-1>", lambda event, i=x: self.mode3d.start_interaction_y(event, i))
            entry.bind("<B1-Motion>", self.mode3d.drag_to_select)
            entry.bind("<ButtonRelease-1>", self.mode3d.end_interaction)
            entry.bind("<Control-a>", lambda event, i=x: self.mode3d.select_all(event, i, 0, "y"))
            entry.bind("<Tab>", self.mode3d.clear_highlight_on_tab)
            entry.bind("<Button-3>", self.y_axis_properties.show_context_menu)
            self.entry_y_widgets.append(entry)
            self.original_Y.append("00000")

        self.fig_3d = plt.figure()
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')

        self.fig_3d.patch.set_facecolor('#333')
        self.ax_3d.set_facecolor('#333')

        self.ax_3d.xaxis.pane.fill = True
        self.ax_3d.yaxis.pane.fill = True
        self.ax_3d.zaxis.pane.fill = True
        self.ax_3d.xaxis.pane.set_facecolor('#333')
        self.ax_3d.yaxis.pane.set_facecolor('#333')
        self.ax_3d.zaxis.pane.set_facecolor('#333')

        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=self.right_frame_3d)
        self.canvas_widget_3d = self.canvas_3d.get_tk_widget()
        self.canvas_widget_3d.grid(row=0, column=0, sticky="nsew")

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selected_cells = set()

        mid_frame_3d = CTkFrame(tab3, fg_color="#333")
        mid_frame_3d.grid(row=1, column=0, columnspan=2)

        update_3d = CTkButton(mid_frame_3d, text="Update", command=self.maps.update_3d_from_text,
                                             fg_color="#444", text_color="white", hover_color="#555", width=80)
        update_3d.grid(row=0, column=0)

        self.label_diff_3d = CTkButton(mid_frame_3d, text="Diff: 0", width=80, fg_color="#444",
                                       text_color="white", hover_color="#555")
        self.label_diff_3d.grid(row=0, column=1, padx=10)

        row_frame_3d = CTkFrame(mid_frame_3d, border_color="#555", border_width=1, fg_color="#333")
        row_frame_3d.grid(row=0, column=2, padx=5)

        CTkLabel(row_frame_3d, text="Row:", fg_color="#333", text_color="white").grid(row=0, column=1, padx=5, pady=3)
        self.rows_entry = CTkEntry(row_frame_3d, width=28, fg_color="#555", text_color="white")
        self.rows_entry.insert(0, str(self.rows_3d))
        self.rows_entry.grid(row=0, column=2, padx=5, pady=3)
        self.rows_entry.configure(state="disabled")

        col_frame_3d = CTkFrame(mid_frame_3d, border_color="#555", border_width=1, fg_color="#333")
        col_frame_3d.grid(row=0, column=3, padx=5)

        CTkLabel(col_frame_3d, text="Col:", fg_color="#333", text_color="white").grid(row=0, column=0, padx=5, pady=3)
        self.columns_entry = CTkEntry(col_frame_3d, width=28, fg_color="#555", text_color="white")
        self.columns_entry.insert(0, str(self.columns_3d))
        self.columns_entry.grid(row=0, column=1, padx=5, pady=3)
        self.columns_entry.configure(state="disabled")

        value_dialog_3d_btn = CTkButton(mid_frame_3d, text="Value", command=self.value_dialog_3d.value_dialog,
                                                fg_color="#444", text_color="white", hover_color="#555", width=80)
        value_dialog_3d_btn.grid(row=0, column=4, padx=10)

        update_3d_button = CTkButton(mid_frame_3d, text="Write Map", command=self.maps.write_map,
                                       fg_color="#444", text_color="white", hover_color="#555", width=80)
        update_3d_button.grid(row=0, column=5)



        left_frame_3d = CTkFrame(tab3, fg_color="#333")
        left_frame_3d.grid(row=1, column=0, pady=5, sticky=W)

        copy_map_values_button = CTkButton(left_frame_3d, text="Copy Map", command=self.mode3d.copy_map_values,
                                             fg_color="#444", text_color="white", hover_color="#555", width=80)
        copy_map_values_button.grid(row=0, column=0, padx=5)

        copy_selected_button = CTkButton(left_frame_3d, text="Copy Selected", command=self.mode3d.copy_selected_cells,
                                           fg_color="#444", text_color="white", hover_color="#555", width=80)
        copy_selected_button.grid(row=0, column=1, padx=5)

        self.copy_x_axis_button = CTkButton(left_frame_3d, text="Copy X Axis", command=self.mode3d.copy_x_axis,
                                            fg_color="#444", text_color="white", hover_color="#555", width=80)
        self.copy_x_axis_button.grid(row=0, column=2, padx=5)

        self.copy_y_axis_button = CTkButton(left_frame_3d, text="Copy Y Axis", command=self.mode3d.copy_y_axis,
                                            fg_color="#444", text_color="white", hover_color="#555", width=80)
        self.copy_y_axis_button.grid(row=0, column=3, padx=5)


        east_frame_3d = CTkFrame(tab3, fg_color="#333")
        east_frame_3d.grid(row=1, column=0, columnspan=2, pady=5, sticky=SE)

        self.paste_x_button = CTkButton(east_frame_3d, text="Paste X Axis", command=lambda: self.mode3d.paste_x_data(False, [], False),
                                     fg_color="#444", text_color="white", hover_color="#555", width=80)
        self.paste_x_button.grid(row=0, column=0, padx=5)

        self.paste_y_button = CTkButton(east_frame_3d, text="Paste Y Axis", command=lambda: self.mode3d.paste_y_data(False, [], False),
                                     fg_color="#444", text_color="white", hover_color="#555", width=80)
        self.paste_y_button.grid(row=0, column=1, padx=5)

        paste_selected_3d_btn = CTkButton(east_frame_3d, text="Paste Selected", command=self.mode3d.paste_selected,
                                       fg_color="#444", text_color="white", hover_color="#555", width=80)
        paste_selected_3d_btn.grid(row=0, column=2, padx=5)

        self.paste_button = CTkButton(east_frame_3d, text="Paste Map", hover_color="#555", width=80,
                                    command=lambda: self.mode3d.paste_data(False, [], 0, 0, False, ""), fg_color="#444",
                                   text_color="white")
        self.paste_button.grid(row=0, column=3, padx=5)

        tab4 = Frame(self.notebook, bg="#333")
        self.notebook.add(tab4, text=" Maps ")

        self.map_list = Listbox(tab4, bg="#333", fg="white", font=10, highlightthickness=0)
        self.map_list.pack(fill=BOTH, expand=YES)

        self.map_list.bind('<Double-Button-1>', self.maps.on_double_click)

        self.remove_menu = Menu(tab4, tearoff=0, bg="#333", fg="white")
        self.remove_menu.add_command(label="Remove", command=self.maps.remove_item)

        self.map_list.bind("<Button-3>", self.maps.show_context_menu)

        self.window.bind("<Button-1>", self.maps.hide_context_menu)

        menu_bar = Menu(self.window, bg="#333", fg="white")
        self.window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0, bg="#333", fg="white")
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.text_view_.open_file(self))
        file_menu.add_command(label="Save", command=self.text_view_.save_file)

        options_menu = Menu(menu_bar, tearoff=0, bg="#333", fg="white")
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Find", command=self.find_dialog.find_dialog)
        options_menu.add_command(label="Import", command=lambda: self.file_import.import_file(self, False, ""))
        options_menu.add_command(label="Difference", command=lambda: self.diff_dialog.differences_dialog(self))
        options_menu.add_command(label="Value Changer", command=lambda event=None: self.value_dial.value_dialog(self, event))
        options_menu.add_command(label="Find Hex Address", command=self.hex_address_dial.hex_find_dialog)

        mappack_menu = Menu(menu_bar, tearoff=0, bg="#333", fg="white")
        menu_bar.add_cascade(label="Mappack", menu=mappack_menu)
        mappack_menu.add_command(label="Import Mappack", command=self.maps.import_map)
        mappack_menu.add_command(label="Export Mappack", command=self.maps.export_map)

        self.text_widget.bind("<Button-1>", self.text_addons.start_selection)
        self.text_widget.bind("<ButtonRelease-1>", self.text_addons.stop_drag)
        self.text_widget.bind("<Double-1>", self.text_addons.disable_double_click_selection)
        self.text_widget.bind("<Key>", self.text_addons.disable_user_input)
        self.text_widget.bind("<percent>", lambda event=None: self.value_dial.value_dialog(self, event))
        self.text_widget.bind("<e>", self.text_addons.edit_mode)
        self.text_widget.bind("<E>", self.text_addons.edit_mode)

        self.text_widget.bind('<Motion>', self.text_addons.update_selected_count)

        self.window.protocol("WM_DELETE_WINDOW", self.exit_app)

        self.clean_up()

    def clean_up(self):
        if self.new_path and os.path.exists(self.new_path):
            os.remove(self.new_path)
        file_path = "mappack.mp"
        if os.path.exists(file_path):
            os.remove(file_path)

    def exit_app(self, event=None):
        self.clean_up()
        self.window.quit()