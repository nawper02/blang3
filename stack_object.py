import numpy as np


class StackObject:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if type(self.value) == float:
            return str(self.value)
        elif type(self.value) == str:
            return str(self.value)
        elif type(self.value) == list:
            return str(self.value)
        elif type(self.value) == np.ndarray:
            if len(self.value.shape) == 1:
                return str(self.value)
            else:
                arr_str = ""
                for index, row in enumerate(self.value):
                    if index == 0:
                        arr_str += f"[{row},\n"
                    elif 0 < index < (len(self.value) - 1):
                        arr_str += f"\t  {row},\n"
                    else:
                        arr_str += f"\t  {row}]"
            return arr_str

