from tkinter import *
from paths import Paths
from buttons import Buttons
from alternative import Alternative
from conditional import Conditional
from settings import Parameters
from configparser import ConfigParser
from tkinter.font import Font


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.buttons = None
        self.alt_scenes = None
        self.title("Ren'py Assistant 1.0")
        self.iconbitmap('./icon.ico')
        self.resizable(False, False)

        self.params = Parameters()
        self.paths = Paths(self, params=self.params)
        self.alt_scenes = Alternative(self, self.paths, params=self.params)
        self.conditionals = Conditional(self, self.paths, alt=self.alt_scenes, params=self.params)
        self.buttons = Buttons(self, self.paths, self.alt_scenes, self.conditionals, params=self.params)

