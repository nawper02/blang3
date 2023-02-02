from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QHeaderView
from stack_object import StackObject


class Visualizer(QtWidgets.QMainWindow):
    def __init__(self, blang, *args):
        super(Visualizer, self).__init__()
        uic.loadUi('/Users/kinblandford/PycharmProjects/blang/blang2_ui.ui', self)

        # set stuff up
        self.blang = blang
        self.setWindowTitle("blang")
        self.setStyleSheet(
        """
        QTabBar::tab:selected {
            border-radius: 1px;
            background: grey;
        }
        QTabBar::tab:!selected {
            border-radius: 1px;
            background: rgb(90, 90, 90);
        }
        QTabBar::tab {
        min-width: 85px;
        min-height: 20px;
        }
        QTableView {
        selection-background-color: rgb(90, 90, 90)
        }
        """
        )

        # connect objects
        self.input = self.findChild(QtWidgets.QLineEdit, 'input')
        self.log_scrollarea_label = self.findChild(QtWidgets.QLabel, 'log_scrollarea_label')
        self.varw_done_button = self.findChild(QtWidgets.QPushButton, 'varw_done_button')
        self.varw_current_vars_label = self.findChild(QtWidgets.QLabel, 'varw_current_vars_label')
        self.varw_name_lineedit = self.findChild(QtWidgets.QLineEdit, 'varw_name_lineedit')
        self.varw_value_lineedit = self.findChild(QtWidgets.QLineEdit, 'varw_value_lineedit')
        self.macrw_current_macros_label = self.findChild(QtWidgets.QLabel, 'macrw_current_macros_label')
        self.macrw_done_button = self.findChild(QtWidgets.QPushButton, 'macrw_done_button')
        self.macrw_textedit = self.findChild(QtWidgets.QPlainTextEdit, 'macrw_textedit')
        self.macrw_name_lineedit = self.findChild(QtWidgets.QLineEdit, 'macrw_name_lineedit')
        self.matrw_cols_spinbox = self.findChild(QtWidgets.QSpinBox, 'matrw_cols_spinbox')
        self.matrw_rows_spinbox = self.findChild(QtWidgets.QSpinBox, 'matrw_rows_spinbox')
        self.matrw_done_button = self.findChild(QtWidgets.QPushButton, 'matrw_done_button')
        self.matrw_tablewidget = self.findChild(QtWidgets.QTableWidget, 'matrw_tablewidget')
        self.stack_label = self.findChild(QtWidgets.QLabel, 'stack_label')

        # connect functionality
        self.input.returnPressed.connect(self.handle_input)
        self.varw_done_button.clicked.connect(self.handle_varw_done_button)
        self.macrw_done_button.clicked.connect(self.handle_macrw_done_button)
        self.matrw_done_button.clicked.connect(self.handle_matrw_done_button)
        self.matrw_rows_spinbox.valueChanged.connect(self.handle_matrw_rows_spinbox)
        self.matrw_cols_spinbox.valueChanged.connect(self.handle_matrw_cols_spinbox)
        self.matrw_tablewidget.cellChanged.connect(self.handle_matrw_tablewidget_cell_changed)

        # set up tablewidget
        self.matrw_tablewidget.setColumnCount(self.blang.data.matrw_cols)
        self.matrw_tablewidget.setRowCount(self.blang.data.matrw_rows)

        # set initial labels
        self.update_all()

    def handle_input(self):
        s = self.input.text()
        self.input.clear()
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize(s))
        self.update_all()

    def handle_varw_done_button(self):
        name = self.varw_name_lineedit.text()
        value = self.blang.parser.get_value(self.varw_value_lineedit.text(), allow_string_value=True)
        self.varw_name_lineedit.clear()
        self.varw_value_lineedit.clear()
        self.blang.interpreter.command_handler.define_var([name, value])
        self.update_all()

    def handle_macrw_done_button(self):
        name = self.macrw_name_lineedit.text()
        value = self.macrw_textedit.toPlainText()
        self.macrw_name_lineedit.clear()
        self.macrw_textedit.clear()
        self.blang.interpreter.command_handler.define_macro([name, value])
        self.update_all()

    def handle_matrw_done_button(self):
        # Bypass parser because stackobject can be created directly from matrix
        stack_object = StackObject(self.blang.data.matrw_mat)
        self.blang.stack.auto_push(stack_object)
        self.update_all()

    def handle_matrw_rows_spinbox(self):
        self.blang.data.matrw_rows = self.matrw_rows_spinbox.value()
        self.update_all()

    def handle_matrw_cols_spinbox(self):
        self.blang.data.matrw_cols = self.matrw_cols_spinbox.value()
        self.update_all()

    def handle_matrw_tablewidget_cell_changed(self):
        row = self.matrw_tablewidget.currentRow()
        col = self.matrw_tablewidget.currentColumn()
        try:
            value = float(self.matrw_tablewidget.item(row, col).text())
            self.blang.data.matrw_mat[row, col] = value
        except ValueError:
            pass
        except UnboundLocalError:
            pass

    def update_log(self):
        self.log_scrollarea_label.setText(self.blang.data.get_log_string())

    def update_varw(self):
        self.varw_current_vars_label.setText(self.blang.data.get_var_string())

    def update_macrw(self):
        self.macrw_current_macros_label.setText(self.blang.data.get_macrw_string())

    def update_stack(self):
        self.stack_label.setText(self.blang.stack.get_full_stack_string())

    def update_matrw(self):
        self.matrw_tablewidget.clear()
        self.blang.data.update_matrw_mat()
        self.matrw_tablewidget.setColumnCount(self.blang.data.matrw_cols)
        self.matrw_tablewidget.setRowCount(self.blang.data.matrw_rows)

    def update_all(self):
        self.update_log()
        self.update_varw()
        self.update_macrw()
        self.update_stack()
        self.update_matrw()
