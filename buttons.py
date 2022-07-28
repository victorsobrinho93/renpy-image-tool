from tkinter import *
from tkinter import filedialog
from preview import Preview
from pathlib import Path
from paths import Paths

# TODO: Output should be it's own thing. V4...

class Buttons(Frame):
    def __init__(self, app, path, alt, cnd, params):
        super().__init__(app)
        self.rpy_file = ''
        self.image_files = ''
        self.rpy_data = None
        Button(self, text='Open File', command=self.open_file).grid(column=0, row=0, sticky='NE')
        Button(self, text="Select Frames", command=self.add_images).grid(column=0, row=1, sticky="NE")
        self.preview = Button(self, text='Preview Scene', command=self.preview_scene, state=DISABLED)
        self.output = Button(self, text='Write', command=self.create_scene, state=DISABLED)
        for child in self.winfo_children():
            child.grid(pady=(5, 0), padx=(30, 10), sticky=NE)

        self.ini = params
        # --------- Paths aliases -----------
        self.scene_name = path.scene_entry
        self.timing = path.timing_entry
        self.rpy_path = path.file_path
        self.images = path.img_entry
        # -------- Alternative aliases --------------
        self.alt = alt.alt_list
        self.alt_switch = alt.output_alternative
        # ------- Conditionals aliases ---------------
        self.cnd = cnd.cnd_list
        self.cnd_name = cnd.conditional_name
        self.cnd_switch = cnd.output_cswitch

        # ? Tracers // Watchers:
        path.default_timing.trace_add('write', self.switches)
        path.image_files.trace_add('write', self.switches)
        path.scene.trace_add('write', self.switches)
        path.rpy_file.trace_add('write', self.switches)
        self.suffix_check = alt.suffix

        self.grid(row=0, column=1)

    def open_file(self):
        self.rpy_file = filedialog.askopenfilename(initialdir=self.ini['Files']['RpyDirectory'],
                                                   title="Select *.rpy file",
                                                   filetypes=(("Ren'py file", "*.rpy"),
                                                              ("All files", "*.*")))
        self.rpy_path.insert(0, str(Path(self.rpy_file).stem))
        # print(self.rpy_file)
        if "rpy" in self.rpy_file:
            # print(f"*rpy: {str(Path(self.rpy_file).parent)}")
            self.read_file()
            self.ini.update_params((str(Path(self.rpy_file).parent)), rpy_dir=True)

    def add_images(self):
        self.image_files = filedialog.askopenfilenames(initialdir=self.ini['Files']['ImagesDirectory'],
                                                       title="Select animation frames",
                                                       filetypes=(("Images", "*.png *.jpg *.webp"),
                                                                  ("All files", "*.*")))

        self.images.delete(0, END)
        self.images.insert(0, self.split_path())
        try:
            if Path(self.image_files[0]).parent.is_dir():
                img_dir = str(Path(self.image_files[0]).parent)
                self.ini.update_params(img_dir, img_dir=True)
        except IndexError:
            pass

    def split_path(self):
        img_list = ''
        for file in self.image_files:
            img_list += f"\"{Path(file).stem}\", "
        return img_list

    def preview_scene(self):
        preview = Preview(self.image_files, self.timing)
        preview.player()
        preview.mainloop()

    def create_scene(self):
        if not self.suffix_check.get():
            self.output_scene()
        if self.alt_switch.get() == '1':
            self.output_alternative()
        if self.cnd_switch.get():
            self.output_conditionals()
        self.read_file()

    def output_scene(self):
        if not self.duplicate(self.scene_name.get()):
            with open(self.rpy_file, mode="a+") as rpy:
                rpy.write(f"image {self.scene_name.get()}:\n")
                for frame in self.image_files:
                    rpy.write(f"    \"{Path(frame).stem}\"\n"
                              f"    {self.timing.get()}\n")
                rpy.write("    repeat\n\n")

    def output_alternative(self):
        with open(self.rpy_file, mode='a+') as rpy:
            for var in self.alt:
                data = var.return_values()
                try:
                    if not self.duplicate(f"{self.scene_name.get()}_{data[0]}"):
                        rpy.write(f"image {self.scene_name.get()}_{data[0]}:\n")
                        for frame in self.image_files:
                            rpy.write(f"    \"{Path(frame).stem}\"\n"
                                      f"    {data[1]}\n")
                        rpy.write("    repeat\n\n")
                except TypeError:
                    pass

    def output_conditionals(self):
        with open(self.rpy_file, mode="a+") as rpy:
            if self.cnd:
                valid = []
                for var in self.cnd:
                    if var.return_condition() and var.return_scene():
                        valid.append(f"    \"{var.return_condition()}\", \"{var.return_scene()}\",\n")
                if valid:
                    rpy.write(f"image {self.cnd_name.get()} = ConditionSwitch(\n")
                    for var in valid:
                        rpy.write(var)
                    rpy.write(")\n\n")

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

    def duplicate(self, image_name):
        return image_name in self.rpy_data

    def if_num(self, num):
        # I probably could import from alternative or export to there, but for now I'm going for function,
        # I'm going for function right now, refactoring on v4
        try:
            return float(num)
        except ValueError:
            return False
