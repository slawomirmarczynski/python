#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Podstawowe działania matematyczne (w tym obliczanie pierwiastka kwadratowego),
używanie zmiennych i wypisywanie wyników na przykładzie obliczania pola
powierzchni trójkąta którego długości boków są zadane.

Do obliczeń używamy wzoru Herona, patrz
https://pl.wikipedia.org/wiki/Wzór_Herona (10.10.2020).

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

from math import sqrt

a = 4
b = 5
c = 6

p = (a + b + c) / 2
s = sqrt(p * (p - a) * (p - b) * (p - c))

print('długość boku BC =', a)
print('długość boku AC =', b)
print('długość boku AB =', c)

print('pole powierzchni trójkąta ABC =', s)
