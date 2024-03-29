from tkinter import *
from tkinter import ttk


class Alternative(Frame):
    def __init__(self, parent_frame, controller):
        super().__init__()
        self.controller = controller
        self.alt_entries = controller.alt_entries
        self.conf = controller.config
        self.enable_alternatives = ttk.Checkbutton(
            self,
            text="Alternative timings",
            variable=self.controller.alt_scenes_enabled,
        )
        self.enable_alternatives.selection_clear()
        self.enable_alternatives.grid(column=0, row=0, sticky="w", columnspan=2, pady=(5, 5))
        self.controller.alt_scenes_enabled.trace_add('write', self.alternative_options)

        self.filter_suffix = ttk.Checkbutton(
            self,
            text="Suffixed only",
            variable=self.controller.suffix_only_enabled,
            state=DISABLED
        )
        self.filter_suffix.selection_clear()
        self.filter_suffix.grid(column=2, row=0, sticky=W, columnspan=2, pady=(5, 5), padx=3)

        self.bar_row = IntVar(value=1)
        self.button_row = IntVar(value=2)

        self.add_entry = ttk.Button(self, text="Add alternative", command=self.add_alternative)
        self.columnconfigure(0, weight=1)
        self.grid(row=2, column=0, sticky=W, padx=(20, 0))

    def add_alternative(self):
        entry = AlternativeEntry(self, self.controller)
        self.controller.alt_entries.append(entry)
        self.controller.alt_entries[-1].post_init()
        self.controller.alt_entries[-1].place(self.bar_row.get())
        # self.alt_entries.append(AlternativeEntry(self, self.controller).place(self.bar_row.get()))
        self.update_grid()

    def alternative_options(self, *args):
        if self.controller.alt_scenes_enabled.get():
            self.add_entry.grid(row=1, column=0, sticky=W, pady=(5, 5), columnspan=2)
            self.filter_suffix.config(state=NORMAL)
        else:
            self.filter_suffix.config(state=DISABLED)
            self.controller.suffix_only_enabled.set(value=False)
            for widget in self.winfo_children():
                if widget.winfo_class() != 'TCheckbutton':
                    widget.grid_forget()
            self.controller.alt_entries.clear()
            self.bar_row.set(value=1)
            self.button_row.set(value=2)
            # This is going to clear the list when I uncheck the option,
            # I might change this once the rebuilding is done.

    def update_grid(self):
        self.add_entry.grid(row=self.button_row.get(), column=0, sticky=W, pady=(15, 0))
        self.bar_row.set(value=self.add_entry.grid_info()['row'])
        self.button_row.set(value=self.bar_row.get() + 1)


class AlternativeEntry(Frame):
    def __init__(self, frame, controller):
        super().__init__()
        self.controller = controller
        self.config = controller.config
        # self.entry_id = ''.join(choices(letters + digits, k=20))
        # I'm aware I'm overcomplicating things. But I'm trying something different.
        self.play_button = PhotoImage(file="src/play_button.png")
        self.delete_button = PhotoImage(file="src/close_button.png")
        self.alt_handle = StringVar()
        self.alt_timing = StringVar()
        self.attr = (
            ttk.Label(frame, text="Suffix: "),
            ttk.Entry(frame, width=15, textvariable=self.alt_handle),
            ttk.Label(frame, text="Timing: "),
            ttk.Entry(frame, width=5, textvariable=self.alt_timing),
            ttk.Button(frame, image=self.delete_button, command=self.delete),
            ttk.Button(frame,
                       image=self.play_button,
                       state=DISABLED,
                       command=lambda: self.controller.preview_scene(self.alt_timing)
                       )
        )

        self.alt_handle.trace_add('write', self.store_handle)
        self.alt_timing.trace_add('write', self.enable_preview)
        self.alt_timing.trace_add('write', self.store_timing)

    def post_init(self):
        object_index = self.controller.alt_entries.index(self)
        if self.config.has_option('Parameters', f"alt_handle_{object_index}"):
            self.alt_handle.set(self.config['Parameters'][f"alt_handle_{object_index}"])
        if self.config.has_option('Parameters', f"alt_timing_{object_index}"):
            self.alt_timing.set(self.config['Parameters'][f"alt_timing_{object_index}"])

    def store_handle(self, *args):
        handle = f"alt_handle_{self.controller.alt_entries.index(self)}"
        if not self.config.has_option('Parameters', handle):
            self.config['Parameters'] = {handle: self.alt_handle.get()}
        else:
            self.config.export(handle, self.alt_handle.get())

    def store_timing(self, *args):
        timing = f"alt_timing_{self.controller.alt_entries.index(self)}"
        if not self.config.has_option('Parameters', timing):
            self.config['Parameters'] = {timing: self.alt_timing.get()}
        else:
            self.config.export(timing, self.alt_timing.get())

    def enable_preview(self, *args):
        if self.controller.is_num(self.alt_timing.get()):
            self.attr[5].config(state=NORMAL)
        else:
            self.attr[5].config(state=DISABLED)

    def place(self, at):
        for widget in self.attr:
            widget.grid(row=at, column=self.attr.index(widget), padx=(3, 3), pady=(2, 0), sticky=W)

    def delete(self):
        for widget in self.attr:
            widget.grid_forget()
        self.controller.alt_entries.remove(self)

    def suffix(self):
        if self.attr[1].get():
            return self.attr[1].get()

    def timing(self):
        if self.controller.is_num(self.attr[3].get()):
            return self.attr[3].get()

    def __repr__(self):
        if self.controller.scene_name.get() == '' or self.attr[1].get() == '':
            return ''
        return f"{self.controller.scene_name.get()}_{self.attr[1].get()}"
