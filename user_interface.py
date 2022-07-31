from tkinter import *
from file_entry import FileEntry
from buttons import Buttons
from alternative import Alternative
from conditional import Conditional
from controller import Controller


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Ren'py Image Tool")
        self.iconbitmap('src/icon.ico')
        self.resizable(False, False)

        self.controller = Controller()
        self.file_entry = FileEntry(self, self.controller)
        # self.action_buttons = Buttons(self, self.controller)
        self.alternative = Alternative(self, self.controller)
        self.conditional = Conditional(self, self.controller)
        self.buttons = Buttons(self, self.controller)
