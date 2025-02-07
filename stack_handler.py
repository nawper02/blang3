from stack_object import StackObject


class StackHandler:
    def __init__(self, stack, data, parser):
        self.stack = stack
        self.data = data
        self.parser = parser

    def handle_token(self, token):
        value = self.parser.get_value(token, allow_string_value=True)
        stack_object = StackObject(value)
        self.stack.auto_push(stack_object)
