from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QEvent
from stack_object import StackObject
from variable_name_prompt import VariableNamePrompt


class Visualizer(QtWidgets.QMainWindow):
    def __init__(self, blang, *args):
        super(Visualizer, self).__init__()
        uic.loadUi('/Users/kinblandford/PycharmProjects/blang/blang2_prototype_ui.ui', self)
        downarrow_icon_path = "/Users/kinblandford/PycharmProjects/blang/downarrow.png"

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
        QListWidget {
            selection-background-color: rgb(90, 90, 90)
        }
        QTreeWidget {
            selection-background-color: rgb(90, 90, 90)
        }
        QComboBox {
            selection-background-color: rgb(90, 90, 90)
        }
        """
        )

        # connect objects
        self.input = self.findChild(QtWidgets.QLineEdit, 'input')
        self.log_scrollarea_label = self.findChild(QtWidgets.QLabel, 'log_scrollarea_label')

        self.varw_done_button = self.findChild(QtWidgets.QPushButton, 'varw_done_button')
        self.varw_done_button_2 = self.findChild(QtWidgets.QPushButton, 'varw_done_button_2')
        self.varw_delete_button = self.findChild(QtWidgets.QPushButton, 'varw_delete_button')
        self.varw_current_vars_list = self.findChild(QtWidgets.QListWidget, 'varw_listwidget')
        self.varw_name_lineedit = self.findChild(QtWidgets.QLineEdit, 'varw_name_lineedit')
        self.varw_name_lineedit_2 = self.findChild(QtWidgets.QLineEdit, 'varw_name_lineedit_2')
        self.varw_value_lineedit = self.findChild(QtWidgets.QLineEdit, 'varw_value_lineedit')
        self.varw_index_lineedit = self.findChild(QtWidgets.QLineEdit, 'varw_index_lineedit')

        self.fnwrtr_current_functions_tree = self.findChild(QtWidgets.QTreeWidget, 'fnwrtr_tree')
        self.fnwrtr_done_button = self.findChild(QtWidgets.QPushButton, 'fnwrtr_done_button')
        self.fnwrtr_textedit = self.findChild(QtWidgets.QPlainTextEdit, 'fnwrtr_textedit')
        self.fnwrtr_combobox = self.findChild(QtWidgets.QComboBox, 'fnwrtr_combobox')
        self.fnwrtr_new_folder_lineedit = self.findChild(QtWidgets.QLineEdit, 'fnwrtr_new_folder_lineedit')
        self.fnwrtr_new_folder_done_button = self.findChild(QtWidgets.QPushButton, 'fnwrtr_new_folder_done_button')

        self.matrw_cols_spinbox = self.findChild(QtWidgets.QSpinBox, 'matrw_cols_spinbox')
        self.matrw_rows_spinbox = self.findChild(QtWidgets.QSpinBox, 'matrw_rows_spinbox')
        self.matrw_done_button = self.findChild(QtWidgets.QPushButton, 'matrw_done_button')
        self.matrw_tablewidget = self.findChild(QtWidgets.QTableWidget, 'matrw_tablewidget')

        self.stack_listwidget = self.findChild(QtWidgets.QListWidget, 'stack_listwidget')

        # connect functionality
        self.input.returnPressed.connect(self.handle_input)
        self.stack_listwidget.itemDoubleClicked.connect(self.handle_stack_listwidget_double_clicked)
        self.stack_listwidget.installEventFilter(self)

        self.varw_done_button.clicked.connect(self.handle_varw_done_button)
        self.varw_done_button_2.clicked.connect(self.handle_varw_done_button_2)
        self.varw_delete_button.clicked.connect(self.handle_varw_delete_button)
        self.varw_current_vars_list.itemDoubleClicked.connect(self.handle_varw_current_vars_list_double_clicked)

        self.fnwrtr_done_button.clicked.connect(self.handle_fnwrtr_done_button)
        self.fnwrtr_new_folder_done_button.clicked.connect(self.handle_fnwrtr_new_folder_done_button)
        self.fnwrtr_current_functions_tree.itemDoubleClicked.connect(self.handle_fnwrtr_current_functions_tree_double_clicked)

        self.matrw_done_button.clicked.connect(self.handle_matrw_done_button)
        self.matrw_rows_spinbox.valueChanged.connect(self.handle_matrw_rows_spinbox)
        self.matrw_cols_spinbox.valueChanged.connect(self.handle_matrw_cols_spinbox)
        self.matrw_tablewidget.cellChanged.connect(self.handle_matrw_tablewidget_cell_changed)

        # create shortcuts for basic stack operations
        self.stack_up_shortcut = QShortcut(QKeySequence("Up"), self)
        self.stack_up_shortcut.activated.connect(self.handle_stack_up_shortcut)
        self.stack_down_shortcut = QShortcut(QKeySequence("Down"), self)
        self.stack_down_shortcut.activated.connect(self.handle_stack_down_shortcut)
        self.stack_right_shortcut = QShortcut(QKeySequence("Right"), self)
        self.stack_right_shortcut.activated.connect(self.handle_stack_right_shortcut)
        self.stack_pop_shortcut = QShortcut(QKeySequence("Backspace"), self)
        self.stack_pop_shortcut.activated.connect(self.handle_stack_pop_shortcut)
        self.stack_multiply_shortcut = QShortcut(QKeySequence("*"), self)
        self.stack_multiply_shortcut.activated.connect(self.handle_stack_multiply_shortcut)
        self.stack_divide_shortcut = QShortcut(QKeySequence("/"), self)
        self.stack_divide_shortcut.activated.connect(self.handle_stack_divide_shortcut)
        self.stack_add_shortcut = QShortcut(QKeySequence("+"), self)
        self.stack_add_shortcut.activated.connect(self.handle_stack_add_shortcut)
        self.stack_subtract_shortcut = QShortcut(QKeySequence("-"), self)
        self.stack_subtract_shortcut.activated.connect(self.handle_stack_subtract_shortcut)
        self.stack_power_shortcut = QShortcut(QKeySequence("^"), self)
        self.stack_power_shortcut.activated.connect(self.handle_stack_power_shortcut)
        self.escape_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.escape_shortcut.activated.connect(self.escape_input)
        self.enter_input_shortcut = QShortcut(QKeySequence("i"), self)
        self.enter_input_shortcut.activated.connect(self.enter_input)
        self.stack_get_1_shortcut = QShortcut(QKeySequence("1"), self)
        self.stack_get_1_shortcut.activated.connect(self.handle_stack_get_1_shortcut)
        self.stack_get_2_shortcut = QShortcut(QKeySequence("2"), self)
        self.stack_get_2_shortcut.activated.connect(self.handle_stack_get_2_shortcut)
        self.stack_get_3_shortcut = QShortcut(QKeySequence("3"), self)
        self.stack_get_3_shortcut.activated.connect(self.handle_stack_get_3_shortcut)
        self.stack_get_4_shortcut = QShortcut(QKeySequence("4"), self)
        self.stack_get_4_shortcut.activated.connect(self.handle_stack_get_4_shortcut)
        self.stack_get_5_shortcut = QShortcut(QKeySequence("5"), self)
        self.stack_get_5_shortcut.activated.connect(self.handle_stack_get_5_shortcut)
        self.stack_get_6_shortcut = QShortcut(QKeySequence("6"), self)
        self.stack_get_6_shortcut.activated.connect(self.handle_stack_get_6_shortcut)
        self.stack_get_7_shortcut = QShortcut(QKeySequence("7"), self)
        self.stack_get_7_shortcut.activated.connect(self.handle_stack_get_7_shortcut)
        self.stack_get_8_shortcut = QShortcut(QKeySequence("8"), self)
        self.stack_get_8_shortcut.activated.connect(self.handle_stack_get_8_shortcut)
        self.stack_get_9_shortcut = QShortcut(QKeySequence("9"), self)
        self.stack_get_9_shortcut.activated.connect(self.handle_stack_get_9_shortcut)
        self.stack_get_0_shortcut = QShortcut(QKeySequence("0"), self)
        self.stack_get_0_shortcut.activated.connect(self.handle_stack_get_0_shortcut)

        # set up tablewidget
        self.matrw_tablewidget.setColumnCount(self.blang.data.matrw_cols)
        self.matrw_tablewidget.setRowCount(self.blang.data.matrw_rows)

        # initialize variable name prompt
        self.prompt = None

        # set initial labels
        self.update_all()

    def eventFilter(self, source, event):
        if source is self.stack_listwidget and event.type() == event.Type.ContextMenu:
            menu = QtWidgets.QMenu()
            menu.addAction('Save as Variable')

            if menu.exec(event.globalPos()):
                item = source.itemAt(event.pos())
                try:
                    index = int(item.text().split("\t")[0].strip(":"))
                    stack_object = self.blang.interpreter.stack_handler.stack.get(index + 1)

                    self.prompt = VariableNamePrompt(self, stack_object)
                except AttributeError:
                    pass
            return True #indent?
        return super().eventFilter(source, event)

    def handle_input(self):
        s = self.input.text()
        self.input.clear()
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize(s))
        self.update_all()

    def escape_input(self):
        self.log_scrollarea_label.setFocus()
        # this is a hack to get the focus off of the input lineedit
        # if the log label is ever something else, this will break

    def enter_input(self):
        self.input.setFocus()

    def handle_stack_divide_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.div'))
        self.update_all()

    def handle_stack_up_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.up'))
        self.update_all()

    def handle_stack_down_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.down'))
        self.update_all()

    def handle_stack_pop_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.pop'))
        self.update_all()

    def handle_stack_multiply_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.x'))
        self.update_all()

    def handle_stack_add_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.add'))
        self.update_all()

    def handle_stack_subtract_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.sub'))
        self.update_all()

    def handle_stack_power_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.xty'))
        self.update_all()

    def handle_stack_right_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.swap'))
        self.update_all()

    def handle_stack_get_1_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(1)'))
        self.update_all()

    def handle_stack_get_2_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(2)'))
        self.update_all()

    def handle_stack_get_3_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(3)'))
        self.update_all()

    def handle_stack_get_4_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(4)'))
        self.update_all()

    def handle_stack_get_5_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(5)'))
        self.update_all()

    def handle_stack_get_6_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(6)'))
        self.update_all()

    def handle_stack_get_7_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(7)'))
        self.update_all()

    def handle_stack_get_8_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(8)'))
        self.update_all()

    def handle_stack_get_9_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(9)'))
        self.update_all()

    def handle_stack_get_0_shortcut(self):
        self.blang.interpreter.interpret_tokens(self.blang.parser.tokenize('.get(0)'))
        self.update_all()


    def handle_varw_done_button(self):
        name = self.varw_name_lineedit.text()
        value = self.blang.parser.get_value(self.varw_value_lineedit.text(), allow_string_value=True)
        if name not in (None, '') and value not in (None, ''):
            self.varw_name_lineedit.clear()
            self.varw_value_lineedit.clear()
            self.blang.interpreter.command_handler.define_var([name, value])
            self.update_all()

    def handle_varw_done_button_2(self):
        name = self.varw_name_lineedit_2.text()
        index = self.varw_index_lineedit.text()
        if name not in (None, '') and index not in (None, ''):
            self.blang.interpreter.command_handler.define_var_from_index([name, index])
            self.varw_index_lineedit.clear()
            self.varw_name_lineedit_2.clear()
            self.update_all()

    def handle_varw_current_vars_list_double_clicked(self):
        try:
            item = self.varw_current_vars_list.currentItem().text()
            name = item.split("=")[0].strip(" ")
            self.blang.interpreter.stack_handler.handle_token(name)
            self.update_all()
        except AttributeError:
            pass

    def handle_fnwrtr_current_functions_tree_double_clicked(self):
        try:
            item = self.fnwrtr_current_functions_tree.currentItem().text(0)
            name = item.split("(")[0].strip(" .")
            self.fnwrtr_textedit.setPlainText(self.blang.data.get_full_bfunction_string(name))
            self.update_all()
        except AttributeError:
            pass

    def handle_stack_listwidget_double_clicked(self):
        try:
            index = int(self.stack_listwidget.currentItem().text().split("\t")[0].strip(":"))
            stack_object = self.blang.interpreter.stack_handler.stack.get(index + 1)
            self.blang.interpreter.stack_handler.stack.auto_push(stack_object)
            self.update_all()
        except AttributeError:
            pass

    def handle_varw_delete_button(self):
        try:
            item = self.varw_current_vars_list.currentItem().text()
            name = item.split("=")[0].strip(" ")
            self.blang.data.rm('vars', name)
            self.update_all()
        except AttributeError:
            pass

    def handle_fnwrtr_done_button(self):
        body = self.fnwrtr_textedit.toPlainText()
        self.fnwrtr_textedit.clear()
        folder = self.fnwrtr_combobox.currentText()
        self.blang.interpreter.command_handler.define_bfunction(body, folder)
        self.update_all()

    def handle_fnwrtr_new_folder_done_button(self):
        name = self.fnwrtr_new_folder_lineedit.text()
        self.fnwrtr_new_folder_lineedit.clear()
        self.blang.data.define_bfunction_folder(name)
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
        except AttributeError:
            pass

    def update_log(self):
        self.log_scrollarea_label.setText(self.blang.data.get_log_string())

    def update_varw(self):
        self.varw_current_vars_list.clear()
        var_listwidget_items = self.blang.data.get_var_listwidget_items()
        for item in var_listwidget_items:
            self.varw_current_vars_list.addItem(item)

    def update_fnwrtr(self):
        folders = self.blang.data.get_fnwrtr_folders()
        self.fnwrtr_combobox.clear()
        self.fnwrtr_combobox.addItems(folders)
        items = self.blang.data.get_fnwrtr_tree_items()
        self.fnwrtr_current_functions_tree.clear()
        self.fnwrtr_current_functions_tree.insertTopLevelItems(0, items)

    def update_stack(self):
        #self.stack_label.setText(self.blang.stack.get_full_stack_string())
        self.stack_listwidget.clear()
        stack_listwidget_items = self.blang.stack.get_stack_listwidget_items()
        for item in stack_listwidget_items:
            self.stack_listwidget.addItem(item)

    def update_matrw(self):
        self.matrw_tablewidget.clear()
        self.blang.data.update_matrw_mat()
        self.matrw_tablewidget.setColumnCount(self.blang.data.matrw_cols)
        self.matrw_tablewidget.setRowCount(self.blang.data.matrw_rows)

    def update_all(self):
        self.update_log()
        self.update_varw()
        self.update_fnwrtr()
        self.update_stack()
        self.update_matrw()
