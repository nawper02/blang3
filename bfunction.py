"""
Example function:

.testfunc('x' 'y')      # initializes function name and arguments
.teq(x y)               # checks if x and y are equal
+ x y .add              # if teq returns 1, do this
- x y .sub              # if teq returns 0, do this
~ x y .div              # do this until teq is 1?
.return                  # return whatever is in the stack

# When called, should replace all x and y with their value
# Should execute line by line and have a conditional state (changed by teq tlt etc) -- should only execute lines
# with + if state is 1, and - if state is 0
# Should be able to get a return value internally (like in my python functions)

"""
import re
from parser import Parser


# Temporarily, BFunction does some of the work that the parser should do
class BFunction:
    def __init__(self, body: str, parser: Parser):
        # Split text body (from macrw) into lines
        self.lines = body.split('\n')
        # Get the first line (the header)
        self.head = self.lines[0]
        # Get the name and args from the header
        self.name, self.args = self.get_name_and_args()
        # Get the rest of the lines (the program)
        self.pgrm_lines = self.lines[1:]
        self.parser = parser

    def get_name_and_args(self):
        # Extract name and args from token
        match = re.match(r'\.(\w+)(\(.*\))?', self.head)

        # Index out the groups (command and args)
        name = match.group(1)  # COMMAND
        if match.group(2) is None:
            args_string = ""  # EMPTY ARGS
        else:
            args_string = match.group(2).strip("( )")  # ARGS

        # Split args into list
        args = args_string.split(" ")
        return name, args

    def tokenize_from_inputs(self, inputs: list):
        tokens = self.parser.tokenize_bfunction(self.pgrm_lines)

        return tokens
