from tkinter import *
from tkinter import ttk
from pathlib import Path
# from tkinter import font
from tkinter.font import Font


class FileEntry(Frame):
    def __init__(self, frame, controller):
        super().__init__(frame)
        self.controller = controller
        self.conf = controller.config

        self.rpy_var = StringVar()
        ttk.Label(self, text="*.rpy file").grid(column=0, row=0, sticky='W', pady=(30, 5), padx=(0, 15))
        self.rpy_entry = ttk.Entry(self, width=30, textvariable=self.rpy_var)
        self.rpy_entry.grid(column=1, row=0, sticky='W', pady=(30, 5))
        self.controller.rpy_file.trace_add('write', self.rpy_insert)

        ttk.Label(self, text='Scene name:').grid(column=0, row=1, sticky='W', pady=(0, 5), padx=(0, 8))
        self.scene_entry = ttk.Entry(self, width=30, textvariable=self.controller.scene_name)
        self.scene_entry.focus()
        self.scene_entry.grid(column=1, row=1, sticky='W', pady=(0, 5))

        # Default timing
        ttk.Label(self, text="Timing: ").grid(column=2, row=1, sticky=W, padx=(10, 3), pady=(0, 5))
        self.timing_entry = ttk.Entry(self, width=5, textvariable=self.controller.main_timing)
        self.timing_entry.grid(row=1, column=3, sticky=W, padx=(0, 15), pady=(0, 5))
        self.timing_entry.insert(0, self.conf.timing_insert())
        # ttk.Label(self, text=" aaaaaaaaa      ").grid(column=4, row=1, sticky=W)
        # Select images
        self.images_var = StringVar()
        ttk.Label(self, text='Frames: ').grid(row=2, column=0, sticky="W", pady=(0, 5))
        self.images_entry = ttk.Entry(self, width=30, textvariable=self.images_var)
        self.images_entry.grid(column=1, row=2, pady=(0, 5))
        self.down_icon = PhotoImage(file="src/down.png")
        self.up_icon = PhotoImage(file="src/up.png")
        self.controller.image_entry.trace_add('write', self.images_insert)

        self.expand = Button(self, image=self.down_icon, borderwidth=0, command=self.show_frames)
        self.expand.grid(column=2, row=2, sticky=W, padx=3)
        self.show_all = False
        self.frame_window = None

        self.grid(row=0, column=0, padx=(20, 0), sticky=W)

    def rpy_insert(self, *args):
        self.rpy_entry.insert(0, str(Path(self.controller.rpy_file.get()).stem))

    def images_insert(self, *args):
        self.images_entry.delete(0, END)
        self.images_entry.insert(0, self.controller.image_entry.get().strip(', '))

    def show_frames(self):
        self.show_all ^= True
        # print(font.families())
        if self.show_all:
            frame_list = self.controller.image_entry.get().split(", ")
            self.frame_window = Text(
                self,
                height=len(frame_list),
                width=30,
                font=Font(family="Segoe UI Historic", size=9),
                border=1
            )
            self.images_entry.grid_forget()
            self.frame_window.grid(column=1, row=2, sticky=W, pady=(0, 5))
            for item in frame_list[::-1]:
                self.frame_window.insert('1.0', f"{item}\n")
            self.expand.configure(image=self.up_icon)
        else:
            self.expand.configure(image=self.down_icon)
            self.frame_window.grid_forget()
            self.images_entry.grid(column=1, row=2, sticky=W, pady=(0, 5))
            self.images_insert()
        # for item in self.controller.image_entry.get().split(', '):
        #     print(item)