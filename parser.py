import re
import ast
import numpy as np
from bfunction import BFunction


class Parser:
    def __init__(self, stack, data):
        self.stack = stack
        self.data = data



    # Method to turn string input into list of usable tokens
    # Doesn't split up things we don't want to split up, like lists strings or args
    @staticmethod
    def tokenize(s: str): # , bfunction=None, inputs=None
        # if the entire string is just an empty string, return it so commandhandler can catch it and call dup
        if s == "":
            return [s]
        # Find all substrings between round brackets (function arguments) to hide them from the split
        arg_matches = re.findall(r'\(.*?\)', s)
        for match in arg_matches:
            # Replace the substring with a special character
            s = s.replace(match, "__ARGS__")

        # Find all substrings between square brackets (lists) to hide them from the split
        list_matches = re.findall(r'\[.*?\]', s)
        for match in list_matches:
            # Replace the substring with a special character
            s = s.replace(match, "__LIST__")

        # Find all substrings between single quotes (strings) to hide them from the split
        string_matches = re.findall(r'\'.*?\'', s)
        for match in string_matches:
            # Replace the substring with a special character
            s = s.replace(match, "__STRING__")

        # Split the string on spaces
        tokens = s.split(" ")

        # Replace the special character with the original substring
        for i in range(len(tokens)):

            if "__ARGS__" in tokens[i]:
                tokens[i] = tokens[i].replace("__ARGS__", arg_matches.pop(0))

            if "__LIST__" in tokens[i]:
                tokens[i] = tokens[i].replace("__LIST__", list_matches.pop(0))

            if "__STRING__" in tokens[i]:
                tokens[i] = tokens[i].replace("__STRING__", string_matches.pop(0))

        # Remove empty tokens created by extra spaces
        tokens = list(filter(lambda x: x.strip(), tokens))
        return tokens

    # the main job of this method is to replace variables with values
    def tokenize_bfunction(self, f: BFunction, inputs: list):
        # turn everything in inputs into a string representation of the object
        # if it's a list, turn it into a string representation of a list
        # if it's a string, wrap it in quotes
        # if it's a number, leave it as is
        for index, inp in enumerate(inputs):
            if type(inp) == str:
                inputs[index] = f"'{inp}'"
            elif type(inp) in (list, np.ndarray):
                inputs[index] = "[" + ",".join([str(item) for item in inp]) + "]"
            else:
                inputs[index] = str(inp)

        # map f.args to inputs (element wise) and raise an error if there is a different number of args and inputs
        variables_dict = dict(zip(f.args, inputs))

        tokens = []
        for line in f.pgrm_lines:
            tokens += self.tokenize(line)

        # Replace tokens with inputs
        for index, token in enumerate(tokens):  # For each token
            if token in f.args:  # If token is an arg
                tokens[index] = variables_dict[token]  # Replace token with inp
            elif self.is_cmd(token):  # If token is a command
                tokens[index] = self.replace_variables_in_block(token, variables_dict, left_char="(", right_char=")") # Replace variables in parentheses with inputs

            elif self.is_list(token): # If token is a list
                tokens[index] = self.replace_variables_in_block(token, variables_dict, left_char="[", right_char="]")

        return tokens

    @staticmethod
    def replace_variables_in_block(string, variables, left_char="(", right_char=")"):
        start = 0
        result = ""
        while True:
            open_paren = string.find(left_char, start)
            if open_paren == -1:
                result += string[start:]
                break
            result += string[start:open_paren + 1]
            close_paren = string.find(right_char, open_paren)
            if close_paren == -1:
                break
            inside_paren = string[open_paren + 1:close_paren]
            for var, val in variables.items():
                inside_paren = inside_paren.replace(var, val)
            result += inside_paren + right_char
            start = close_paren + 1
        return result

    @staticmethod
    def find_outermost_block(s: str, left_char: str, right_char: str):
        # Function that takes a string and finds the outermost block specified by the left and right characters
        # I wrote this method because re.findall doesn't work with nested brackets
        left_index = None
        right_index = None
        # Loop from left to right until we find the first left character
        for index, char in enumerate(s):
            if char == left_char:
                left_index = index
                break
        # Loop from right to left until we find the first right character
        for index, char in enumerate(s[::-1]):
            if char == right_char:
                right_index = index
                break
        # If we found both characters, return the substring between them
        if left_index is not None and right_index is not None:
            return s[left_index: len(s) - right_index]
        else:
            return None

    @staticmethod
    def is_cmd(token): #CHANGETAG
        pattern = re.compile(r"[tTfF]?\.[a-zA-Z]+(\(.+\))?", re.IGNORECASE)
        return pattern.match(token)

    @staticmethod
    def is_number(token):
        # if token is an actual float
        if type(token) in (float, int, np.float64):
            return True
        # if token is a string that can be interpreted as a float
        else:
            try:
                pattern = re.compile(r"^[tTfF]?([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?$", re.IGNORECASE)
                return pattern.match(token)
            except TypeError:
                return False

    @staticmethod
    def is_list(token, check_value=True, check_string=True):
        if check_string:
            try:
                pattern = re.compile(r"^[tTfF]?\[(.*)\]$", re.IGNORECASE)
                return pattern.match(token)
            except TypeError:
                return False
        if check_value:
            if type(token) in (list, np.ndarray):
                return True
            else:
                return False

    def is_string(self, token):
        if not self.is_number(token) and not self.is_list(token):
            pattern = re.compile(r"[tTfF]?('.*')", re.IGNORECASE)
            return re.match(pattern, token) or token == "__STRING__"
        else:
            return False

    @staticmethod
    def get_string(token):
        pattern = re.compile(r"[tTfF]?('.*')", re.IGNORECASE)
        match = re.match(pattern, token)
        if match:
            # This is a string token
            string = match.group(1)
            # Remove the surrounding quotes
            return string[1:-1]
        else:
            return None

    # Checks if a token can be interpreted as a value
    def is_value(self, token):

        # If the token is a floating point number
        if self.is_number(token):
            return True

        # If the token is a list
        elif self.is_list(token):
            return True

        # If the token is a string
        #elif self.is_string(token):
        #    return True

        # If the token is a var
        elif token in self.data.vars.keys():
            return True

        else:
            return False

    # Gets value of a token or string (if it can be interpreted as a value or string)
    def get_value(self, token, allow_string_value=False):

        # if the token starts with a t or f, remove it
        token = self.strip_prefix(token)

        # If the token is a floating point number
        if self.is_number(token):
            # Return token interpreted as a float
            return float(token)

        # If the token is a list in string form
        elif self.is_list(token, check_value=False):
            # Return token interpreted as a python list
            return np.array(ast.literal_eval(token))

        # This is a hack to get around malformed node or string in ast.literal_eval
        # If token is actually a list already
        elif self.is_list(token, check_string=False):
            # Return the token without changing it
            return token

        # If the token is a var
        elif token in self.data.vars.keys():
            # Return value associated with token
            return self.data.vars[token]

        elif self.is_string(token) and allow_string_value:
            return self.get_string(token)

        else:
            return None

    @staticmethod
    def strip_prefix(token):
        if type(token) is not str:
            return token
        if token[0] in "tTfF":
            return token[1:]
        else:
            return token

