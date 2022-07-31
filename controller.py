from configuration import *
from user_interface import *
from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import filedialog
from preview import Preview
# from alternative import AlternativeEntry
from tkinter import messagebox
from time import sleep


def is_num(num):
    try:
        return float(num)
    except ValueError:
        return False


class Controller():
    def __init__(self):
        super().__init__()
        self.config = Configuration(self)
        self.alt_entries = []
        self.conditional_entries = []
        self.rpy_file = StringVar()
        self.scene_name = StringVar()
        self.image_entry = StringVar()
        self.main_timing = StringVar()

        self.preview_btn = None
        self.output_btn = None
        self.rpy_data = None
        self.frames = None
        self.suffix_only_enabled = BooleanVar()
        self.alt_scenes_enabled = BooleanVar()
        self.conditionals_enabled = BooleanVar()


    def read_rpy(self):
        self.rpy_data = open(self.rpy_file.get()).read()

    def open_rpy(self):
        self.rpy_file.set(filedialog.askopenfilename(initialdir=self.config['Files']['RpyDirectory'],
                                                     title="Select *.rpy file",
                                                     filetypes=(("Ren'py file", "*.rpy"),
                                                                ("All files", "*.*")))
                          )
        if Path(self.rpy_file.get()).suffix == '.rpy':
            self.read_rpy()
            self.config.set_('Files', 'RpyFile', self.rpy_file.get())
            self.config.set_('Files', 'RpyDirectory', str(Path(self.rpy_file.get()).parent))

    def select_frames(self):
        def format_insert():
            insert = ''
            for file in self.frames:
                insert += f"\"{Path(file).stem}\", "
            self.image_entry.set(insert)

        self.frames = filedialog.askopenfilenames(initialdir=self.config['Files']['ImagesDirectory'],
                                                  title="Select animation frames",
                                                  filetypes=(("Images", "*.png *.jpg *.webp"),
                                                             ("All files", "*.*")))

        format_insert()
        try:
            if Path(self.frames[0]).parent.is_dir():
                directory = str(Path(self.frames[0]).parent)
                self.config.set_('Files', 'ImagesDirectory', directory)
        except IndexError:
            pass

    def preview_scene(self, timing):
        preview = Preview(self.frames, timing)
        preview.player()
        preview.mainloop()

    def output(self):
        if not self.suffix_only_enabled.get():
            self.output_scene()
        if self.alt_scenes_enabled.get():
            self.output_alternative()
        if self.conditionals_enabled.get():
            self.output_conditionals()
        self.read_rpy()

    def output_scene(self):
        if not self.duplicate(self.scene_name.get()):
            with open(self.rpy_file.get(), mode="a+") as rpy:
                rpy.write(f"image {self.scene_name.get()}:\n")
                for frame in self.frames:
                    rpy.write(f"    \"{Path(frame).stem}\"\n"
                              f"    {self.main_timing.get()}\n")
                rpy.write("    repeat\n\n")

    def output_alternative(self):
        with open(self.rpy_file.get(), mode='a+') as rpy:
            for var in self.alt_entries:
                self.read_rpy()
                if not self.duplicate(repr(var)):
                    try:
                        if repr(var) != '' and is_num(var.timing()):
                            print(repr(var))
                            rpy.write(f"image {repr(var)}:\n")
                            for frame in self.frames:
                                rpy.write(f"    \"{Path(frame).stem}\"\n"
                                          f"    {var.timing()}\n")
                            rpy.write("    repeat\n\n")
                    except TypeError:
                        pass

    def output_conditionals(self):
        with open(self.rpy_file.get(), mode="a+") as rpy:
            if self.conditional_objects:
                valid = []
                for var in self.conditional_objects:
                    if var.return_condition() and var.return_scene():
                        valid.append(f"    \"{var.return_condition()}\", \"{var.return_scene()}\",\n")
                if valid:
                    rpy.write(f"image {self.cnd_name.get()} = ConditionSwitch(\n")
                    for var in valid:
                        rpy.write(var)
                    rpy.write(")\n\n")

    def duplicate(self, image_name):
        return image_name in self.rpy_data

    @staticmethod
    def is_num(num):
        try:
            return float(num)
        except ValueError:
            return False








