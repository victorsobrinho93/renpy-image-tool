from tkinter import *
from tkinter import ttk


class Buttons(Frame):
    def __init__(self, parent_frame, controller):
        super().__init__(parent_frame)
        self.controller = controller
        self.conf = controller.config

        ttk.Button(self, text='Open File', command=self.controller.open_rpy).grid(column=0, row=0, sticky='NE', ipadx=7)
        ttk.Button(self, text="Select Frames", command=self.controller.select_frames).grid(column=0, row=1, sticky="NE",
                                                                                           ipadx=4)
        self.preview_btn = ttk.Button(self,
                                      text='Preview Scene',
                                      command=lambda: self.controller.preview_scene(self.controller.main_timing),
                                      state=DISABLED)
        self.preview_btn.grid(column=0, row=2, sticky=NE, ipadx=3)
        # self.controller.preview_btn = self.preview
        self.output_btn = ttk.Button(self,
                                     text='Write',
                                     command=self.controller.output,
                                     state=DISABLED)
        self.output_btn.grid(column=0, row=3, sticky=NE, ipadx=7)
        # self.controller.output_btn = self.output
        ttk.Button(self, text="DEBUG", command=self.controller.debug, width=14)
        ttk.Checkbutton(self,
                        variable=self.controller.legacy_syntax,
                        text="Legacy syntax")

        for child in self.winfo_children():
            child.grid(pady=(5, 0), padx=(30, 10), sticky=NE)

        self.controller.scene_name.trace_add('write', self.set_state)
        self.controller.image_entry.trace_add('write', self.set_state)
        self.controller.main_timing.trace_add('write', self.set_state)

        self.grid(row=0, column=1)

    def set_state(self, *args):
        try:
            if self.controller.is_num(self.controller.main_timing.get()) and self.controller.frames is not None:
                if self.controller.rpy_file.get() != '' and self.controller.scene_name.get() != '':
                    self.output_btn.config(state=NORMAL)
                else:
                    self.output_btn.config(state=DISABLED)
                self.preview_btn.config(state=NORMAL)
                return
            else:
                self.preview_btn.config(state=DISABLED)
                self.output_btn.config(state=DISABLED)
        except AttributeError:
            pass
