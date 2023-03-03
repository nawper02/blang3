from command_handler import CommandHandler
from stack_handler import StackHandler


class Interpreter:
    def __init__(self, stack, data, parser):
        self.run_state = True
        self.stack = stack
        self.data = data
        self.parser = parser
        self.stack_handler = StackHandler(self.stack, self.data, self.parser)
        self.command_handler = CommandHandler(self.stack, self.data, self.parser, self.stack_handler, self)

    def interpret_tokens(self, tokens):
        for token in tokens:
            if self.parser.is_value(token) or self.parser.is_string(token):
                # Putting 'is_string' in 'is_value' (an attempt at refactoring) broke everything for no reason.
                self.interpret_value(token)
            elif self.parser.is_cmd(token):
                self.interpret_command(token)
            elif len(tokens) == 1 and token == "":
                self.command_handler.handle_token(token)
            else:
                pass

    # this method handles regular values and conditional values
    def interpret_value(self, value):
        try:
            if type(value) != str:
                self.stack_handler.handle_token(value)

            else:
                if (value[0].upper(), self.run_state) in [('T', True), ('F', False)]:
                    self.stack_handler.handle_token(value)
                elif (value[0].upper(), self.run_state) in [('T', False), ('F', True)]:
                    pass
                else:
                    self.stack_handler.handle_token(value)

        except Exception as e:
            self.data.log.append(str(e))

    # this method handles regular commands and conditional commands
    def interpret_command(self, command):
        try:
            if (command[0].upper(), self.run_state) in [('T', True), ('F', False)]:
                self.command_handler.handle_token(command)
            elif (command[0].upper(), self.run_state) in [('T', False), ('F', True)]:
                pass
            else:
                self.command_handler.handle_token(command)
        except Exception as e:
            self.data.log.append(str(e))
