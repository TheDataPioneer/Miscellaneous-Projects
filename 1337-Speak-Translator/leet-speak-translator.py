# 1337 Speak Translator
# Author:  Joshua Paul Barnard
# Date: January 29th, 2024

# This is my 1337 speak translator.  There are many like it, but this one is mine.
# There are many different ways to use 1337 speak, and some letters can have tens of variations.
# I created this translator to be able to quickly convert text into my style of 1337.


# Function to replace characters
def replace_chars(input_string, replacements):
    modified_string = ""
    for char in input_string:
        modified_string += replacements.get(char, char)
    return modified_string

# Define the characters to be replaced, with complexity == 1 (basic 1337).
replacements_basic = {
    'a' : '4',
    'A' : '4',
    'e' : '3',
    'E' : '3',
    'i' : '1',
    'I' : '1',
    'l' : '|',
    'L' : '|',
    'o' : '0',
    'O' : '0'
}

# Define the characters to be replaced, with complexity == 2 (intermediate 1337).
replacements_intermediate = {
    '1' : 'i',
    '2' : 'Z',
    '3' : 'E',
    '4' : 'A',
    '5' : 'S',
    '6' : 'b',
    '7' : 'T',
    '8' : 'B',
    '9' : 'q',
    '0' : 'o',
    'a': '/-\\',
    'A': '/-\\',
    'b': '8',
    'B': '8',
    'c': '(',
    'C': '(',
    'd': '[)',
    'D': '[)',
    'e': '3',
    'E': '3',
    'f': '|=',
    'F': '|=',
    'g': '6',
    'G': '6',
    'h': '|-|',
    'H': '|-|',
    'i': '1',
    'I': '1',
    'j': '_|',
    'J': '_|',
    'k': '|<',
    'K': '|<',
    'l': '|_',
    'L': '|_',
    'm': '/\\/\\',
    'M': '/\\/\\',
    'n': '/\\/',
    'N': '/\\/',
    'o': '0',
    'O': '0',
    'p': '|>',
    'P': '|>',
    'q': '(,)',
    'Q': '(,)',
    'r': '|2',
    'R': '|2',
    's': '5',
    'S': '5',
    't': '7',
    'T': '7',
    'u': '|_|',
    'U': '|_|',
    'v': '\\/',
    'V': '\\/',
    'w': '\\/\\/',
    'W': '\\/\\/',
    'x': '><',
    'X': '><',
    'y': '`/',
    'Y': '`/',
    'z': '-/_',
    'Z': '-/_'
}

# Define the characters to be replaced, with complexity == 3 (advanced 1337).
replacements_advanced = {
    '1' : 'i',
    '2' : 'Z',
    '3' : 'E',
    '4' : 'A',
    '5' : 'S',
    '6' : 'b',
    '7' : 'T',
    '8' : 'B',
    '9' : 'q',
    '0' : 'o',
    'a': '@',
    'A': '/-\\',
    'b': '6',
    'B': '|3',
    'c': '©',
    'C': '¢',
    'd': 'ꞇ|',
    'D': '[)',
    'e': 'ë',
    'E': '[-',
    'f': 'ƒ',
    'F': '|=',
    'g': '9',
    'G': '(_+',
    'h': 'ר|',
    'H': ']-[',
    'i': '1',
    'I': '][',
    'j': '_|',
    'J': '_]',
    'k': '|<',
    'K': '|{',
    'l': '|',
    'L': '|_',
    'm': '^^',
    'M': '|\\/|',
    'n': '^/',
    'N': '|\\|',
    'o': '0',
    'O': '()',
    'p': '|*',
    'P': '|°',
    'q': '9',
    'Q': '(_,)',
    'r': '®',
    'R': '®',
    's': '$',
    'S': '5',
    't': '-|-',
    'T': '7',
    'u': '(_)',
    'U': '|_|',
    'v': '|/',
    'V': '\/',
    'w': '\\^/',
    'W': '\\/\\/',
    'x': '><',
    'X': '}{',
    'y': '`/',
    'Y': '\|/',
    'z': '%',
    'Z': '%'
}

# Define the characters to be replaced, with complexity == 4 (ultra 1337).
replacements_ultra = {
    '1' : 'i',
    '2' : 'Z',
    '3' : 'E',
    '4' : 'A',
    '5' : 'S',
    '6' : 'b',
    '7' : 'T',
    '8' : 'B',
    '9' : 'q',
    '0' : 'o',
    'a': '',
    'A': '',
    'b': '',
    'B': '',
    'c': '',
    'C': '',
    'd': '',
    'D': '',
    'e': '',
    'E': '',
    'f': '',
    'F': '',
    'g': '',
    'G': '',
    'h': '',
    'H': '',
    'i': '',
    'I': '',
    'j': '',
    'J': '',
    'k': '',
    'K': '',
    'l': '',
    'L': '',
    'm': '',
    'M': '',
    'n': '',
    'N': '',
    'o': '',
    'O': '',
    'p': '',
    'P': '',
    'q': '',
    'Q': '',
    'r': '',
    'R': '',
    's': '',
    'S': '',
    't': '',
    'T': '',
    'u': '',
    'U': '',
    'v': '',
    'V': '',
    'w': '',
    'W': '',
    'x': '',
    'X': '',
    'y': '',
    'Y': '',
    'z': '',
    'Z': ''
}


# Request input for the degree of complexity of 1337 speak.
complexity_level = input("Enter the level of complexity (1 is basic, 2 is intermediate, 3 is advanced, and 4 is ultra): ")

# Check if the user inputted a valid number for complexity level.
if complexity_level.isdigit():
    # Convert the input to an integer.
    number = int(complexity_level)
    # Check if the input is within the valid range.
    if number in [1, 2, 3, 4]:
        print(" ")
    else:
        print("Input is not within the valid range.")
else:
    print("Input is not a valid number.")


# Request input for the english words to be converted.
original_input = input("Enter your English to be translated to 1337: ")

# Perform replacement based on the chosen dictionary.
if complexity_level == '1':
    leet_speak = replace_chars(original_input, replacements_basic)
    print(leet_speak)
elif complexity_level == '2':
    leet_speak = replace_chars(original_input, replacements_intermediate)
    print(leet_speak)
elif complexity_level == '3':
    leet_speak = replace_chars(original_input, replacements_advanced)
    print(leet_speak)
elif complexity_level == '4':
    leet_speak = replace_chars(original_input, replacements_ultra)
    print(leet_speak)
else:
    print("Error:  Could not modify original input.")










