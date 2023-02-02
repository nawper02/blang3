import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget

from stack import Stack
from data import Data
from parser import Parser
from interpreter import Interpreter
from visualizer import Visualizer

# TODO: Fully implement QT
# TODO: Make matrw rows and cols scale to fit in window until a certain point at which scroll is enabled?
# TODO: Fill in commands -- sqrt broken
# TODO: add more functionality to macrowriter -- control flow? args?
# TODO: Catch up to old version in misc features
# TODO: Add stats functionality -- distributions, etc
# TODO: Add units functionality using new strings functionality
# TODO: Make macro label a macro browser where you can expand/open and edit macros
# TODO: Make var label a var browser where you can edit / remove values

# OLD TODOS:
"""
# ADD #
# TODO: FINISH MATRW: more visual improvement?
# TODO:             --> Add safety for types in stack with arrays
# TODO:             --> add functions to do on arrays! dot product, etc
# TODO: remove stupid stuff from units?
# TODO: Make units tab with categories?
# TODO: add more functions/methods to function definitions / execution
# TODO: conversions -- dtr(deg to rad), rtd(rad to deg), ctpd(cartesian to polar), ctsd(cartesian to spherical),
# TODO:                ctcd(cartesian to cylindrical) and other way for all as well as xxxr for radians.

# REFACTOR #
# TODO: make print_stack print abbreviated units ( inside print object method units elif)
# TODO: make transpose work on [1,2,3] pushes
# TODO: add displaytypes for all stack objects

# TEST #
# TODO: test trig functions, test units thuroughly
"""


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
