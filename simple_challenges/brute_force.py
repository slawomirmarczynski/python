#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Liczbą trzycyfrową będziemy nazywać każdą liczbę naturalną od 100 do 999.
Napisz program który sprawdzi wszystkie liczby trzycyfrowe a i wszystkie liczby
trzycyfrowe b oraz policzy ile jest takich par (a, b) dla których: suma a + b
jest liczbą trzycyfrową, różnica a − b jest też liczbą trzycyfrową, jeżeli suma
cyfr a jest parzysta to suma cyfr b jest nieparzysta i na odwrót... gdy a ma
nieparzystą sumę cyfr to b ma parzystą.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

counter = 0

for a0 in range(9):
    for a1 in range(9):
        for a2 in range(9):
            for b0 in range(9):
                for b1 in range(9):
                    for b2 in range(9):
                        a = 100 * a2 + 10 * a1 + a0
                        b = 100 * b2 + 10 * b1 + b0
                        if (100 <= a <= 999 and 100 <= b <= 999 and
                                100 <= a + b <= 999 and 100 <= a - b <= 999 and
                                ((a % 2 == 0 and b % 2 == 1) or
                                 (a % 2 == 1 and b % 2 == 0))):
                            # print(a, b)
                            counter += 1

print("jest", counter, "takich liczb")
