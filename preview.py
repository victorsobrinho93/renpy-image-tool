from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from itertools import cycle


class Preview(Toplevel):
    def __init__(self, controller, timing):
        super().__init__()
        self.controller = controller
        self.title("Animation Preview")
        self.iconbitmap("src/icon.ico")
        self.frames = cycle(ImageTk.PhotoImage(Image.open(frame)) for frame in self.controller.frames)
        self.timing = int(float(timing.get()) * 1000)
        self.entry = timing
        self.frames_per_second = IntVar()
        self.frames_per_second.set(int(1000 / self.timing))

    def player(self):

        fps = IntVar()
        fps.set(int(1000 / self.timing))
        apply_timing = ttk.Button(self, text="Apply New Timing", command=self.apply_timing)
        apply_timing.grid(row=2, column=9, columnspan=5, sticky=EW, padx=5)
        frames_per_second_slider = ttk.Scale(self, from_=1, to=60, orient=HORIZONTAL, length=300,
                                         variable=self.frames_per_second, command=self.adjust_fps)
        frames_per_second_slider.grid(row=2, column=0)
        close = ttk.Button(self, text="Close Window", command=lambda: self.destroy())
        close.grid(row=2, column=17, sticky=E, pady=(10, 10))
        self.screen()

    def adjust_fps(self, *args):
        self.timing = int(1000 / self.frames_per_second.get())

    def screen(self, *args):
        try:
            args[0].grid_forget()
        except IndexError:
            pass
        self.frame = next(self.frames)
        show = Label(self, image=self.frame)
        show.grid(column=0, row=1, columnspan=20)
        Label(self, text=f"{self.frames_per_second.get()} FPS").grid(column=1, row=2, columnspan=1)
        self.after(self.timing, lambda:self.screen(show))

    def increase_timing(self, ms):
        if self.timing == 17:
            ms -= 7
        self.timing += ms

    def decrease_timing(self, ms):
        if self.timing >= 17:
            self.timing -= ms
        if self.timing < 17:
            self.timing = 17

    def apply_timing(self):
        # self.entry.delete(0, END)
        timing_format = "{:.3f}".format(self.timing / 1000).rstrip('0')
        self.entry.set(timing_format)
