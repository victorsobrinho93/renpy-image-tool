from tkinter import *
from buttons import Buttons
from PIL import ImageTk, Image

from preview import Preview


class Alternative(Frame):
    def __init__(self, app, paths, params):
        super().__init__(app)
        self.ini = params
        self.name = paths.scene_entry
        self.alt = None
        self.last_row = None
        self.output_alternative = StringVar()
        self.check_alternative = Checkbutton(
            self,
            text="Alternative timings",
            variable=self.output_alternative,
            # command=lambda: print("Nothing for now")
        )
        self.check_alternative.deselect()
        self.check_alternative.grid(column=0, row=0, sticky="w", columnspan=2, pady=(5, 5))

        # Giving the user the choice to only output suffixed scenes
        self.suffix = BooleanVar()
        self.suffix_only = Checkbutton(
            self,
            text="Suffixed only",
            variable=self.suffix,
            state=DISABLED
        )
        self.suffix_only.deselect()
        self.suffix_only.grid(column=3, row=0, sticky=W, columnspan=2, pady=(5, 5))

        self.alt_list = []

        self.bar_row = IntVar(value=1)
        self.button_row = IntVar(value=2)

        self.add = Button(self, text="Add scene", command=self.add_alternative)
        # self.add.grid(row=self.row.get() + 1, column=0, sticky=W, pady=(5, 5))

        self.output_alternative.trace("w", self.alt_enabled)
        self.columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky=W, padx=(20, 0))

    def add_alternative(self):
        self.alt_list.append(AlternativeObject(self, scene_name=self.name, alt_list=self.alt_list))
        self.alt_list[-1].place_object(self.bar_row.get())
        self.grid_update()

    def alt_enabled(self, *args):
        if self.output_alternative.get() == '1':
            self.add.grid(row=self.button_row.get(), column=0, sticky=W, pady=(5, 5))
            self.suffix_only.config(state=NORMAL)
        else:
            self.suffix_only.deselect()
            self.suffix_only.config(state=DISABLED)
            for widget in self.winfo_children():
                if widget.winfo_class() != "Checkbutton":
                    widget.grid_forget()
            # self.add.grid_forget()

    def grid_update(self):
        self.bar_row.set(self.bar_row.get() + 1)
        self.button_row.set(self.button_row.get() + 1)
        self.add.grid(row=self.button_row.get(), column=0, sticky=W, pady=(15, 5))

    # def return_ids(self):
    #     for widget in self.winfo_children():
    #         print(widget)


class AlternativeObject(Frame):
    def __init__(self, frame, scene_name, alt_list):
        super().__init__(frame)
        self.name = scene_name
        self.parent = alt_list
        self.play_button = PhotoImage(file="play_button.png")
        self.delete_button = PhotoImage(file="close_button.png")
        self.attr = (
            Label(frame, text="Suffix: "),
            Entry(frame, width=15),
            Label(frame, text="Timing: "),
            Entry(frame, width=5),
            Button(frame, image=self.delete_button, command=self.delete_object),
            Button(frame, image=self.play_button, state=DISABLED)
        )

    def place_object(self, at):
        for widget in self.attr:
            widget.grid(row=at, column=self.attr.index(widget), padx=(5, 5), pady=(2, 0), sticky=E)

    def delete_object(self):
        for widget in self.attr:
            widget.grid_forget()
        self.parent.remove(self)

    def return_values(self):
        # This can be improved for readability
        if self.attr[1].get():
            if self.if_num(self.attr[3].get()):
                return self.attr[1].get(), self.attr[3].get()

    def __repr__(self):
        if self.name.get() == '' or self.attr[1].get() == '':
            return ''
        return f"{self.name.get()}_{self.attr[1].get()}"

    def if_num(self, num):
        try:
            return float(num)
        except ValueError:
            return False

    def alt_name(self):
        # Return scene name for auto-fill
        return f"{self.name.get()}_{self.attr[1].get()}"
