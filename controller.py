from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from configuration import *
from preview import Preview
from string import ascii_lowercase as letters, digits
from random import choices
import math


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
        self.rict_data = None
        self.suffix_only_enabled = BooleanVar()
        self.alt_scenes_enabled = BooleanVar()
        self.conditionals_enabled = BooleanVar()
        self.conditional_image = StringVar()

        self.insert_audio = BooleanVar()
        self.audio_file = StringVar()
        self.audio_directory = StringVar()
        self.audio_timing = StringVar()
        self.audio_start = StringVar()
        self.audio_interval = StringVar()
        self.audio_interval_option = StringVar()
        self.audio_path = StringVar()
        self.disable_repeat = BooleanVar()
        self.sound_function = StringVar()

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
            self.set_script()
            self.read_rict()

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
            try:
                self.audio_path.set(self.audio_file.get().split('game/')[1])
            except IndexError:
                messagebox.showerror("Invalid directory", "File must be inside game directory.")
                # This is a very basic validation check, and probably might lead to problems.

    def preview_scene(self, timing):
        preview = Preview(self, timing)
        preview.player()
        preview.mainloop()

    def output(self):
        if not self.suffix_only_enabled.get():
            if not self.insert_audio.get():
                self.output_scene()
            else:
                if not Path(self.audio_file.get()).is_file():
                    messagebox.showerror("Invalid parameter", "Sound file was not selected.")
                    return
                elif not self.is_num(self.audio_start.get()):
                    messagebox.showerror("Invalid parameter:", "Sound effect starting point is not valid or empty.")
                    return
                elif not self.is_num(self.audio_interval.get()):
                    messagebox.showerror("Invalid parameter", "Sound effect interval is invalid or missing.")
                    return
                if self.audio_interval_option.get().lower() == 'frames':
                    try:
                        int(self.audio_start.get())
                    except ValueError:
                        messagebox.showerror("Invalid parameter", "(Frame) Starting point should be an integer.")
                        return
                    try:
                        int(self.audio_interval.get())
                    except ValueError:
                        messagebox.showerror("Invalid parameter", "(Frame) Interval should be an integer.")
                        return
                self.output_sfx()

        if self.alt_scenes_enabled.get():
            self.output_alternative()
        if self.conditionals_enabled.get():
            self.output_conditionals()
        self.read_rpy()

    def output_scene(self):
        # self.output_sfx()
        if not self.duplicate(self.scene_name.get()):
            with open(self.rpy_file.get(), mode="a+") as rpy:
                rpy.write(f"image {self.scene_name.get()}:\n")
                for frame in self.frames:
                    rpy.write(f"    \"{Path(frame).stem}\"\n"
                              f"    {self.main_timing.get()}\n")
                rpy.write("    repeat\n\n")
        else:
            messagebox.showerror('Duplicate found', f'There is another scene named {self.scene_name.get()}')

    def output_sfx(self):
        self.read_rict()
        self.sfx_function()
        script = self.config['Files']['Script']
        with open(self.rpy_file.get(), mode='a+') as rpy:
            rpy.write(f"image {self.scene_name.get()}:\n")
            if self.audio_interval_option.get().lower() == 'frames':
                self.sfx_frames(rpy)
            if self.audio_interval_option.get().lower() == 'seconds':
                self.sfx_time_interval(rpy)

    def sfx_frames(self, file):
        first_inserted = False
        sfx_at = None
        for frame in self.frames:
            file.write(f"    \"{Path(frame).stem}\"\n")
            if int(self.audio_start.get()) == self.frames.index(frame) + 1:
                first_inserted = True
                sfx_at = self.frames.index(frame)
                file.write(f"    function {self.sound_function.get()}\n")
            if (first_inserted and
                    self.step(sfx_at, self.frames.index(frame), int(self.audio_interval.get())) and
                    not self.disable_repeat.get()):
                file.write(f"    function {self.sound_function.get()}\n")
                sfx_at = self.frames.index(frame)
            file.write(f"    {self.main_timing.get()}\n")
        file.write("    repeat\n\n")

    def sfx_time_interval(self, file):
        loop_duration = 0.0
        interval = round(float(self.audio_interval.get()))
        print(f"[debug]Interval: {interval}")
        file.write("    parallel:\n")
        for frame in self.frames:
            loop_duration += float(self.main_timing.get())
            file.write(f"        \"{Path(frame).stem}\"\n")
            file.write(f"        {self.main_timing.get()}\n")
        file.write("        repeat\n")

        file.write("    parallel:\n")
        file.write(f"        {self.audio_start.get()}\n")
        loop_duration -= interval
        while loop_duration > 0:
            print(loop_duration)
            file.write(f"        function {self.sound_function.get()}\n")
            if loop_duration >= interval:
                file.write(f"        {interval}\n")
                loop_duration -= interval
            else:
                file.write(f"        {round(loop_duration, 2)}\n")
                break
        file.write("        repeat\n\n")

    def sfx_function(self):
        #TODO: CREATE A DIFFERENTLY NAMED VARIABLE IF FILENAME IS THE SAME, BUT PATH IS DIFFERENT.
        self.read_rict()
        self.audio_path.set(self.audio_file.get().split("/game")[1])
        if self.audio_path.get() in self.rict_data:
            # If there is already a function using this file, return that function name.
            with open(self.config['Files']['Script'], mode="r+") as rict:
                for line in rict:
                    if self.audio_path.get() in line:
                        self.sound_function.set(f"{line.split(' = ')[0].strip()}")
                        break
        else:
            with open(self.config['Files']['Script'], mode="a+") as rict:
                rict.write(f"    sfx_{str(Path(self.audio_path.get()).stem)} = "
                           f"lambda *args: renpy.play(\"{self.audio_path.get()}\")\n")
                self.sound_function.set(f"sfx_{str(Path(self.audio_path.get()).stem)}")

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

    def set_script(self):
        if not Path(self.config['Files']['Script']).is_file():
            script_path = f"{self.config.rpy_directory()}/rict_scripts.rpy".replace('\\', '/')
            with open(script_path, 'w') as script:
                script.write(
                    f"# This file contains all the functions used by the images made with Ren'py Image Creation Tool.\n"
                    f"# Moving or renaming this file will cause issues, if you do it while your work is in progress.\n"
                    f"# Check for updates at (https://github.com/victorsobrinho93/renpy-image-creation-tool)\n\n"
                    f"init -1 python:\n"
                    f"    hello = 'there'"

                )
                self.config.set_('Files', 'Script', script_path)

    def read_rict(self):
        self.rict_data = open(self.config['Files']['Script']).read()

    def debug(self):
        """Creating a whole spoof operation."""
        rpy_file_path = self.config['Files']['RpyFile']
        if Path(rpy_file_path).is_file():
            self.rpy_file.set(rpy_file_path)
            self.read_rpy()
            self.scene_name.set(f"scene_{''.join(choices(letters, k=10))}")
            self.frames = [f"frame_{''.join(choices(letters, k=8))}" for i in range(10)]
            self.image_entry.set("\"DEBUG PURPOSES\"")
        else:
            messagebox.showerror("No file selected", "You must select a target .rpy file at least once.")

    def step(self, last_valid, current, step):
        return (current - step) == last_valid
