# Лексический анализатор

from enum import Enum
from string import octdigits, hexdigits

import error
import text
from sets import *
# text.chEOT = '\0' # Он нормально не импортируется


class Lex(Enum):
    NAME, EOT, \
    \
    ABSTRACT, BOOLEAN, BREAK, BYTE, CASE, CATCH, CHAR, CLASS, CONST, CONTINUE, DEFAULT, DO, DOUBLE, ELSE, EXTENDS, \
    FINAL, FINALLY, FLOAT, FOR, GOTO, IF, IMPLEMENTS, IMPORT, INSTANCEOF, INT, INTERFACE, LONG, NATIVE, NEW, PACKAGE, \
    PRIVATE, PROTECTED, PUBLIC, RETURN, SHORT, STATIC, SUPER, SWITCH, SYNCHRONIZED, THIS, THROW, THROWS, TRANSIENT, \
    TRY, VOID, VOLATILE, WHILE, \
    \
    INTEGERNUMBER, FLOATINGPOINTNUMBER, LOGICAL, CHARACTER, STRING, NULL, \
    \
    LPAR, RPAR, BEGIN, END, LSQ, RSQ, SEMI, COMMA, DOT, \
    \
    EQ, EQEQ, PLUS, PLUSEQ, GT, LE, MINUS, MINUSEQ, LT, GE, MULT, MULTEQ, NOT, NOTEQ, DIV, DIVEQ, \
    TILDE, AND, BITAND, ANDEQ, TERN, OR, BITOR, OREQ, COLON, INC, CARET, CARETEQ, DEC, MOD, MODEQ, \
    LTLT, LTLE, GTGT, GTGE, GTGTGT, GTGTGE = range(101)


zeroes = [0] * 101
lex_names = []
for enum_lex in Lex:
    lex_names.append(enum_lex.name)
lex_dict = dict(zip(lex_names, zeroes))
# print(lex_dict)
name = ''

keywords = {
    'abstract': Lex.ABSTRACT,
    'boolean': Lex.BOOLEAN,
    'break': Lex.BREAK,
    'byte': Lex.BYTE,
    'case': Lex.CASE,
    'catch': Lex.CATCH,
    'char': Lex.CHAR,
    'class': Lex.CLASS,
    'const': Lex.CONST,
    'continue': Lex.CONTINUE,
    'default': Lex.DEFAULT,
    'do': Lex.DO,
    'double': Lex.DOUBLE,
    'else': Lex.ELSE,
    'extends': Lex.EXTENDS,
    'final': Lex.FINAL,
    'finally': Lex.FINALLY,
    'float': Lex.FLOAT,
    'for': Lex.FOR,
    'goto': Lex.GOTO,
    'if': Lex.IF,
    'implements': Lex.IMPLEMENTS,
    'import': Lex.IMPORT,
    'instanceof': Lex.INSTANCEOF,
    'int': Lex.INT,
    'interface': Lex.INTERFACE,
    'long': Lex.LONG,
    'native': Lex.NATIVE,
    'new': Lex.NEW,
    'package': Lex.PACKAGE,
    'private': Lex.PRIVATE,
    'protected': Lex.PROTECTED,
    'public': Lex.PUBLIC,
    'return': Lex.RETURN,
    'short': Lex.SHORT,
    'static': Lex.STATIC,
    'super': Lex.SUPER,
    'switch': Lex.SWITCH,
    'synchronized': Lex.SYNCHRONIZED,
    'this': Lex.THIS,
    'throw': Lex.THROW,
    'throws': Lex.THROWS,
    'transient': Lex.TRANSIENT,
    'try': Lex.TRY,
    'void': Lex.VOID,
    'volatile': Lex.VOLATILE,
    'while': Lex.WHILE,

    'true': Lex.LOGICAL,
    'false': Lex.LOGICAL,
    'null': Lex.NULL
}


def signed_integer():
    text.nextCh()
    if text.ch in sign:
        text.nextCh()
    if text.ch in digits:
        text.nextCh()
        while text.ch in digits:
            text.nextCh()
    else:
        error.expect('число')


def traditional_comment():
    text.nextCh()
    while True:
        if text.ch == '*':
            text.nextCh()
            if text.ch == '/':
                text.nextCh()
                break
        elif text.ch == text.chEOT:
            error.lexError('Не закончен комментарий')
        else:
            text.nextCh()


def end_of_the_line_comment():
    text.nextCh()
    while text.ch != text.chEOL:
        text.nextCh()


def octal_escape():
    first_ch = text.ch
    text.nextCh()
    if text.ch in octdigits:
        text.nextCh()
        if text.ch in octdigits:
            if first_ch in '0123':
                text.nextCh()
            else:
                error.lexError('Первая цифра после \\ должна быть от 0 до 3')


def escape_sequence():
    text.nextCh()
    print('first ch in escape =', text.ch)
    if text.ch in 'btnfr\"\'\\':
        text.nextCh()
    elif text.ch in octdigits:
        octal_escape()
    else:
        error.lexError('Недопустимый символ после \\')


