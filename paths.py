from tkinter import *
from pathlib import Path


class Paths(Frame):
    def __init__(self, app, params):
        super().__init__(app)
        self.ini = params
        Label(self, text="*.rpy file").grid(column=0, row=0, sticky='W', pady=(30, 0))
        self.rpy_file = StringVar()
        self.file_path = Entry(self, width=30, textvariable=self.rpy_file)
        self.file_path.grid(column=1, row=0, sticky='W', pady=(30, 0))
        self.file_path.insert(0, self.ini.return_rpy())
        # Scene name
        Label(self, text='Scene name:').grid(column=0, row=1, sticky='W')
        self.scene = StringVar()
        self.scene_entry = Entry(self, width=30, textvariable=self.scene)
        self.scene_entry.focus()
        self.scene_entry.grid(column=1, row=1, sticky='W')

        # Default timing
        self.default_timing = StringVar()

        Label(self, text="Timing: ").grid(column=2, row=1, sticky=W)
        self.timing_entry = Entry(self, width=5, textvariable=self.default_timing)
        self.timing_entry.grid(row=1, column=3, sticky=W, padx=(5, 15))
        self.timing_entry.insert(0, self.ini['Timing']['DefaultTiming'])

        # Select images
        self.image_files = StringVar()

        Label(self, text='Frames: ').grid(row=2, column=0, sticky="W")
        self.img_entry = Entry(self, width=30, textvariable=self.image_files)
        self.img_entry.grid(column=1, row=2)

        self.grid(row=0, column=0, padx=(20, 0), sticky=W)
