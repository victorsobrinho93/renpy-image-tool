import tkinter as tk
from tkinter import *
from tkinter import filedialog
from pathlib import Path
from configparser import ConfigParser
from PIL import ImageTk, Image
from itertools import cycle
from os.path import exists




def ini_update(section, key, value):
    # settings.read('settings.ini')
    settings.set(section, key, value)
    with open('./settings.ini', 'w') as configfile:
        settings.write(configfile)


# TODO: READ FILE TO SEE IF THERE IS NOT A SCENE WITH THE SAME NAME BEFORE ADDING ANOTHER
# TODO: DISABLE THE CREATE SCENE BUTTON IF THE FIELDS ARE EMPTY
# TODO: OBJECTIFY SOME OF THIS STUFF, CLEAN UP THE CODE


root = Tk()
root.title('Ren\'py scene assistant')
root.iconbitmap('./favicon.ico')
# root.geometry('650x300')
# root.attributes('-toolwindow', True)
root.resizable(0, 0)


def button_state(*args):
    def no_check(no):
        try:
            return float(no) > 0
        except ValueError:
            return False

    timing = no_check(default_timing.get())
    file = rpy_file.get()
    # images = image_files.get()
    scene_name = scene.get()
    try:
        if timing and image_files.get():
            preview_button.config(state=NORMAL)
        else:
            preview_button.config(state=DISABLED)
        if file and timing and image_files.get() and scene_name:
            create_button.config(state=NORMAL)
        else:
            create_button.config(state=DISABLED)
    except NameError:
        print("Hey.")





def filename():
    file = filedialog.askopenfilename(initialdir=settings['Paths']['RpyDirectory'],
                                      title="Select .rpy file",
                                      filetypes=(("Ren'py files", "*.rpy"),
                                                 ("all files", "*.*"))
                                      )
    file_path.delete(0, END)
    file_path.insert(0, str(Path(file).stem))
    if rpy_file.get():
        ini_update('Paths', 'RpyDirectory', str(Path(file).parent))
        ini_update('Paths', 'RpyFile', file)


def rpy_path():
    return str(settings['Paths']['RpyFile'])


def add_images():
    img_entry.delete(0, END)
    images = filedialog.askopenfilenames(initialdir=settings['Paths']['ImagesDirectory'],
                                         title='Add images to scene',
                                         filetypes=(("Images", ["*.png", "*.webp", "*.jpg"]),
                                                    ("All files", "*.*")))
    img_entry.insert(0, images)


def file_list():
    """Splitting the string into parts, updating directory"""
    if "{" in img_entry.get():
        files = img_entry.get().strip('{}').split('} {')
    else:
        files = img_entry.get().split(' ')
    if str(Path(files[0]).parent):
        ini_update('Paths', 'ImagesDirectory', str(Path(files[0]).parent))
    files_r = [str(Path(item).stem) for item in files]

    return files_r


def write_scenes(**kw):
    work_files = file_list()
    ini_update('Timing', 'DefaultTiming', timing_entry.get())
    with open(rpy_path(), mode='a+') as rpy:
        if f"image {scene.get()}:\n" in open(rpy_path()).read():
            print("Scene already here.")
        else:
            if multiple_speed.get() == '0':
                rpy.write(f"image {scene.get()}:\n")
                for item in work_files:
                    rpy.write(f"    \"{item}\"\n"
                              f"    {timing_entry.get()}\n")
                rpy.write("    repeat\n\n")
            elif multiple_speed.get() == '1':
                write_multiple(work_files)
            if conditionalSwitch.get() == '1':
                conditional_output(rpy_path())


def write_multiple(files):
    # TODO: Split the multiple scenes widget so we can clean this up
    with open(rpy_path(), mode='a+') as rpy:
        f_name = f'{scene.get()}_{first_variant.get()}'
        s_name = f"{scene.get()}_{second_variant.get()}"
        if f_name in open(rpy_path()).read():
            print("There is already a variant scene by this name.")
        else:
            rpy.write(
                f"image {f_name}:\n"
            )
            for item in files:
                rpy.write(
                    f"    \"{item}\"\n"
                    f"    {first_timing.get()}\n"
                )
            rpy.write("    repeat\n\n")
            rpy.write(
                f"image {s_name}:\n"
            )
            for item in files:
                rpy.write(
                    f"    \"{item}\"\n"
                    f"    {second_timing.get()}\n"
                )
            rpy.write("    repeat\n\n")

    ini_update('Timing', 'FirstVariant', first_variant.get())
    ini_update('Timing', 'FirstVariantTiming', first_timing.get())
    ini_update('Timing', 'SecondVariant', second_variant.get())
    ini_update('Timing', 'SecondVariantTiming', second_timing.get())