def next_lex():
    global name
    while text.ch in {text.chSPACE, text.chHT, text.chEOL, text.chFF}:
        text.nextCh()
    match text.ch:
        # Идентификаторы
        case _ if text.ch in java_letter:
            name = text.ch
            text.nextCh()
            while text.ch in java_letter_or_digit:
                name += text.ch
                text.nextCh()
            print('name =', name)
            print(keywords.get(name, Lex.NAME))
            return keywords.get(name, Lex.NAME)

        # Литералы
        case _ if text.ch in digits:
            if text.ch == '0':
                text.nextCh()
                if text.ch in 'xX':
                    text.nextCh()
                    if text.ch in hexdigits:
                        text.nextCh()
                    else:
                        error.expect('Шестнадцатеричная цифра')
                    while text.ch in hexdigits:
                        text.nextCh()
                elif text.ch in octdigits:
                    text.nextCh()
                    while text.ch in octdigits:
                        text.nextCh()
                if text.ch in '89':
                    text.nextCh()
                    while text.ch in '89':
                        text.nextCh()
                    if text.ch != '.':
                        error.expect('Восьмеричная цифра')
            while text.ch in digits:
                text.nextCh()
            if text.ch == '.':
                text.nextCh()
                while text.ch in digits:
                    text.nextCh()
                if text.ch in exponent_indicator:
                    signed_integer()
                if text.ch in float_type_suffix:
                    text.nextCh()
                return Lex.FLOATINGPOINTNUMBER
            elif text.ch in exponent_indicator:
                signed_integer()
                if text.ch in float_type_suffix:
                    text.nextCh()
                return Lex.FLOATINGPOINTNUMBER
            elif text.ch in float_type_suffix:
                text.nextCh()
                return Lex.FLOATINGPOINTNUMBER
            else:
                if text.ch in integer_type_suffix:
                    text.nextCh()
                return Lex.INTEGERNUMBER
        case '"':  # StringLiteral
            text.nextCh()
            while True:
                if text.ch == '"':
                    text.nextCh()
                    return Lex.STRING
                elif text.ch == '\\':
                    escape_sequence()
                elif text.ch == text.chEOT:
                    error.lexError('Не закончена строка')
                else:
                    text.nextCh()
        case "'":  # CharacterLiteral
            text.nextCh()
            if text.ch == '\\':
                escape_sequence()
            else:
                text.nextCh()
            if text.ch == "'":
                text.nextCh()
                return Lex.CHARACTER
            else:
                error.lexError('В \'\' кавычках должен быть ЕДИНСТВЕННЫЙ символ')

        # Разделители
        case '(':
            text.nextCh()
            return Lex.LPAR
        case ')':
            text.nextCh()
            return Lex.RPAR
        case '{':
            text.nextCh()
            return Lex.BEGIN
        case '}':
            text.nextCh()
            return Lex.END
        case '[':
            text.nextCh()
            return Lex.LSQ
        case ']':
            text.nextCh()
            return Lex.RSQ
        case ';':
            text.nextCh()
            return Lex.SEMI
        case ',':
            text.nextCh()
            return Lex.COMMA
        case '.':
            text.nextCh()
            if text.ch in digits:  # Digits
                text.nextCh()
                while text.ch in digits:
                    text.nextCh()
                if text.ch in exponent_indicator:  # ExponentPart
                    signed_integer()
                if text.ch in float_type_suffix:
                    text.nextCh()
                return Lex.FLOATINGPOINTNUMBER
            else:
                return Lex.DOT

        # Операции
        case '=':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.EQEQ
            else:
                return Lex.EQ
        case '+':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.PLUSEQ
            elif text.ch == '+':
                text.nextCh()
                return Lex.INC
            else:
                return Lex.PLUS
        case '>':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.GE
            elif text.ch == '>':
                text.nextCh()
                if text.ch == '=':
                    text.nextCh()
                    return Lex.GTGE
                elif text.ch == '>':
                    text.nextCh()
                    if text.ch == '=':
                        text.nextCh()
                        return Lex.GTGTGE
                    else:
                        return Lex.GTGTGT
                else:
                    return Lex.GTGT
            else:
                return Lex.GT
        case '<':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.LE
            elif text.ch == '<':
                text.nextCh()
                if text.ch == '=':
                    text.nextCh()
                    return Lex.LTLE
                else:
                    return Lex.LTLT
            else:
                return Lex.LT
        case '-':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.MINUSEQ
            elif text.ch == '-':
                text.nextCh()
                return Lex.DEC
            else:
                return Lex.MINUS
        case '*':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.MULTEQ
            else:
                return Lex.MULT
        case '!':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.NOTEQ
            else:
                return Lex.NOT
        case '/':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.DIVEQ
            elif text.ch == '/':
                end_of_the_line_comment()  # EndOfTheLineComment
                return next_lex()
            elif text.ch == '*':
                traditional_comment()  # TraditionalComment
                return next_lex()
            else:
                return Lex.DIV
        case '~':
            text.nextCh()
            return Lex.TILDE
        case '&':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.ANDEQ
            elif text.ch == '&':
                text.nextCh()
                return Lex.AND
            else:
                return Lex.BITAND
        case '?':
            text.nextCh()
            return Lex.TERN
        case '|':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.OREQ
            elif text.ch == '|':
                text.nextCh()
                return Lex.OR
            else:
                return Lex.BITOR
        case ':':
            text.nextCh()
            return Lex.COLON
        case '^':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.CARETEQ
            else:
                return Lex.CARET
        case '%':
            text.nextCh()
            if text.ch == '=':
                text.nextCh()
                return Lex.MODEQ
            else:
                return Lex.MOD
        case text.chEOT:
            return Lex.EOT
        case _:
            error.lexError("Недопустимый символ")
