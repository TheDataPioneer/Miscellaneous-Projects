# 1337 Speak Translator
# Author:  Joshua Paul Barnard
# Date: January 1st, 2024

# Function to replace characters
def replace_chars(input_string, replacements):
    modified_string = ""
    for char in input_string:
        modified_string += replacements.get(char, char)
    return modified_string

# Define the characters to be replaced, with complexity == 1 (basic 1337).
replacements_basic = {'a' : '4',
                'A' : '4',
                'e' : '3',
                'E' : '3',
                'i' : '1',
                'I' : '1',
                'l' : '|',
                'L' : '|',
                'o' : '0',
                'O' : '0'}

# Define the characters to be replaced, with complexity == 2 (intermediate 1337).
replacements_intermediate = {'1' : 'i',
                '2' : 'Z',
                '3' : 'E',
                '4' : 'A',
                '5' : 'S',
                '6' : 'b',
                '7' : 'T',
                '8' : 'B',
                '9' : 'q',
                '0' : 'o'}

# Define the characters to be replaced, with complexity == 3 (advanced 1337).
replacements_advanced = {'1' : 'i',
                '2' : 'Z',
                '3' : 'E',
                '4' : 'A',
                '5' : 'S',
                '6' : 'b',
                '7' : 'T',
                '8' : 'B',
                '9' : 'q',
                '0' : 'o'}

# Define the characters to be replaced, with complexity == 4 (ultra 1337).
replacements_ultra = {'1' : 'i',
                '2' : 'Z',
                '3' : 'E',
                '4' : 'A',
                '5' : 'S',
                '6' : 'b',
                '7' : 'T',
                '8' : 'B',
                '9' : 'q',
                '0' : 'o'}

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










