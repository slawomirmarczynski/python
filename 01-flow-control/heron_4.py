#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Obliczanie pola powierzchni trójkąta którego długości boków są znane.

Do obliczenia pola powierzchni trójkąta gdy znane są długości boków używamy
wzoru Herona, patrz https://pl.wikipedia.org/wiki/Wzór_Herona (10.10.2020).

CC-BY-NC-ND 2020 Sławomir Marczyński
"""

from math import sqrt


def area(a, b, c):
    """
    Obliczanie powierzchni trójkąta za pomocą wzoru Herona.

    Dane:
        a, b, c - długości boków trójkąta.
    Wynik:
        pole powierzchni trójkąta.
    Wyjątki:
        jeżeli trójkąt o podanych długościach boków nie istnieje,
        to zgłaszany jest wyjątek ValueError.
    """
    if (a <= 0 or b <= 0 or c <= 0 or a >= b + c or b >= a + c or c >= a + b):
        raise ValueError('nie ma takiego trójkąta')

    p = (a + b + c) / 2
    s = sqrt(p * (p - a) * (p - b) * (p - c))
    return s


DŁUGOŚĆ_BOKU_BC = 4
DŁUGOŚĆ_BOKU_AC = 5
DŁUGOŚĆ_BOKU_AB = 6

print('długość boku BC =', DŁUGOŚĆ_BOKU_BC)
print('długość boku AC =', DŁUGOŚĆ_BOKU_AC)
print('długość boku AB =', DŁUGOŚĆ_BOKU_AB)

pole_powierzchni = area(DŁUGOŚĆ_BOKU_BC, DŁUGOŚĆ_BOKU_AC, DŁUGOŚĆ_BOKU_AB)

print('pole powierzchni trójkąta =', pole_powierzchni)
