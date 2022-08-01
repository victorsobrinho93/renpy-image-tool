from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from configuration import *
from preview import Preview


class Controller:
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
        self.conditional_image = StringVar()

        self.insert_audio = BooleanVar()
        self.audio_file = StringVar()
        self.audio_directory = StringVar()
        self.audio_timing = StringVar()

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
            self.create_rict_file()

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

    def select_audio(self):
        self.audio_file.set(filedialog.askopenfilename(initialdir=self.config['Files']['AudioDirectory'],
                                                       title="Select audio file",
                                                       filetypes=(("Audio", "*.ogg *.mp3 *.wav *.flac"),
                                                                  ("All files", "*.*"))))

        if Path(self.audio_file.get()).is_file():
            audio_directory = str(Path(self.audio_file.get()).parent)
            self.config.set_('Files', 'AudioDirectory', audio_directory)

    def preview_scene(self, timing):
        preview = Preview(self, timing)
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
        else:
            messagebox.showerror('Duplicate found', f'There is another scene named {self.scene_name.get()}')

    def output_audio(self):
        pass

    # ? As it is right now, you can have duplicates if you input them at the same time,
    def output_alternative(self):
        with open(self.rpy_file.get(), mode='a+') as rpy:
            self.read_rpy()
            valid = []
            for var in self.alt_entries:
                if self.duplicate(repr(var)):
                    messagebox.showerror('Duplicate found', f'There is another scene named {repr(var)}')
                    return
                if repr(var) in valid:
                    messagebox.showerror("Error", f"Duplicated suffix ({var.suffix()})")
                    return
                valid.append(repr(var))
            for var in self.alt_entries:
                try:
                    if repr(var) != '' and self.is_num(var.timing()):
                        # print(repr(var))
                        rpy.write(f"image {repr(var)}:\n")
                        for frame in self.frames:
                            rpy.write(f"    \"{Path(frame).stem}\"\n"
                                      f"    {var.timing()}\n")
                        rpy.write("    repeat\n\n")
                except TypeError:
                    pass

    def output_conditionals(self):
        self.read_rpy()
        if self.conditional_entries:
            with open(self.rpy_file.get(), mode="a+") as rpy:
                valid = []
                for var in self.conditional_entries:
                    if var.condition() and var.image():
                        valid.append(f"    \"{var.condition()}\", \"{var.image()}\",\n")
                if valid:
                    cs_output = f"image {self.conditional_image.get()} = ConditionSwitch(\n"
                    if cs_output in self.rpy_data:
                        messagebox.showerror('Duplicated Switch',
                                             f"There is already a ConditionSwitch named {self.conditional_image.get()}"
                                             )
                        return
                    rpy.write(f"{cs_output}")
                    for var in valid:
                        rpy.write(var)
                    rpy.write(")\n\n")

    def duplicate(self, image_name):
        return f"image {image_name}:" in self.rpy_data

    @staticmethod
    def is_num(num):
        try:
            return float(num)
        except ValueError:
            return False

    def create_rict_file(self):
        rict_script = f"{self.config.rpy_directory()}/rict_scripts.rpy"
        if not Path(rict_script).is_file():
            with open(f'{self.config.rpy_directory()}/rict_scripts.rpy', 'w') as script:
                script.write(
                    f"# This script contains all the functions used by the images made with RICT.\n"
                    f"init -1 python:\n"
                    f"    def sfx(trans, st, at, file):\n"
                    f"        renpy.play(file, channel=sound)\n\n"

                )