from datetime import date
import numpy as np
from bfunction import BFunction
from PyQt6.QtWidgets import QListWidgetItem, QTreeWidgetItem


class Data:
    def __init__(self):
        self.vars = {
            "e": 2.718281828459,
            "pi": 3.141592653589,
            "na": 6.0221408e+23,
            "bz": 1.380649e-23,
            "mp": 1.67262192e-27,
            "cp": 1.602e-19,
            "me": 9.1093837e-31,
            "ce": -1.602e-19
        }

        self.pvars = {}

        hyp = BFunction(".hyp(a b)\na .sq b .sq .add .sqrt")
        vdiv = BFunction(".vdiv(vin r1 r2)\nr1 r2 r1 .add .div vin .x")
        test = BFunction(".test(s)\ns")
        self.bfunctions = {"Misc": {f"{hyp.name}": hyp, f"{test.name}": test}, "ECE": {f"{vdiv.name}": vdiv}}

        self.reserved_words = \
            ["", "POP", "ADD", "SUB", "X", "DIV", "SQRT", "SQ", "LN", "LBY", "SIN", "SIND", "COS", "COSD", "TAN",
                "TAND", "ASIN", "ASIND", "ACOS", "ACOSD", "ATAN", "ATAND", "CHS", "REC", "EXP", "HYP", "XRY", "XTY",
                "DOT", "NORM", "CROSS", "SWAP", "DUP", "DET", "INV", "TRANS", "SOLVE", "SUM", "C", "V", "CLEAR",
                "VAR", "HELP"]

        self.matrw_rows = 3
        self.matrw_cols = 3
        self.matrw_mat = np.zeros((self.matrw_rows, self.matrw_cols), dtype=float)

        today = date.today()
        init_str = today.strftime("%b-%d-%Y")
        self.log = [f"BLANG v3.0.0 -- {init_str}"]

        self.dictionaries = {"vars": self.vars, "pvars": self.pvars, "bfunctions": self.bfunctions}

    def update_matrw_mat(self):
        self.matrw_mat = np.zeros((self.matrw_rows, self.matrw_cols), dtype=float)

    def define_bfunction(self, bfunction: BFunction, folder: str):
        if bfunction.name.upper() in self.reserved_words:
            self.log.append("WARN: BFunction name assigned to reserved word -- execution will not be possible")
        #self.bfunctions[bfunction.name] = bfunction
        self.bfunctions[folder][bfunction.name] = bfunction

    def find_bfunction(self, name: str):
        for folder in self.bfunctions:
            if name in self.bfunctions[folder]:
                return self.bfunctions[folder][name]
        return None

    def define_var(self, name: str, value):
        self.vars[name] = value

    def define_pvar(self, name: str, value):
        self.pvars[name] = value

    def get_var(self, name):
        return self.vars[name]

    def get_pvar(self, name):
        return self.pvars[name]

    def get_log_string(self):
        log_string = ""
        for index, entry in enumerate(self.log):
            log_string += f"{[index]} : {entry}\n"
        for line in range(5 - len(self.log)):
            log_string += "\n"
        return log_string

    def get_var_listwidget_items(self):
        var_listwidget_items = []
        for entry in self.vars:
            var_listwidget_items.append(QListWidgetItem(f"{entry} = {self.vars[entry]}"))
        return var_listwidget_items

    def get_fnwrtr_tree_items(self):
        fnwrtr_tree_items = []
        for key, values in self.bfunctions.items():
            item = QTreeWidgetItem([key])
            for key2, value2 in values.items():
                #name, args = value2.get_name_and_args()
                child = QTreeWidgetItem([value2.head])
                item.addChild(child)
            fnwrtr_tree_items.append(item)
        return fnwrtr_tree_items

    def get_fnwrtr_folders(self):
        return list(self.bfunctions.keys())

    def get_full_bfunction_string(self, name):
        bfunc = self.find_bfunction(name)
        return bfunc.body

    def define_bfunction_folder(self, name):
        self.bfunctions[name] = {}

    def get_bfuncrw_string(self):
        bfuncrw_string = ""
        for entry in self.bfunctions:
            bfuncrw_string += f"{entry}({self.bfunctions[entry].get_pretty_args()})\n"
            for line in self.bfunctions[entry].pgrm_lines:
                bfuncrw_string += f"    {line}\n"
            bfuncrw_string += "\n"
        for line in range(25 - len(self.bfunctions)):
            bfuncrw_string += "\n"
        return bfuncrw_string

    def rm(self, data_type, name):
        self.dictionaries[data_type].pop(name)

    def clear_pvars(self):
        self.pvars.clear()

    def clear_vars(self):
        self.vars.clear()

    def clear_log(self):
        self.log.clear()

    def clear_bfunctions(self):
        self.bfunctions.clear()

    def clear_all_data(self):
        self.clear_pvars()
        self.clear_vars()
        self.clear_log()
        self.clear_bfunctions()