def conditional_output(file):
    with open(file, mode="a+") as output:
        if f"image {conditional_name.get()}" in open(file).read():
            print("There is already a Conditional Switch by that name.")
        else:
            output.write(
                f"image {conditional_name.get()} = ConditionSwitch(\n"
                f"    \"{first_condition.get()}\", \"{first_image.get()}\",\n"
                f"    \"{second_condition.get()}\", \"{second_image.get()}\"\n"
                f")\n\n"
            )



# Entry Frame
entry = Frame()
# Output file


variant = Frame()


def variant_fill():
    first_variant.delete(0, END)
    first_variant.insert(0, settings['Timing']['FirstVariant'])
    first_timing.delete(0, END)
    first_timing.insert(0, settings['Timing']['FirstVariantTiming'])
    second_variant.delete(0, END)
    second_variant.insert(0, settings['Timing']['SecondVariant'])
    second_timing.delete(0, END)
    second_timing.insert(0, settings['Timing']['SecondVariantTiming'])


# Multiple Speeds


# ConditionalSwitch
conditional_switch = Frame()
conditionalSwitch = StringVar()
check_cs = Checkbutton(
    conditional_switch,
    text="Conditional Switch",
    variable=conditionalSwitch,
    command=lambda: field_toggle(conditional_name, first_condition, first_image, second_condition, second_image)
)
check_cs.deselect()
check_cs.grid(column=0, row=0)


def conditional_auto():
    first_image.delete(0, END)
    second_image.delete(0, END)
    first_image.insert(0, f"{scene.get()}_{first_variant.get()}")
    second_image.insert(0, f"{scene.get()}_{second_variant.get()}")


def csw_check():
    if conditionalSwitch.get() == '1':
        Label(conditional_switch, text="IT'S ACTIVE").grid(row=3, column=1)
    else:
        Label(conditional_switch, text="IT'S NOT ACTIVE").grid(row=3, column=1)


conditional_switch.columnconfigure(0, weight=2)
conditional_switch.configure(padx=20, pady=15)

Label(conditional_switch, text="Image name: ").grid(row=1, column=0, sticky='W')
conditional_name = Entry(conditional_switch, width=30, state=DISABLED)
conditional_name.grid(row=1, column=1, sticky=W)
Label(conditional_switch, text="First condition: ").grid(row=2, column=0, sticky="W")
first_condition = Entry(conditional_switch, width=30, state=DISABLED)
first_condition.grid(row=2, column=1, sticky="W")
Label(conditional_switch, text="Show: ").grid(row=2, column=2, sticky="W", padx=(5, 0))
first_image = Entry(conditional_switch, width=20, state=DISABLED)
first_image.grid(row=2, column=3, sticky="w")
Label(conditional_switch, text="Second condition: ").grid(row=3, column=0, sticky="W")
second_condition = Entry(conditional_switch, width=30, state=DISABLED)
second_condition.grid(row=3, column=1, sticky="W")
Label(conditional_switch, text="Show: ").grid(row=3, column=2, sticky="W", padx=(5, 0))
second_image = Entry(conditional_switch, width=20, state=DISABLED)
second_image.grid(row=3, column=3, sticky="w")
Button(conditional_switch, text="Auto-fill", command=conditional_auto).grid(row=4, column=2)
Button(conditional_switch, text='DEBUG', command=csw_check).grid(row=4, column=1)

frame = Frame()
frame.columnconfigure(0, weight=2)


for widget in frame.winfo_children():
    widget.grid(padx=20, pady=4)

#traces
default_timing.trace("w", button_state)
rpy_file.trace("w", button_state)
image_files.trace("w", button_state)

entry.grid(row=0, column=0)
variant.grid(row=1, column=0)
frame.grid(row=0, column=1)
conditional_switch.grid(row=2, column=0)

root.mainloop()
