from tkinter import Frame
from tkinter import *
import tkinter as tk
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

        ttk.Label(self, text="Audio file: ").grid(row=1, column=0, pady=(3, 8), padx=(0, 2), sticky="w")
        self.entry = ttk.Entry(self, width=30)
        self.entry.grid(row=1, column=1, pady=(3, 8), sticky=W, columnspan=4)
        self.plus_icon = PhotoImage(file="src/open.png")
        self.add_btn = Button(self, image=self.plus_icon, command=self.controller.select_audio, borderwidth=0)
        self.add_btn.grid(row=1, column=5, pady=(3, 8), padx=(2, 5), sticky="w")
        self.timing_option = StringVar()

        ttk.Label(self, text="Start at: ").grid(row=2, column=0, padx=(0, 2), sticky=W)
        self.start_at = ttk.Entry(self, width=5)
        self.start_at.grid(row=2, column=1, sticky=W)

        ttk.Label(self, text="Repeat every ").grid(row=2, column=2, padx=2)
        self.spacing = ttk.Entry(self, width=5)
        self.spacing.grid(row=2, column=3, padx=(0, 3))

        self.spacing_choice = ttk.Combobox(self,
                                           state="readonly",
                                           textvariable=self.timing_option,
                                           values=('Frames', 'Seconds', 'Don\'t repeat'),
                                           width=12
                                           )
        self.spacing_choice.current(0)
        self.spacing_choice['state']="readonly"
        self.spacing_choice.grid(row=2, column=4, columnspan=2)

        self.controller.insert_audio.trace_add('write', self.place)
        self.controller.audio_file.trace_add('write', self.entry_insert)
        self.disable_widgets()
        # self.columnconfigure(0, weight=0)
        self.grid(row=1, column=0, padx=(20, 0), sticky=W)

    def place(self, *args):
        if self.controller.insert_audio.get():
            for widget in self.winfo_children():
                try:
                    if widget.winfo_class() != 'TCheckbutton':
                        if widget.winfo_class() == 'TCombobox':
                            widget['state'] = "readonly"
                        else:
                            widget['state'] = 'active'
                except AttributeError:
                    widget.config(state=NORMAL)
        else:
            self.disable_widgets()

    def disable_widgets(self):
        for widget in self.winfo_children():
            try:
                if widget.winfo_class() != 'TCheckbutton':
                    widget['state'] = 'disabled'
            except AttributeError:
                widget.config(state=DISABLED)

    def entry_insert(self, *args):
        self.entry.insert(0, str(Path(self.controller.audio_file.get()).stem))
