import sys
from PyQt6.QtWidgets import QApplication

from stack import Stack
from data import Data
from parser import Parser
from interpreter import Interpreter
from visualizer import Visualizer


class Blang:
    def __init__(self):
        self.data = Data()
        self.stack = Stack(self.data)
        self.parser = Parser(self.stack, self.data)
        self.interpreter = Interpreter(self.stack, self.data, self.parser)

    def run(self):
        app = QApplication(sys.argv)
        w = Visualizer(self)
        w.show()
        sys.exit(app.exec())
