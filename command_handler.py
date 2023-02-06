import re
import math
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

            case "TEQ":
                self.teq(args)

            case "TNE":
                self.tne(args)

            case "CLEAR":
                self.clear(args)

            case "VAR":
                self.define_var(args)

            case "VARIND":
                self.define_var_from_index(args)

            case "PVAR":
                self.define_pvar(args)

            case "PVARIND":
                self.define_pvar_from_index(args)

            case "GETPVAR":
                self.get_pvar(args)

            case "RM":
                self.rm(args)

            case "CLEARVARS":
                self.clear_vars(args)

            case "CLEARPVARS":
                self.clear_pvars(args)

            case "CLEARMACROS":
                self.clear_macros(args)

            case "CLEARLOG":
                self.clear_log(args)

            case "CLEARALLDATA":
                self.clear_all_data(args)

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

    def sq(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(x * x)
        except Exception as e:
            self.data.log.append(str(e))

    def ln(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.log(x))
        except Exception as e:
            self.data.log.append(str(e))

    def lby(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(math.log(x, y))
        except Exception as e:
            self.data.log.append(str(e))

    def sin(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.sin(x))
        except Exception as e:
            self.data.log.append(str(e))

    def sind(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.sin(math.radians(x)))
        except Exception as e:
            self.data.log.append(str(e))

    def cos(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.cos(x))
        except Exception as e:
            self.data.log.append(str(e))

    def cosd(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.cos(math.radians(x)))
        except Exception as e:
            self.data.log.append(str(e))

    def tan(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.tan(x))
        except Exception as e:
            self.data.log.append(str(e))

    def tand(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.tan(math.radians(x)))
        except Exception as e:
            self.data.log.append(str(e))

    def asin(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.asin(x))
        except Exception as e:
            self.data.log.append(str(e))

    def asind(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.degrees(math.asin(x)))
        except Exception as e:
            self.data.log.append(str(e))

    def acos(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.acos(x))
        except Exception as e:
            self.data.log.append(str(e))

    def acosd(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.degrees(math.acos(x)))
        except Exception as e:
            self.data.log.append(str(e))

    def atan(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.atan(x))
        except Exception as e:
            self.data.log.append(str(e))

    def atand(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.degrees(math.atan(x)))
        except Exception as e:
            self.data.log.append(str(e))

    def chs(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(-x)
        except Exception as e:
            self.data.log.append(str(e))

    def rec(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(1.0/x)
        except Exception as e:
            self.data.log.append(str(e))

    def exp(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(math.exp(x))
        except Exception as e:
            self.data.log.append(str(e))

    def xry(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(pow(y, 1.0/x))
        except Exception as e:
            self.data.log.append(str(e))

    def xty(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(pow(x, y))
        except Exception as e:
            self.data.log.append(str(e))

    def dot(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(float(np.dot(x, y)))
        except Exception as e:
            self.data.log.append(str(e))

    def norm(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(x / np.linalg.norm(x))
        except Exception as e:
            self.data.log.append(str(e))

    def cross(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(np.cross(x, y))
        except Exception as e:
            self.data.log.append(str(e))

    def swap(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(x)
            self.stack_handler.handle_token(y)
        except Exception as e:
            self.data.log.append(str(e))

    def det(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(np.linalg.det(x))
        except Exception as e:
            self.data.log.append(str(e))

    def inv(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(np.linalg.inv(x))
        except Exception as e:
            self.data.log.append(str(e))

    def transpose(self, args):
        try:
            x = self.stack.popval()
            self.stack_handler.handle_token(np.transpose(x))
        except Exception as e:
            self.data.log.append(str(e))

    def solve(self, args):
        try:
            x = self.stack.popval()
            y = self.stack.popval()
            self.stack_handler.handle_token(np.linalg.solve(x, y))
        except Exception as e:
            self.data.log.append(str(e))

    def sum_stack(self, args):
        try:
            value = self.stack.sum_stack()
            self.stack.clear()
            self.stack_handler.handle_token(value)
        except Exception as e:
            self.data.log.append(str(e))

    def copy(self, args):
        try:
            self.stack.copy()
        except Exception as e:
            self.data.log.append(str(e))

    def paste(self, args):
        try:
            self.stack.paste()
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

    def define_var_from_index(self, args):
        try:
            name = args[0]
            index = int(args[1])
            value = self.stack.stack_list[index].value
            self.data.define_var(name, value)
        except Exception as e:
            self.data.log.append(str(e))

    def define_pvar(self, args):
        try:
            name = args[0]
            value = args[1]
            self.data.define_pvar(name, value)
        except Exception as e:
            self.data.log.append(str(e))

    def define_pvar_from_index(self, args):
        try:
            name = args[0]
            index = int(args[1])
            value = self.stack.stack_list[index].value
            self.data.define_pvar(name, value)
        except Exception as e:
            self.data.log.append(str(e))

    def get_pvar(self, args):
        try:
            name = args[0]
            value = self.data.get_pvar(name)
            self.stack_handler.handle_token(value)
        except Exception as e:
            self.data.log.append("KeyError: " + str(e))

    def rm(self, args):
        try:
            data_type = args[0]
            name = args[1]
            self.data.rm(data_type, name)
        except Exception as e:
            self.data.log.append("KeyError: " + str(e))

    def clear_vars(self, args):
        try:
            self.data.clear_vars()
        except Exception as e:
            self.data.log.append(str(e))

    def clear_pvars(self, args):
        try:
            self.data.clear_pvars()
        except Exception as e:
            self.data.log.append(str(e))

    def clear_macros(self, args):
        try:
            self.data.clear_macros()
        except Exception as e:
            self.data.log.append(str(e))

    def clear_log(self, args):
        try:
            self.data.clear_log()
        except Exception as e:
            self.data.log.append(str(e))

    def clear_all_data(self, args):
        try:
            self.data.clear_all_data()
        except Exception as e:
            self.data.log.append(str(e))

    def define_macro(self, args):
        try:
            name = args[0]
            value = args[1]
            self.data.define_macro(name, value)
        except Exception as e:
            self.data.log.append(str(e))

    def teq(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            self.stack_handler.handle_token(int(value1 == value2))
        except Exception as e:
            self.data.log.append(str(e))

    def tne(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            self.stack_handler.handle_token(int(value1 != value2))
        except Exception as e:
            self.data.log.append(str(e))

    @staticmethod
    def help(args: list):
        import webbrowser
        webbrowser.open('https://www.kinblandford.com/home/blang', new=2)