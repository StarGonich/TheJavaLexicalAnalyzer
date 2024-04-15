# Лексический анализатор

from enum import Enum
from string import octdigits, hexdigits

import error
from text import next_ch
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
    INTEGERNUMBER, FLOATINGNUMBER, DOUBLENUMBER, TRUE, FALSE, CHARACTER, STRING, NULL, \
    \
    LPAR, RPAR, BEGIN, END, LSQ, RSQ, SEMI, COMMA, DOT, \
    \
    EQ, EQEQ, PLUS, PLUSEQ, GT, LE, MINUS, MINUSEQ, LT, GE, MULT, MULTEQ, NOT, NOTEQ, DIV, DIVEQ, \
    TILDE, AND, BITAND, ANDEQ, TERN, OR, BITOR, OREQ, COLON, INC, CARET, CARETEQ, DEC, MOD, MODEQ, \
    LTLT, LTLE, GTGT, GTGE, GTGTGT, GTGTGE = range(103)  # !!! float double literal, true false


lex_names = []
for enum_lex in Lex:
    lex_names.append(enum_lex.name)
lex_dict = dict(zip(lex_names, [0] * len(Lex)))
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

    'true': Lex.TRUE,
    'false': Lex.FALSE,
    'null': Lex.NULL
}


def signed_integer():
    if text.ch in sign:
        next_ch()
    if text.ch in digits:
        next_ch()
        while text.ch in digits:
            next_ch()
    else:
        error.lexError('Ожидается десятичное число')


def traditional_comment():
    next_ch()
    while True:
        if text.ch == '*':
            next_ch()
            if text.ch == '/':
                next_ch()
                break
        elif text.ch == text.chEOT:
            error.lexError('Не закончен комментарий')
        else:
            next_ch()


def end_of_the_line_comment():
    next_ch()
    while text.ch not in {text.chEOL, text.chEOT}:
        next_ch()


def octal_escape():
    first_ch = text.ch
    next_ch()
    if text.ch in octdigits:
        next_ch()
        if text.ch in octdigits:
            if first_ch in '0123':
                next_ch()
            else:
                error.lexError('Первая цифра после \\ должна быть от 0 до 3')


def escape_sequence():
    next_ch()
    if text.ch in 'btnfr\"\'\\':
        next_ch()
    elif text.ch in octdigits:
        octal_escape()
    else:
        error.lexError('Недопустимый символ после \\')


