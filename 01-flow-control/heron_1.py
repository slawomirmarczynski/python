#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Obliczanie pola powierzchni trójkąta którego długości boków są znane.

Do obliczenia pola powierzchni trójkąta gdy znane są długości boków używamy
wzoru Herona, patrz https://pl.wikipedia.org/wiki/Wzór_Herona (10.10.2020).

CC-BY-NC-ND 2020 Sławomir Marczyński
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
