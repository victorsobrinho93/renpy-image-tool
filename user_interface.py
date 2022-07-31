from tkinter import *
from alternative import Alternative
from buttons import Buttons
from conditional import Conditional
from controller import Controller
from file_entry import FileEntry


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Ren'py Image Tool 1.2.5a")
        self.iconbitmap('src/icon.ico')
        self.resizable(False, False)

        self.controller = Controller()
        self.file_entry = FileEntry(self, self.controller)
        self.alternative = Alternative(self, self.controller)
        self.conditional = Conditional(self, self.controller)
        self.buttons = Buttons(self, self.controller)