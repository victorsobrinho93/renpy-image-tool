from tkinter import *


class FileEntry(Frame):
    def __init__(self, frame, controller):
        super().__init__(frame)
        self.controller = controller
        self.conf = controller.config

        self.rpy_var = StringVar()
        Label(self, text="*.rpy file").grid(column=0, row=0, sticky='W', pady=(30, 0))
        self.rpy_entry = Entry(self, width=30, textvariable=self.rpy_var)
        self.rpy_entry.grid(column=1, row=0, sticky='W', pady=(30, 0))

        self.scene_var = StringVar()
        Label(self, text='Scene name:').grid(column=0, row=1, sticky='W')
        self.scene_entry = Entry(self, width=30, textvariable=self.scene_var)
        self.scene_entry.focus()
        self.scene_entry.grid(column=1, row=1, sticky='W')

        # Default timing
        self.timing_var = StringVar()
        Label(self, text="Timing: ").grid(column=2, row=1, sticky=W)
        self.timing_entry = Entry(self, width=5, textvariable=self.timing_var)
        self.timing_entry.grid(row=1, column=3, sticky=W, padx=(5, 15))
        self.timing_entry.insert(0, self.conf.timing_insert())

        # Select images
        self.images_var = StringVar()
        Label(self, text='Frames: ').grid(row=2, column=0, sticky="W")
        self.images_entry = Entry(self, width=30, textvariable=self.images_var)
        self.images_entry.grid(column=1, row=2)

        self.grid(row=0, column=0, padx=(20, 0), sticky=W)
