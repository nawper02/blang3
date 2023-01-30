from command_handler import CommandHandler
from stack_handler import StackHandler


class Interpreter:
    def __init__(self, stack, data, parser):
        self.stack = stack
        self.data = data
        self.parser = parser
        self.stack_handler = StackHandler(self.stack, self.data, self.parser)
        self.command_handler = CommandHandler(self.stack, self.data, self.parser, self.stack_handler, self)

    def interpret_tokens(self, tokens):
        for token in tokens:
            if self.parser.is_value(token) or self.parser.is_string(token):
                self.stack_handler.handle_token(token)
            elif self.parser.is_cmd(token):
                self.command_handler.handle_token(token)
            elif len(tokens) == 1 and token == "":
                self.command_handler.handle_token(token)
            else:
                pass
