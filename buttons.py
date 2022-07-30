from tkinter import *
from tkinter import filedialog
from preview import Preview
from pathlib import Path


class Buttons(Frame):
    def __init__(self, parent_frame, controller):
        super().__init__(parent_frame)
        self.controller = controller
        self.conf = controller.config

        Button(self, text='Open File', command=self.controller.open_rpy).grid(column=0, row=0, sticky='NE')
        Button(self, text="Select Frames", command=self.controller.select_frames).grid(column=0, row=1, sticky="NE")
        self.preview = Button(self,
                              text='Preview Scene',
                              command=lambda: self.controller.preview_scene(self.controller.main_timing.get()),
                              state=DISABLED)
        self.controller.preview_btn = self.preview
        self.output = Button(self,
                             text='Write',
                             command=self.controller.output,
                             state=DISABLED)
        self.controller.output_btn = self.output

        for child in self.winfo_children():
            child.grid(pady=(5, 0), padx=(30, 10), sticky=NE)
        self.grid(row=0, column=1)









    def switches(self, *args):
        """Enable or enable buttons and functionality"""
        if self.scene_name.get() == '' or self.rpy_file == '':
            self.output.config(state=DISABLED)
        if not self.if_num(self.timing.get()) or self.images.get() == '':
            self.preview.config(state=DISABLED)
            self.output.config(state=DISABLED)
        elif self.if_num(self.timing.get()) and self.images.get() != '':
            self.preview.config(state=NORMAL)
            if self.scene_name.get() != '' and self.rpy_file != '':
                self.output.config(state=NORMAL)

    def read_file(self, *args):
        if Path(self.rpy_file).is_file():
            self.rpy_data = open(self.rpy_file).read()



    def if_num(self, num):
        # I probably could import from alternative or export to there, but for now I'm going for function,
        # I'm going for function right now, refactoring on v4
        try:
            return float(num)
        except ValueError:
            return False
