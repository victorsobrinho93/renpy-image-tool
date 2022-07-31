from tkinter import *
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

    def player(self):
        minus_hundred = Button(self, text="-100 ms", command=lambda: self.decrease_timing(100))
        minus_hundred.grid(row=2, column=7, sticky=E)
        minus_ten = Button(self, text="-10 ms", command=lambda: self.decrease_timing(10))
        minus_ten.grid(row=2, column=8, sticky=E)
        apply_timing = Button(self, text="Apply New Timing", command=self.apply_timing)
        apply_timing.grid(row=2, column=9, columnspan=5, sticky=EW, padx=5)
        plus_ten = Button(self, text="+10 ms", command=lambda: self.increase_timing(10))
        plus_ten.grid(row=2, column=14, sticky=W)
        plus_hundred = Button(self, text="+100 ms", command=lambda: self.increase_timing(100))
        plus_hundred.grid(row=2, column=15, sticky=W)
        close = Button(self, text="Close Window", command=lambda: self.destroy())
        close.grid(row=2, column=17, sticky=E, pady=(10, 10))
        self.screen()

    def screen(self, *args):
        try:
            args[0].grid_forget()
        except IndexError:
            pass
        self.frame = next(self.frames)
        show = Label(self, image=self.frame)
        show.grid(column=0, row=1, columnspan=20)
        Label(self, text=f"Timing: {self.timing} ms ({'{:.2f}'.format(1000/self.timing)} fps)").grid(column=1, row=2, columnspan=5)
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
