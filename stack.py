from stack_object import StackObject
import numpy as np


class Stack:
    def __init__(self, data):
        self.data = data
        self.stack_list = []
        self.clipboard = StackObject(888)

    def __str__(self):
        return str(self.stack_list)

    def ret(self):
        return self.popval()

    def auto_push(self, stack_object: StackObject):
        try:
            self.stack_list.append(stack_object)
        except Exception as e:
            self.data.log.append(str(e))

    def pop(self):
        try:
            return self.stack_list.pop()
        except Exception as e:
            self.data.log.append(str(e))

    def popval(self):
        try:
            return self.stack_list.pop().value
        except Exception as e:
            self.data.log.append(str(e))

    def sum_stack(self):
        try:
            return sum([x.value for x in self.stack_list])
        except Exception as e:
            self.data.log.append(str(e))

    def prod_stack(self):
        try:
            return np.prod([x.value for x in self.stack_list])
        except Exception as e:
            self.data.log.append(str(e))

    def clear(self):
        self.stack_list.clear()

    def copy(self):
        self.clipboard = self.stack_list[-1]

    def paste(self):
        self.stack_list.append(self.clipboard)

    def get_full_stack_string(self):
        stack_string = ""
        for i in range(19, 0, -1):
            if i < 11:
                if i > len(self.stack_list):
                    stack_string += f" {i - 1}:\t \n"
                else:
                    stack_string += f" {i - 1}:\t {str(self.stack_list[-i])} \n"
            else:
                if i > len(self.stack_list):
                    stack_string += f"{i - 1}:\t \n"
                else:
                    stack_string += f"{i - 1}:\t {str(self.stack_list[-i])} \n"
        return stack_string
