from tkinter import *


class Alternative(Frame):
    def __init__(self, parent_frame, controller):
        super().__init__()
        self.controller = controller
        self.alt_entries = controller.alt_entries
        self.conf = controller.config
        self.enable_alternatives = Checkbutton(
            self,
            text="Alternative timings",
            variable=self.controller.alt_scenes_enabled,
        )
        self.enable_alternatives.deselect()
        self.enable_alternatives.grid(column=0, row=0, sticky="w", columnspan=2, pady=(5, 5))
        self.controller.alt_scenes_enabled.trace_add('write', self.alternative_options)

        self.filter_no_suffix = Checkbutton(
            self,
            text="Suffixed only",
            variable=self.controller.suffix_only_enabled,
            state=DISABLED
        )
        self.filter_no_suffix.deselect()
        self.filter_no_suffix.grid(column=3, row=0, sticky=W, columnspan=2, pady=(5, 5))

        self.bar_row = IntVar(value=1)
        self.button_row = IntVar(value=2)

        self.add_entry = Button(self, text="Add alternative", command=self.add_alternative)
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky=W, padx=(20, 0))

    def add_alternative(self):
        entry = AlternativeEntry(self, self.controller)
        self.controller.alt_entries.append(entry)
        self.controller.alt_entries[-1].place(self.bar_row.get())
        # self.alt_entries.append(AlternativeEntry(self, self.controller).place(self.bar_row.get()))
        self.update_grid()

    def alternative_options(self, *args):
        if self.controller.alt_scenes_enabled.get():
            self.add_entry.grid(row=1, column=0, sticky=W, pady=(5, 5))
            self.filter_no_suffix.config(state=NORMAL)
        else:
            self.filter_no_suffix.deselect()
            self.filter_no_suffix.config(state=DISABLED)
            for widget in self.winfo_children():
                if widget.winfo_class() != 'Checkbutton':
                    widget.grid_forget()
            self.controller.alternative_objects.clear()
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
        # self.entry_id = ''.join(choices(letters + digits, k=20))
        # I'm aware I'm overcomplicating things. But I'm trying something different.
        self.play_button = PhotoImage(file="src/play_button.png")
        self.delete_button = PhotoImage(file="src/close_button.png")
        self.alt_timing = StringVar()
        self.attr = (
            Label(frame, text="Suffix: "),
            Entry(frame, width=15),
            Label(frame, text="Timing: "),
            Entry(frame, width=5, textvariable=self.alt_timing),
            Button(frame, image=self.delete_button, command=self.delete),
            Button(frame,
                   image=self.play_button,
                   state=DISABLED,
                   command=lambda: self.controller.preview_scene(self.alt_timing)
                   )
        )

        self.alt_timing.trace_add('write', self.enable_preview)

    def enable_preview(self, *args):
        if self.controller.is_num(self.alt_timing.get()):
            self.attr[5].config(state=NORMAL)
        else:
            self.attr[5].config(state=DISABLED)

    def place(self, at):
        for widget in self.attr:
            widget.grid(row=at, column=self.attr.index(widget), padx=(5, 5), pady=(2, 0), sticky=E)

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
