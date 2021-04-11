#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Wyłączenie komunikatów że nazwy a, b, c nie są zgodne z konwencją PEP8.
# pylint: disable=c0103
#
# Program pylint służy do analizy zgodności kodu źródłowego z zalecaniami
# stylistycznymi, a to pozwala na wychwycenie różnego rodzaju niedoskonałości.
# Jednak pylint jest prostym programem i nie zawsze ma rację, np. domagając
# się dłuższych niż jednoliterowe nazw zmiennych. Można zmienić zachowanie
# programu pylint edytując jego konfigurację, można też je dostroić podając
# w programie (po znaku komentarza) polecenia takie jak powyżej.

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
        jeżeli trójkąt o podanych długościach boków nie istnieje i są
        sprawdzane asercje, to zgłaszany jest wyjątek AssertionError.

    """

    # UWAGA: assert jest gorszym rozwiązaniem niż sprawdzanie instrukcją if
    # wyjątku ValueError. Assert może nie zadziałać - bo jest możliwość
    # wyłączania - dla przyspieszenia programu - działania instrukcji Assert.
    # Z drugiej strony jeżeli mamy pewność że dane nie potrzebują sprawdzania
    # to wyłączenie assert może przyspieszyć działanie programu.
    #
    # Instrukcja assert expression jest równoważna takiemu fragmentowi kodu::
    #
    #    if __debug__:
    #        if not expression: raise AssertionError

    assert a > 0 and b > 0 and c > 0
    assert a < b + c and b < a + c and c < a + b

    p = (a + b + c) / 2
    s = sqrt(p * (p - a) * (p - b) * (p - c))
    return s


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
