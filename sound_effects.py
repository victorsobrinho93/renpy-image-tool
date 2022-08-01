from tkinter import Frame
from tkinter import *
from tkinter import ttk
from pathlib import Path

class SoundEffects(Frame):
    def __init__(self, app, controller):
        super().__init__()
        self.controller = controller
        self.conf = controller.config

        # Insert audio file.
        self.enable_audio = ttk.Checkbutton(
            self,
            text="Add sound effects",
            variable=self.controller.insert_audio
        )
        self.enable_audio.selection_clear()
        self.enable_audio.grid(column=0, row=0, pady=(0, 5), sticky=W, columnspan=2)

        self.f_label = ttk.Label(self, text="Audio file: ")
        self.entry = ttk.Entry(self, width=30)
        self.plus_icon = PhotoImage(file="src/open.png")
        self.add_btn = Button(self, image=self.plus_icon, command=self.controller.select_audio, border=0)
        self.s_label = ttk.Label(self, text="Timing: ")
        self.timing = ttk.Entry(self, width=5, textvariable=self.controller.audio_timing)
        self.controller.insert_audio.trace_add('write', self.place)
        self.controller.audio_file.trace_add('write', self.entry_insert)

        # self.columnconfigure(0, weight=0)
        self.grid(row=1, column=0, padx=(20, 0), sticky=W)

    def place(self, *args):
        if self.controller.insert_audio.get():
            col = 0
            for widget in self.winfo_children():
                if widget.winfo_class() != 'TCheckbutton':
                    widget.grid(row=1, column=col, pady=(3, 8), padx=2, sticky="w")
                    if widget.winfo_class() == 'Button':
                        widget.grid_configure(padx=(2, 5))
                    col += 1
        else:
            for widget in self.winfo_children():
                if widget.winfo_class() != 'TCheckbutton':
                    widget.grid_forget()

    def entry_insert(self, *args):
        self.entry.insert(0, str(Path(self.controller.audio_file.get()).stem))
