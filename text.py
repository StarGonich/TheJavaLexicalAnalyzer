# Драйвер исходного текста
import glob
import sys
import loc
import error
from string import hexdigits

chEOT = '\0'
chEOL = '\n'
chSPACE = ' '
chHT = '\t'
chFF = '\f'


src = ""
i = 0
ch = ""


def reset():
    global src
    if len(sys.argv) < 2:
        error.Error("Запуск: python Java.py <файл программы>")
    else:
        try:
            file_list = glob.glob(sys.argv[1])
        except:
            error.Error("Ошибка открытия файла")
        try:
            for file_name in file_list:
                with open(file_name, 'r') as file:
                    src += file.read()
                    file.close()
        except:
            error.Error("Ошибка чтения файла")


def unicode_escape():
    global ch
    next_ch()
    unicode = ''
    while ch == 'u':
        next_ch()
    for _ in range(3):
        if ch in hexdigits:
            unicode += ch
            next_ch()
        else:
            error.lexError('Unicode дописан не до конца')
    if ch in hexdigits:
        unicode += ch
    else:
        error.lexError('Unicode дописан не до конца')
    # print('Unicode =', unicode)
    return chr(int(unicode, 16))


def next_ch():
    global src, i, ch
    if i < len(src):
        ch = src[i]
        loc.pos += 1
        i += 1
        if ch == '\\':
            next_ch()
            if ch == 'u':
                ch = unicode_escape()
            else:
                ch = '\\'
                loc.pos -= 1
                i -= 1
        if ch in '\n\r':
            ch = chEOL
            loc.pos = 0
    else:
        ch = chEOT
