import re
import numpy as np


class CommandHandler:
    def __init__(self, stack, data, parser, stack_handler, interpreter):
        self.stack = stack
        self.data = data
        self.parser = parser
        self.interpreter = interpreter
        self.stack_handler = stack_handler

    def handle_token(self, token):
        # The one exception -- if token is an empty string, just execute it to call the dup method
        if token == "":
            self.execute_command(token, [])

        else:
            # Extract command and args from token
            match = re.match(r'\.(\w+)(\(.*\))?', token)

            # Index out the groups (command and args)
            command = match.group(1)                            # COMMAND
            if match.group(2) is None:
                args_string = ""                                # EMPTY ARGS
            else:
                args_string = match.group(2).strip("( )")       # ARGS

            # Find string arguments and 'hide' them from the split
            string_matches = re.findall(r'\'.*?\'', args_string)
            for match in string_matches:
                # Replace the substring with a special character
                args_string = args_string.replace(match, "__STRING__")

            # Find list arguments and 'hide' them from the split
            list_matches = re.findall(r'\[.*?\]', args_string)
            for match in string_matches:
                # Replace the substring with a special character
                args_string = args_string.replace(match, "__LIST__")

            args = []
            # Split the args string into a list of args
            for arg in args_string.split(" "):
                # If the arg is a value, get that value and append it to the args list
                if self.parser.is_value(arg.strip()):
                    args.append(self.parser.get_value(arg.strip()))
                # If the arg is a list, get that list and append it to the args list
                elif arg == "__LIST__":
                    args.append(self.parser.get_value(list_matches.pop(0).strip("'")))
                # If the arg is the string special character, put the string back in
                elif arg == "__STRING__":
                    args.append(string_matches.pop(0).strip("'"))

            # Give the command and args to the execute_command method
            self.execute_command(command, args)

    def execute_command(self, command: str, args: list):
        match command.upper():

            case "":
                self.dup(args)

            case "POP":
                self.pop(args)

            case "ADD":
                self.add(args)

            case "SUB":
                self.sub(args)

            case "X":
                self.times(args)

            case "DIV":
                self.div(args)

            case "SQRT":
                self.sqrt(args)

            case "SQ":
                self.sq(args)

            case "LN":
                self.ln(args)

            case "LBY":
                self.lby(args)

            case "SIN":
                self.sin(args)

            case "SIND":
                self.sind(args)

            case "COS":
                self.cos(args)

            case "COSD":
                self.cosd(args)

            case "TAN":
                self.tan(args)

            case "TAND":
                self.tand(args)

            case "ASIN":
                self.asin(args)

            case "ASIND":
                self.asind(args)

            case "ACOS":
                self.acos(args)

            case "ACOSD":
                self.acosd(args)

            case "ATAN":
                self.atan(args)

            case "ATAND":
                self.atand(args)

            case "CHS":
                self.chs(args)

            case "REC":
                self.rec(args)

            case "EXP":
                self.exp(args)

            case "HYP":
                self.hyp(args)

            case "XRY":
                self.xry(args)

            case "XTY":
                self.xty(args)

            case "DOT":
                self.dot(args)

            case "NORM":
                self.norm(args)

            case "CROSS":
                self.cross(args)

            case "SWAP":
                self.swap(args)

            case "DUP":
                self.dup(args)

            case "DET":
                self.det(args)

            case "INV":
                self.inv(args)

            case "TRANS":
                self.transpose(args)

            case "SOLVE":
                self.solve(args)

            case "SUM":
                self.sum_stack(args)

            case "C":
                self.copy(args)

            case "V":
                self.paste(args)

            case "CLEAR":
                self.clear(args)

            case "VAR":
                self.define_var(args)

            case "HELP":
                self.help(args)

            # Remember to add to reserved keywords when making new commands!

            case _:
                if command in self.data.macros.keys():
                    self.execute_macro([command])

    def add(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(x + y)
        except Exception as e:
            self.data.log.append(str(e))

    def sub(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(y - x)
        except Exception as e:
            self.data.log.append(str(e))

    def times(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(y * x)
        except Exception as e:
            self.data.log.append(str(e))

    def div(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(y / x)
        except Exception as e:
            self.data.log.append(str(e))

    def sqrt(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(np.sqrt(x))
        except Exception as e:
            self.data.log.append(str(e))

    def dup(self, args):
        try:
            self.stack.stack_list.append(self.stack.stack_list[0])
        except Exception as e:
            self.data.log.append(str(e))

    def pop(self, args):
        try:
            self.stack.stack_list.pop()
        except Exception as e:
            self.data.log.append(str(e))

    def clear(self, args):
        try:
            self.stack.clear()
        except Exception as e:
            self.data.log.append(str(e))

    def execute_macro(self, args):
        try:
            key = args[0]
            macro = self.data.macros[key]
            self.interpreter.interpret_tokens(self.parser.tokenize_macro(macro))
        except Exception as e:
            self.data.log.append(str(e))

    def define_var(self, args):
        try:
            name = args[0]
            value = args[1]
            self.data.define_var(name, value)
        except Exception as e:
            self.data.log.append(str(e))

    def define_macro(self, args):
        try:
            name = args[0]
            value = args[1]
            self.data.define_macro(name, value)
        except Exception as e:
            self.data.log.append(str(e))

    @staticmethod
    def help(args: list):
        import webbrowser
        webbrowser.open('https://www.kinblandford.com/home/blang', new=2)