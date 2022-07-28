from tkinter import *
from PIL import ImageTk, Image


class Conditional(Frame):
    def __init__(self, app, paths, alt, params):
        super().__init__(app)
        self.ini = params
        self.alt = alt.alt_list
        #Band-aiding a fix for the name_entry issue
        self.n_check = False
        self.name = None
        self.output_cswitch = BooleanVar()
        self.check_cswitch = Checkbutton(
            self,
            text="Add ConditionalSwitch",
            variable=self.output_cswitch,
            command=self.grid_update
        )
        self.button_row = IntVar(value=2)
        self.bar_row = IntVar(value=2)
        self.check_cswitch.deselect()
        self.check_cswitch.grid(row=0, column=0, columnspan=2, sticky=W)
        self.add = Button(self, text="Add condition", command=self.add_condition)
        self.auto = Button(self, text="Auto-fill", command=self.auto_fill)
        self.output_cswitch.trace("w", self.grid_update)
        self.cnd_list = []
        self.grid(row=2, column=0, sticky=W, padx=(20, 0))



    def name_entry(self):
        Label(self, text="Image name: ").grid(row=1, column=0)
        self.name = Entry(self, width=25)
        self.name.grid(row=1, column=1)
        self.n_check = True

    def add_condition(self, **auto):
        self.cnd_list.append(Condition(self))
        self.button_row.set(self.button_row.get() + 1)
        self.cnd_list[-1].place_object(self.bar_row.get())
        self.bar_row.set(self.bar_row.get() + 1)
        self.grid_update()

    def auto_fill(self):
        #TODO: Add length check so new lines aren't created if not necessary
        for var in self.alt:
            self.cnd_list.append(Condition(self))
            self.button_row.set(self.button_row.get() + 1)
            self.cnd_list[-1].place_object(self.bar_row.get())
            self.cnd_list[-1].attr[3].insert(0, var.alt_name())
            self.bar_row.set(self.bar_row.get() + 1)
            self.grid_update()



    def grid_update(self, *args):
        if self.output_cswitch.get():
            if not self.n_check:
                self.name_entry()
            self.add.grid(row=self.button_row.get(), column=0, pady=(5, 5))
            self.auto.grid(row=self.button_row.get(), column=1, pady=(5, 5))
        else:
            self.n_check = False
            for widget in self.winfo_children():
                if widget.winfo_class() != "Checkbutton":
                    widget.grid_forget()


class Condition(Frame):
    def __init__(self, frame):
        super().__init__(frame)
        self.icon = PhotoImage(file="close_button.png")
        self.attr = (
            Label(frame, text="Condition:"),
            Entry(frame, width=25),
            Label(frame, text="Image:"),
            Entry(frame, width=25),
            Button(frame, image=self.icon, command=self.delete_object)
        )

    def place_object(self, at):
        for widget in self.attr:
            widget.grid(row=at, column=self.attr.index(widget), padx=(5, 5), pady=(2, 0), sticky=E)

    def delete_object(self):
        for widget in self.attr:
            widget.grid_forget()


    def return_condition(self):
        return self.attr[1].get()

    def return_scene(self):
        return self.attr[3].get()

