#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przykład - pętla for na różne sposoby.

CC-BY-NC-ND 2020 Sławomir Marczyński
"""

# Generowanie tabeli pseudolosowych liczb z zakresu od 0 do 9. W każdym wierszu
# ma być 10 liczb, wierszy ma też być 10. Uwaga: parametr end=' ' powoduje że
# print nie wypisuje końca wiersza, ale znak odstępu.

from random import randint

for i in range(10):
    for j in range(10):
        print(randint(0, 9), end=' ')
    print()


# Modyfikowanie "zmiennej kontrolnej" w pętli for nie zmienia liczby iteracji:
# choć i będzie większe niż 100, to i tak w następnej iteracji zostanie "zresetowane".
# Czyli instrukcje w pętli wykonają się 20 razy.

for i in range(10, 105, 5):  # liczby 10, 15, 20, ..., 100
    print(i, end=' ')
    i = 200
    print(i)


# Pętla for z break, continue oraz else

N = 50
for k in range(1, N):
    if k < 10:
        print('continue -> od razu wejście w kolejny cykl')
        continue
    if k > 100:
        print('break -> "awaryjne" wyjście z pętli')
        break
    print(k)
else:
    print('Normalne zakończenie pętli (nie było break)')
