from datetime import date
import numpy as np


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
        self.macros = {
            "example macro": "non implemented test macro"
        }

        self.matrw_rows = 3
        self.matrw_cols = 3
        self.matrw_mat = np.zeros((self.matrw_rows, self.matrw_cols), dtype=float)

        today = date.today()
        init_str = today.strftime("%b-%d-%Y")
        self.log = [f"BLANG v2.0.0 -- {init_str}"]

    def update_matrw_mat(self):
        self.matrw_mat = np.zeros((self.matrw_rows, self.matrw_cols), dtype=float)

    def define_var(self, name: str, value):
        self.vars[name] = value

    def define_macro(self, name: str, value: str):
        self.macros[name] = value

    def get_log_string(self):
        log_string = ""
        for index, entry in enumerate(self.log):
            log_string += f"{[index]} : {entry}\n"
        for line in range(5 - len(self.log)):
            log_string += "\n"
        return log_string

    def get_var_string(self):
        vars_string = ""
        for entry in self.vars:
            vars_string += f"{entry} = {self.vars[entry]}\n"
        for line in range(27 - len(self.vars)):
            vars_string += "\n"
        return vars_string

    def get_macrw_string(self):
        macrw_string = ""
        for entry in self.macros:
            macrw_string += f"{entry}\n"
            for line in self.macros[entry].split("\n"):
                macrw_string += f"    {line}\n"
            macrw_string += "\n"
        for line in range(25 - len(self.macros)):
            macrw_string += "\n"
        return macrw_string
