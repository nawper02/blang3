from PyQt6.QtWidgets import QDialog, QLineEdit
from PyQt6 import uic


class VariableNamePrompt(QDialog):
    def __init__(self, parent, stack_object):
        super().__init__()
        uic.loadUi('/Users/kinblandford/PycharmProjects/blang/variablenameprompt_ui.ui', self)

        # set stuff up
        self.setWindowTitle("")
        self.setStyleSheet(
            """
            QTableView {
            selection-background-color: rgb(90, 90, 90)
            }
            """
        )

        self.variable_name = None
        self.stack_object = stack_object
        self.parent = parent

        # find objects
        self.line_edit = self.findChild(QLineEdit, "line_edit")

        # connect functionality
        self.line_edit.returnPressed.connect(self.return_pressed)

        self.show()

    def return_pressed(self):

        if self.stack_object.value is not None and self.line_edit.text() != "":
            value = self.stack_object.value
            name = self.line_edit.text()

            self.parent.blang.data.define_var(name, value)
            self.parent.update_all()

        self.close()
