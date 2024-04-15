#Синтаксический анализатор

import text
import scan


def testText():
    text.next_ch()
    while text.ch != text.chEOT:
        text.next_ch()


def Compile():
    text.next_ch()
    lex = scan.next_lex()
    n = 0
    while lex != scan.Lex.EOT:
        n += 1
        scan.lex_dict[lex.name] += 1
        lex = scan.next_lex()
        # print(n, lex)
    print("\nЧисло лексем:", n)
    for key in scan.lex_dict:
        if scan.lex_dict[key] != 0:
            print("{:20}{:6}{:8.2f}".format(key, scan.lex_dict[key], scan.lex_dict[key] * 100 / n) + '%')
