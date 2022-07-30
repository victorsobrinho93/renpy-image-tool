from configuration import *
from user_interface import *


def if_num(self, num):
    try:
        return float(num)
    except ValueError:
        return False


class Controller():
    def __init__(self):
        super().__init__()
        self.config = Configuration(self)
        self.alternative_objects = []
        self.conditional_objects = []