def next_lex():
    global name
    while text.ch in {text.chSPACE, text.chHT, text.chEOL, text.chFF}:
        next_ch()
    match text.ch:

        # Идентификаторы
        case _ if text.ch in java_letter:
            name = text.ch
            next_ch()
            while text.ch in java_letter_or_digit:
                name += text.ch
                next_ch()
            return keywords.get(name, Lex.NAME)

        # Литералы
        case _ if text.ch in digits:
            if text.ch == '0':
                next_ch()
                if text.ch in 'xX':
                    next_ch()
                    if text.ch in hexdigits:
                        next_ch()
                    else:
                        error.lexError('Ожидается шестнадцатеричная цифра')
                    while text.ch in hexdigits:
                        next_ch()
                elif text.ch in octdigits:
                    next_ch()
                    while text.ch in octdigits:
                        next_ch()
                    if text.ch in '89':
                        next_ch()
                        while text.ch in digits:
                            next_ch()
                        if text.ch not in '.eEfFdD':
                            error.lexError('Ожидается \'.\', экспонента или суффикс типа')
            while text.ch in digits:
                next_ch()
            if text.ch == '.':
                next_ch()
                while text.ch in digits:
                    next_ch()
                if text.ch in exponent_indicator:
                    next_ch()
                    signed_integer()
                if text.ch in float_type_suffix:
                    if text.ch in 'fF':
                        next_ch()
                        return Lex.FLOATINGNUMBER
                    else:
                        next_ch()
                return Lex.DOUBLENUMBER
            elif text.ch in exponent_indicator:
                next_ch()
                signed_integer()
                if text.ch in float_type_suffix:
                    if text.ch in 'fF':
                        next_ch()
                        return Lex.FLOATINGNUMBER
                    else:
                        next_ch()
                return Lex.DOUBLENUMBER
            elif text.ch in float_type_suffix:
                if text.ch in 'fF':
                    next_ch()
                    return Lex.FLOATINGNUMBER
                else:
                    next_ch()
                return Lex.DOUBLENUMBER
            else:
                if text.ch in integer_type_suffix:
                    next_ch()
                return Lex.INTEGERNUMBER
        case '"':  # StringLiteral
            next_ch()
            while True:
                if text.ch == '"':
                    next_ch()
                    return Lex.STRING
                elif text.ch == '\\':
                    escape_sequence()
                elif text.ch == text.chEOT:
                    error.lexError('Не закончена строка')
                else:
                    next_ch()
        case "'":  # CharacterLiteral
            next_ch()
            if text.ch == '\\':
                escape_sequence()
            else:
                next_ch()
            if text.ch == "'":
                next_ch()
                return Lex.CHARACTER
            else:
                error.lexError('В \'\' кавычках должен быть ЕДИНСТВЕННЫЙ символ')

        # Разделители
        case '(':
            next_ch()
            return Lex.LPAR
        case ')':
            next_ch()
            return Lex.RPAR
        case '{':
            next_ch()
            return Lex.BEGIN
        case '}':
            next_ch()
            return Lex.END
        case '[':
            next_ch()
            return Lex.LSQ
        case ']':
            next_ch()
            return Lex.RSQ
        case ';':
            next_ch()
            return Lex.SEMI
        case ',':
            next_ch()
            return Lex.COMMA
        case '.':
            next_ch()
            if text.ch in digits:  # Digits
                next_ch()
                while text.ch in digits:
                    next_ch()
                if text.ch in exponent_indicator:  # ExponentPart
                    next_ch()
                    signed_integer()
                if text.ch in float_type_suffix:
                    if text.ch in 'fF':
                        next_ch()
                        return Lex.FLOATINGNUMBER
                    else:
                        next_ch()
                return Lex.DOUBLENUMBER
            else:
                return Lex.DOT

        # Операции
        case '=':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.EQEQ
            else:
                return Lex.EQ
        case '+':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.PLUSEQ
            elif text.ch == '+':
                next_ch()
                return Lex.INC
            else:
                return Lex.PLUS
        case '>':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.GE
            elif text.ch == '>':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    return Lex.GTGE
                elif text.ch == '>':
                    next_ch()
                    if text.ch == '=':
                        next_ch()
                        return Lex.GTGTGE
                    else:
                        return Lex.GTGTGT
                else:
                    return Lex.GTGT
            else:
                return Lex.GT
        case '<':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.LE
            elif text.ch == '<':
                next_ch()
                if text.ch == '=':
                    next_ch()
                    return Lex.LTLE
                else:
                    return Lex.LTLT
            else:
                return Lex.LT
        case '-':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MINUSEQ
            elif text.ch == '-':
                next_ch()
                return Lex.DEC
            else:
                return Lex.MINUS
        case '*':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MULTEQ
            else:
                return Lex.MULT
        case '!':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.NOTEQ
            else:
                return Lex.NOT
        case '/':
            next_ch()
            if text.ch == '=':
                next_ch()
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
            next_ch()
            return Lex.TILDE
        case '&':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.ANDEQ
            elif text.ch == '&':
                next_ch()
                return Lex.AND
            else:
                return Lex.BITAND
        case '?':
            next_ch()
            return Lex.TERN
        case '|':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.OREQ
            elif text.ch == '|':
                next_ch()
                return Lex.OR
            else:
                return Lex.BITOR
        case ':':
            next_ch()
            return Lex.COLON
        case '^':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.CARETEQ
            else:
                return Lex.CARET
        case '%':
            next_ch()
            if text.ch == '=':
                next_ch()
                return Lex.MODEQ
            else:
                return Lex.MOD
        case text.chEOT:
            return Lex.EOT
        case _:
            error.lexError("Недопустимый символ")
