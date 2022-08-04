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
        self.legacy_syntax = BooleanVar()

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
        if self.insert_audio.get():
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
            # If validated write function on rict_script.
            self.write_sfx_function()
        if not self.suffix_only_enabled.get():
            self.output_scene()
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
                if self.insert_audio.get() and self.async_output():
                    self.sfx_async_output(file=rpy, timing_var=self.main_timing.get())
                else:
                    for frame in self.frames:
                        if self.legacy_syntax.get():
                            rpy.write(f"    \"{frame.split('images/')[1]}\"\n")
                        else:
                            rpy.write(f"    \"{Path(frame).stem}\"\n")
                        self.output_effect(sound_enabled=self.insert_audio.get(),
                                           file=rpy,
                                           current_frame=frame)
                        rpy.write(f"    {self.main_timing.get()}\n")
                    rpy.write("    repeat\n\n")
        else:
            messagebox.showerror('Duplicate found', f'There is another scene named {self.scene_name.get()}')

    # TODO: ADD THE OPTION TO INSERT SOUND EFFECTS INTO ALTERNATIVE SCENES. (Looking at this Ima have to redo it all)
    # if main_timing > alt_timing:
    # timing = main / (main/alt)
    # if main_timing < alt_timing:
    # timing = main * (alt/main)
    def adjust_async_timing(self, async_timing, **kw):
        main = round(float(self.main_timing.get()), 3)
        async_timing = round(float(async_timing), 3)
        start_point = round(float(self.audio_start.get()), 3)
        interval = round(float(self.audio_interval.get()), 3)
        if kw.get('adjust_start'):
            if main > async_timing:
                return round(start_point / (main / async_timing), 3)
            elif main == async_timing:
                return round(float(self.audio_start.get()), 3)
            else:
                return round(start_point * (async_timing / main), 3)
        else:
            if main > async_timing:
                return round(interval / (main / async_timing), 3)
            elif main == async_timing:
                return round(float(self.audio_interval.get()), 3)
            else:
                return round(interval * (async_timing / main), 3)

    def output_effect(self, file=None, sound_enabled=False, current_frame=None):
        if sound_enabled and \
                self.sfx_frame_validation(current_frame) and \
                self.audio_interval_option.get().lower() == 'frames':
            file.write(f"    function {self.sound_function.get()}\n")
        else:
            pass

    def sfx_frame_validation(self, current_frame):
        start = int(self.audio_start.get()) - 1
        step = int(self.audio_interval.get())
        if self.frames.index(current_frame) in range(start, len(self.frames), step):
            return True
        else:
            return False

    def sfx_async_output(self, file, timing_var):
        # print(f"[DEBUG] timing_var: {timing_var}")
        loop_duration = 0.0
        starting_point = self.adjust_async_timing(timing_var, adjust_start=True)
        interval = self.adjust_async_timing(timing_var)
        # print(f"[DEBUG] Adjusted Interval: {interval}")
        file.write("    parallel:\n")
        for frame in self.frames:
            loop_duration += round(float(timing_var), 3)
            if self.legacy_syntax.get():
                file.write(f"        \"{frame.split('images/')[1]}\"\n")
            else:
                file.write(f"        \"{Path(frame).stem}\"\n")
            file.write(f"        {timing_var}\n")
        file.write("        repeat\n")

        file.write("    parallel:\n")
        file.write(f"        {starting_point}\n")
        loop_duration -= starting_point
        while loop_duration > 0:
            if round(loop_duration, 3) >= round(interval, 3):
                # print(f"[DEBUG] Current loop duration: {round(loop_duration, 3)}")
                file.write(f"        function {self.sound_function.get()}\n")
                file.write(f"        {interval}\n")
                loop_duration -= interval
                # print(f"[DEBUG] loop duration after subtraction: {round(loop_duration, 3)}")
            else:
                file.write(f"        {round(loop_duration, 3)}\n")
                break
        file.write("        repeat\n\n")

    def async_output(self):
        return self.audio_interval_option.get() == "Seconds"

    def write_sfx_function(self):
        # TODO: CREATE A DIFFERENTLY NAMED VARIABLE IF FILENAME IS THE SAME, BUT PATH IS DIFFERENT.
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
                        if self.insert_audio.get() and self.async_output():
                            self.sfx_async_output(file=rpy,
                                                  timing_var=var.timing())
                        else:
                            for frame in self.frames:
                                if self.legacy_syntax.get():
                                    rpy.write(f"    \"{frame.split('images/')[1]}\"\n")
                                else:
                                    rpy.write(f"    \"{Path(frame).stem}\"\n")
                                self.output_effect(file=rpy,
                                                   sound_enabled=self.insert_audio.get(),
                                                   current_frame=frame)
                                rpy.write(f"    {var.timing()}\n")
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
        """Randomly fill some fields and variables. For testing purposes."""
        rpy_file_path = self.config['Files']['RpyFile']
        if Path(rpy_file_path).is_file():
            self.rpy_file.set(rpy_file_path)
            self.read_rpy()
            self.scene_name.set(f"scene_{''.join(choices(letters, k=10))}")
            self.frames = [f"frame_{''.join(choices(letters, k=8))}" for i in range(10)]
            self.image_entry.set("\"DEBUG PURPOSES\"")
        else:
            messagebox.showerror("No file selected", "You must select a target .rpy file at least once.")