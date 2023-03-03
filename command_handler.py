import re
import math

import numpy as np
from bfunction import BFunction


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
            match = re.match(r'[tTfF]?\.(\w+)(\(.*\))?', token) #CHANGETAG

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

            case "UP":
                self.up(args)

            case "DOWN":
                self.down(args)

            case "DUP":
                self.dup(args)

            case "GET":
                self.get(args)

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

            case "PROD":
                self.prod_stack(args)

            case "INT":
                self.integrate(args)

            case "DIF":
                self.differentiate(args)

            case "ROOTS":
                self.roots(args)

            case "C":
                self.copy(args)

            case "V":
                self.paste(args)

            case "TEQ":
                self.teq(args)

            case "TNE":
                self.tne(args)

            case "TGT":
                self.tgt(args)

            case "TLT":
                self.tlt(args)

            case "TGE":
                self.tge(args)

            case "TLE":
                self.tle(args)

            case "CLEAR":
                self.clear(args)

            case "RETURN":
                self.ret(args)

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

            case "CLEARBFUNCTIONS":
                self.clear_bfunctions(args)

            case "CLEARLOG":
                self.clear_log(args)

            case "CLEARALLDATA":
                self.clear_all_data(args)

            case "IOTA":
                self.iota(args)

            case "UNPACK":
                self.unpack(args)

            case "PACK":
                self.pack(args)

            case "REVERSE":
                self.reverse(args)

            case "EYE":
                self.eye(args)

            case "HELP":
                self.help(args)

            # Remember to add to reserved keywords when making new commands!

            case _:
                cmds = []
                for key, folder in self.data.bfunctions.items():
                    for name in folder.keys():
                        cmds.append(name)

                if command in cmds:
                    self.execute_bfunction(command, args)

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
            x = self.stack.pop()
            y = self.stack.pop()
            self.stack.stack_list.append(x)
            self.stack.stack_list.append(y)
        except Exception as e:
            self.data.log.append(str(e))

    def get(self, args):
        try:
            index = int(args[0])
            x = self.stack.stack_list[-index-1]
            self.stack_handler.handle_token(x.value)
        except Exception as e:
            self.data.log.append(str(e))

    def reverse(self, args):
        try:
            self.stack.stack_list.reverse()
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

    def prod_stack(self, args):
        try:
            value = self.stack.prod_stack()
            self.stack.clear()
            self.stack_handler.handle_token(value)
        except Exception as e:
            self.data.log.append(str(e))

    def integrate(self, args):
        # define interior integration functions

        def trapezoidal(command, x0, xf, n=1000):
            h = (xf - x0) / n
            x = np.linspace(x0, xf, n + 1)
            y = np.zeros(len(x))
            for index, element in enumerate(x):
                self.execute_command(command, [element]) # element is a list because execute_command expects a list
                y[index] = self.stack.ret()
            return h * np.sum(y[:-1] + y[1:]) / 2

        def quadrature(f, a, b, n=3):
            raise Exception("Quadrature does not currently work.")
            # cant remember what these are, been a while since numerical methods
            o = (b - a) / 2
            m = (b + a) / 2
            # get x and w from n using numpy
            x, w = np.polynomial.legendre.leggauss(n)
            # evaluate the function at the points
            vals = np.zeros(len(x))

            for index, element in enumerate(x):
                self.execute_command(f, [o * element + m])
                vals[index] = sum(self.stack.ret() * w)

            return o * np.sum(vals)

        try:  # assign args and hardcode type requirements
            bfunc_string: str = args[0]
            if not isinstance(bfunc_string, (str)):
                raise TypeError("The 'bfunction_name' argument must be a string")

            lower_bound: float = args[1]
            if not isinstance(lower_bound, (int, float, np.float64)):
                raise TypeError("The 'lower_bound' argument must be a number")

            upper_bound: float = args[2]
            if not isinstance(upper_bound, (int, float, np.float64)):
                raise TypeError("The 'upper_bound' argument must be a number")

            if len(args) > 3:
                method_string: str = args[3]
                if not isinstance(method_string, (str)):
                    raise TypeError("The 'method_string' argument must be a string")
            else:
                method_string = "TRAP"

            # integrate based on chosen method
            match method_string.upper():
                case "TRAP":
                    area = trapezoidal(bfunc_string, lower_bound, upper_bound, n = 1000)
                    self.stack_handler.handle_token(area)
                    # optional argument assignment can later be replaced with provided arguments from user
                case "QUAD":
                    area = quadrature(bfunc_string, lower_bound, upper_bound, n=3)
                    self.stack_handler.handle_token(area)
                case _:
                    raise ValueError(f"{method_string} is not a valid integration method")

        except Exception as e:
            self.data.log.append(str(e))

    def differentiate(self, args):
        # define interior differentiation functions
        def central_difference(command, x, h=1e-6):
            self.execute_command(command, [x + h])
            upper_val = self.stack.ret()
            self.execute_command(command, [x - h])
            lower_val = self.stack.ret()
            return (upper_val - lower_val) / (2 * h)

        def second_central_difference(command, x, h=1e-6):
            self.execute_command(command, [x + h])
            upper_val = self.stack.ret()
            self.execute_command(command, [x - h])
            lower_val = self.stack.ret()
            self.execute_command(command, [x])
            center_val = self.stack.ret()
            return (upper_val - 2 * center_val + lower_val) / (h ** 2)

        try:
            # assign args and hardcode type requirements

            bfunc_string: str = args[0]
            if not isinstance(bfunc_string, (str)):
                raise TypeError("The 'bfunction_name' argument must be a string")

            x: float = args[1]
            if not isinstance(x, (int, float, np.float64)):
                raise TypeError("The 'lower_bound' argument must be a number")

            if len(args) > 2:
                method_string: str = args[2]
                if not isinstance(method_string, (str)):
                    raise TypeError("The 'method_string' argument must be a string")
            else:
                method_string = "CDIF"

            # differentiate based on chosen method

            match method_string.upper():
                case "CDIF":
                    slope = central_difference(bfunc_string, x, h=1e-6)
                    self.stack_handler.handle_token(slope)
                case "SECOND":
                    slope = second_central_difference(bfunc_string, x, h=1e-6)
                    self.stack_handler.handle_token(slope)
                case _:
                    raise ValueError(f"{method_string} is not a valid differentiation method")

        except Exception as e:
            self.data.log.append(str(e))

    def roots(self, args):
        # define interior differentiation functions
        def bisection(command, a, b, tol=1e-6, maxits=1000):
            # initial check
            self.execute_command(command, [a])
            fa = self.stack.ret()
            self.execute_command(command, [b])
            fb = self.stack.ret()
            # if the initial limits do not bracket a root, raise an error
            if fa * fb > 0:
                raise Exception("Bad interval - 0 or 2+ roots")

            # initialize an interation counter and tolerance checking boolean flag
            tol_check = False
            iteration = 0
            while iteration < maxits:

                # increment iteration
                iteration += 1

                # find midpoint of a and b
                c = (b + a) / 2

                # if not first loop
                if iteration > 1:
                    ea = abs((c - last_c) / c)
                    # if tolerance has been met
                    if (abs(b - a) / 2) < tol or abs(ea) < tol:
                        tol_check = True
                        break

                # calls to the anonymous function to find the value of f(inputs) at these points
                self.execute_command(command, [a])
                fa = self.stack.ret()
                self.execute_command(command, [c])
                fc = self.stack.ret()

                # adjust the boundaries depending on where the zero is (between a negative and a positive f(x) value)
                if fa * fc > 0:
                    a = c
                else:
                    b = c

                last_c = c

            # if no root found within tolerance and maximum number of iterations, raise an error
            if not tol_check:
                raise Exception("Root not found within tolerance and maximum number of iterations")

            return c

        def secant(command, x, tol=1e-6):
            return None

        try:
            # assign args and hardcode type requirements

            bfunc_string: str = args[0]
            if not isinstance(bfunc_string, (str)):
                raise TypeError("The 'bfunction_name' argument must be a string")

            lower_guess: float = args[1]
            if not isinstance(lower_guess, (int, float, np.float64)):
                raise TypeError("The 'lower_bound' argument must be a number")

            upper_guess: float = args[2]
            if not isinstance(upper_guess, (int, float, np.float64)):
                raise TypeError("The 'upper_bound' argument must be a number")

            method_string = "BISECTION"  # hardcoded because secant is not implemented

            # find root based on chosen method

            match method_string.upper():
                case "BISECTION":
                    root = bisection(bfunc_string, lower_guess, upper_guess, tol=1e-6, maxits=1000)
                    self.stack_handler.handle_token(root)
                case "SECANT":
                    root = secant(bfunc_string, 666, tol=1e-6)
                    self.stack_handler.handle_token(root)
                case _:
                    raise ValueError(f"{method_string} is not a valid differentiation method")

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
            self.stack.stack_list.append(self.stack.stack_list[-1])
        except Exception as e:
            self.data.log.append(str(e))

    def up(self, args):
        try:
            self.stack.stack_list.append(self.stack.stack_list[0])
            self.stack.stack_list.pop(0)
        except Exception as e:
            self.data.log.append(str(e))

    def down(self, args):
        try:
            self.stack.stack_list.insert(0, self.stack.stack_list[-1])
            self.stack.stack_list.pop()
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

    def execute_bfunction(self, name, args):
        try:
            bfunction = self.data.find_bfunction(name)
            self.interpreter.interpret_tokens(self.parser.tokenize_bfunction(bfunction, args))
        except Exception as e:
            self.data.log.append(str(e))

    def ret(self, args):
        try:
            val = self.stack.stack_list[-1]
            self.stack.clear()
            self.stack.stack_list.append(val)
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

    def clear_bfunctions(self, args):
        try:
            self.data.clear_bfunctions()
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

    def define_bfunction(self, body, folder):
        try:
            bfunction = BFunction(body)
            self.data.define_bfunction(bfunction, folder)
        except Exception as e:
            self.data.log.append(str(e))

    def teq(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            if value1 == value2:
                self.interpreter.run_state = True
            else:
                self.interpreter.run_state = False
        except Exception as e:
            self.data.log.append(str(e))

    def tne(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            if value1 != value2:
                self.interpreter.run_state = True
            else:
                self.interpreter.run_state = False
        except Exception as e:
            self.data.log.append(str(e))

    def tgt(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            if value1 > value2:
                self.interpreter.run_state = True
            else:
                self.interpreter.run_state = False
        except Exception as e:
            self.data.log.append(str(e))

    def tlt(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            if value1 < value2:
                self.interpreter.run_state = True
            else:
                self.interpreter.run_state = False
        except Exception as e:
            self.data.log.append(str(e))

    def tge(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            if value1 >= value2:
                self.interpreter.run_state = True
            else:
                self.interpreter.run_state = False
        except Exception as e:
            self.data.log.append(str(e))

    def tle(self, args):
        try:
            value1 = args[0]
            value2 = args[1]
            if value1 <= value2:
                self.interpreter.run_state = True
            else:
                self.interpreter.run_state = False
        except Exception as e:
            self.data.log.append(str(e))

    def iota(self, args):
        try:
            value = int(args[0])
            self.stack_handler.handle_token(list(range(value)))
        except Exception as e:
            self.data.log.append(str(e))

    def pack(self, args):
        try:
            array = []
            for item in self.stack.stack_list:
                array.append(item.value)
            self.stack.clear()
            self.stack_handler.handle_token(np.array(array))
        except Exception as e:
            self.data.log.append(str(e))

    def unpack(self, args):
        try:
            array = self.stack.popval()
            for value in array:
                self.stack_handler.handle_token(value)
        except Exception as e:
            self.data.log.append(str(e))

    def eye(self, args):
        try:
            value = int(args[0])
            self.stack_handler.handle_token(np.eye(value))
        except Exception as e:
            self.data.log.append(str(e))

    @staticmethod
    def help(args: list):
        import webbrowser
        webbrowser.open('https://www.kinblandford.com/home/blang', new=2)