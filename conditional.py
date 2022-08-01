from tkinter import *
from tkinter import ttk


class Conditional(Frame):
    def __init__(self, parent_frame, controller):
        super().__init__()
        self.n_check = False
        self.controller = controller
        self.entries = controller.conditional_entries
        self.conf = controller.config

        # self.conditional_enabled = BooleanVar()
        self.enable_conditional = ttk.Checkbutton(
            self,
            text="Add ConditionalSwitch",
            variable=self.controller.conditionals_enabled,
            command=self.update_grid
        )
        self.enable_conditional.selection_clear()
        self.enable_conditional.grid(row=0, column=0, columnspan=2, sticky=W)
        self.controller.conditionals_enabled.trace("w", self.update_grid)

        self.button_row = IntVar(value=2)
        self.bar_row = IntVar(value=2)

        self.add_condition_btn = ttk.Button(self, text="Add statement", command=self.add_condition)
        self.auto_fill_btn = ttk.Button(self, text="Auto-fill", command=self.auto_fill)
        self.grid(row=3, column=0, sticky=W, padx=(20, 0), pady=(3, 10), columnspan=2)

    def name_entry(self):
        ttk.Label(self, text="Image name: ").grid(row=1, column=0)
        name = ttk.Entry(self, width=25, textvariable=self.controller.conditional_image)
        name.grid(row=1, column=1, pady=(5, 5))
        # self.n_check = True

    def add_condition(self):
        statement = (Condition(self, self.controller))
        self.entries.append(statement)
        self.entries[-1].place(self.bar_row.get())
        self.update_grid()
        # self.cnd_list.append(Condition(self, self.cnd_list))
        # self.button_row.set(self.button_row.get() + 1)
        # self.cnd_list[-1].place_object(self.bar_row.get())
        # self.bar_row.set(self.bar_row.get() + 1)
        # self.grid_update()

    def auto_fill(self):
        valid = []
        if not self.controller.suffix_only_enabled.get():
            valid.append(self.controller.scene_name.get())
        for var in self.controller.alt_entries:
            if repr(var) != '':
                valid.append(repr(var))
        while len(self.entries) < len(valid):
            self.add_condition()
        for (string, condition) in zip(valid, self.entries):
            condition.insert(string)
        valid.clear()

    def update_grid(self, *args):
        if self.controller.conditionals_enabled.get():
            self.name_entry()
            self.bar_row.set(self.bar_row.get() + 1)
            self.add_condition_btn.grid(row=self.button_row.get(), column=0, pady=(10, 0))
            self.auto_fill_btn.grid(row=self.button_row.get(), column=1, pady=(10, 0))
            self.button_row.set(self.bar_row.get() + 1)
        else:
            for widget in self.winfo_children():
                if widget.winfo_class() != "TCheckbutton":
                    widget.grid_forget()
            self.entries.clear()
            self.bar_row.set(2)
            self.button_row.set(2)


class Condition(Frame):
    def __init__(self, frame, controller):
        super().__init__(frame)
        self.icon = PhotoImage(file="src/close_button.png")
        self.controller = controller
        self.attr = (
            ttk.Label(frame, text="Condition:"),
            ttk.Entry(frame, width=25),
            ttk.Label(frame, text="Image:"),
            ttk.Entry(frame, width=25),
            ttk.Button(frame, image=self.icon, command=self.delete),
            # Button(frame, text="Debug", command=self.debug)
        )

    def insert(self, string):
        """Insert condition"""
        self.attr[3].delete(0, END)
        self.attr[3].insert(0, string)

    def place(self, at):
        for widget in self.attr:
            widget.grid(row=at, column=self.attr.index(widget), padx=(5, 5), pady=(3, 0), sticky=E)

    def delete(self):
        for widget in self.attr:
            widget.grid_forget()
        self.controller.conditional_entries.remove(self)

    # def debug(self):
    #     print(self.parent.index(self))

    def condition(self):
        return self.attr[1].get()

    def image(self):
        return self.attr[3].get()
