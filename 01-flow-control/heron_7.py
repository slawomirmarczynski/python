#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Wyłączenie komunikatów że nazwy a, b, c nie są zgodne z konwencją PEP8.
# pylint: disable=c0103

"""
Obliczanie pola powierzchni trójkąta którego długości boków są znane.

Do obliczenia pola powierzchni trójkąta gdy znane są długości boków używamy
wzoru Herona, patrz https://pl.wikipedia.org/wiki/Wzór_Herona (10.10.2020).

W tej wersji programu sprawdzanie poprawności jest wyodrębnione w sposób
umożliwiający przetestowania danych niezależnie od liczenia pola powierzchni.

CC-BY-NC-ND 2020 Sławomir Marczyński
"""

from math import sqrt


def check(a, b, c):
    """
    Funkcja check sprawdza, czy trójkąt o bokach a, b, c może istnieć.
    Zakładamy przy tym że trójkąt musi mieć niezerowe pole powierzchni.
    Zwraca True jeżeli trójkąt istnieje albo False.
    """
    bad_sign = a <= 0 or b <= 0 or c <= 0
    bad_length = a >= b + c or b >= c + a or c >= a + b
    return not bad_sign and not bad_length


def area(a, b, c):
    """
    Obliczanie powierzchni trójkąta za pomocą wzoru Herona.

    Dane:
        a, b, c - długości boków trójkąta.
    Wynik:
        pole powierzchni trójkąta.
    Wyjątki:
        jeżeli trójkąt o podanych długościach boków nie istnieje to zgłaszany
        jest wyjątek ValueError.

    """

    if check(a, b, c):
        p = (a + b + c) / 2
        s = sqrt(p * (p - a) * (p - b) * (p - c))
        return s
    else:
        raise ValueError


def main():

    DŁUGOŚĆ_BOKU_BC = 4
    DŁUGOŚĆ_BOKU_AC = 5
    DŁUGOŚĆ_BOKU_AB = 6

    print('długość boku BC =', DŁUGOŚĆ_BOKU_BC)
    print('długość boku AC =', DŁUGOŚĆ_BOKU_AC)
    print('długość boku AB =', DŁUGOŚĆ_BOKU_AB)

    pole_powierzchni = area(DŁUGOŚĆ_BOKU_BC, DŁUGOŚĆ_BOKU_AC, DŁUGOŚĆ_BOKU_AB)

    print('pole powierzchni trójkąta =', pole_powierzchni)


if __name__ == '__main__':
    main()
