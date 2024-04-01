from string import digits

with open('output.txt', 'r', encoding='utf-8') as file:
    java_letter = file.read()
java_letter_or_digit = java_letter + digits
integer_type_suffix = 'lL'
exponent_indicator = 'eE'
sign = '+-'
float_type_suffix = 'fFdD'