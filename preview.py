from tkinter import *
from PIL import ImageTk, Image
from itertools import cycle


class Preview(Toplevel):
    def __init__(self, image_list, timing):
        super().__init__()
        self.title("Animation Preview")
        self.iconbitmap("icon.ico")
        self.frames = cycle(ImageTk.PhotoImage(Image.open(frame)) for frame in image_list)
        self.timing = int(float(timing.get()) * 1000)
        self.output = timing

    def player(self):

        self.slow = Button(self, text="-100 ms", command=lambda: self.decrease_timing(100))
        self.slow.grid(row=2, column=7, sticky=E)
        self.v_slow = Button(self, text="-10 ms", command=lambda: self.decrease_timing(10))
        self.v_slow.grid(row=2, column=8, sticky=E)
        self.apply_timing = Button(self, text="Apply New Timing", command=self.apply_timing)
        self.apply_timing.grid(row=2, column=9, columnspan=5, sticky=EW, padx=5)
        self.v_fast = Button(self, text="+10 ms", command=lambda: self.increase_timing(10))
        self.v_fast.grid(row=2, column=14, sticky=W)
        self.fast = Button(self, text="+100 ms", command=lambda: self.increase_timing(100))
        self.fast.grid(row=2, column=15, sticky=W)
        self.close = Button(self, text="Close Window", command=lambda: self.destroy())
        self.close.grid(row=2, column=17, sticky=E, pady=(10, 10))
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
        self.after(self.timing, self.screen(show))

    def increase_timing(self, ms):
        self.timing += ms

    def decrease_timing(self, ms):
        if self.timing >= 16:
            self.timing -= ms
        if self.timing < 16:
            self.timing = 16

    def apply_timing(self):
        self.output.delete(0, END)
        timing_format = "{:.2f}".format(self.timing / 1000)
        self.output.insert(0, timing_format)