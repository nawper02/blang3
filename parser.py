import re
import ast
import numpy as np


class Parser:
    def __init__(self, stack, data):
        self.stack = stack
        self.data = data

    # Method to turn string input into list of usable tokens
    # Doesn't split up things we don't want to split up, like lists strings or args
    @staticmethod
    def tokenize(s: str):
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

    @staticmethod
    def tokenize_macro(s: str):
        tokens = s.split("\n")
        return tokens

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
    def is_cmd(token):
        pattern = re.compile(r"\.[a-zA-Z]+(\(.+\))?", re.IGNORECASE)
        return pattern.match(token)

    @staticmethod
    def is_number(token):
        # if token is an actual float
        if type(token) == float:
            return True
        # if token is a string that can be interpreted as a float
        else:
            try:
                pattern = re.compile(r"^([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?$", re.IGNORECASE)
                return pattern.match(token)
            except TypeError:
                return False

    @staticmethod
    def is_list(token):
        # if token is an actual list
        if type(token) == np.ndarray or type(token) == list:
            return True
        # if token is a string that can be interpreted as a list
        else:
            try:
                pattern = re.compile(r"^\[(.*)\]$", re.IGNORECASE)
                return pattern.match(token)
            except TypeError:
                return False

    @staticmethod
    def is_string(token):
        pattern = re.compile(r"^('.*')$", re.IGNORECASE)
        return re.match(pattern, token) or token == "__STRING__"

    @staticmethod
    def get_string(token):
        pattern = re.compile(r"('.*')", re.IGNORECASE)
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

        # If the token is a var
        elif token in self.data.vars.keys():
            return True

        else:
            return False

    # Gets value of a token or string (if it can be interpreted as a value or string)
    def get_value_or_string(self, token):

        # If the token is a floating point number
        if self.is_number(token):
            # Return token interpreted as a float
            return float(token)

        # If the token is a list
        elif self.is_list(token):
            # Return token interpreted as a python list
            return np.array(ast.literal_eval(token))

        # If the token is a var
        elif token in self.data.vars.keys():
            # Return value associated with token
            return self.data.vars[token]

        elif self.is_string(token):
            return self.get_string(token)

        else:
            return None

    # Gets value of a token (if it can be interpreted as a value)
    def get_value(self, token):

        # If the token is a floating point number
        if self.is_number(token):
            # Return token interpreted as a float
            return float(token)

        # If the token is a list
        elif self.is_list(token):
            # Return token interpreted as a python list
            return np.array(ast.literal_eval(token))

        # If the token is a var
        elif token in self.data.vars.keys():
            # Return value associated with token
            return self.data.vars[token]

        else:
            return None

