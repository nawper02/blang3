from datetime import date
import numpy as np
from bfunction import BFunction
from PyQt6.QtWidgets import QListWidgetItem


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

        example_bfunction = BFunction(".hyp(a b)\na .sq b .sq .add .sqrt")
        self.bfunctions = {}
        self.bfunctions[example_bfunction.name] = example_bfunction

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
        self.log = [f"BLANG v2.0.0 -- {init_str}"]

        self.dictionaries = {"vars": self.vars, "pvars": self.pvars, "bfunctions": self.bfunctions}

    def update_matrw_mat(self):
        self.matrw_mat = np.zeros((self.matrw_rows, self.matrw_cols), dtype=float)

    def define_bfunction(self, bfunction: BFunction):
        if bfunction.name.upper() in self.reserved_words:
            self.log.append("WARN: BFunction name assigned to reserved word -- execution will not be possible")
        self.bfunctions[bfunction.name] = bfunction

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

    # DEPRECATED
    def get_var_string(self):
        vars_string = ""
        for entry in self.vars:
            vars_string += f"{entry} = {self.vars[entry]}\n"
        for line in range(27 - len(self.vars)):
            vars_string += "\n"
        return vars_string

    def get_var_listwidget_items(self):
        var_listwidget_items = []
        for entry in self.vars:
            var_listwidget_items.append(QListWidgetItem(f"{entry} = {self.vars[entry]}"))
        return var_listwidget_items

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
