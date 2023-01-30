from stack_object import StackObject


class Stack:
    def __init__(self):
        self.stack_list = []

    def __str__(self):
        return str(self.stack_list)

    def auto_push(self, stack_object: StackObject):
        try:
            self.stack_list.append(stack_object)
        except Exception as e:
            print(str(e))

    def clear(self):
        self.stack_list.clear()

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
