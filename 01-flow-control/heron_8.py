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
Obliczanie pola powierzchni trójkąta - szkic jak można byłoby zrobić to
dla trójkątów zadanych na rozmaite sposoby - boki, kąty, współrzędne
wierzchołków.

CC-BY-NC-ND 2020 Sławomir Marczyński
"""

from math import sqrt


def area(a=None, b=None, c=None,
         A=None, B=None, C=None, alpha=None, beta=None, gamma=None):
    """
    Obliczanie powierzchni trójkąta.

    Dane:
        a, b, c -- długości boków trójkąta;
        A, B, C -- współrzędne wierzchołków trójkąta, np. A=(3, 2) albo nawet
                   A=(3, 2, 2) jeżeli obliczenia będą w przestrzeniu 3D.
        alpha, beta, gamma -- miary kątów trójkąta (w stopniach).
    Wynik:
        pole powierzchni trójkąta, jeżli trójkąt istnieje. Jeżeli trójkąt
        o podanych bokach, wierzchołkach i kątach nie istnieje - zgłaszany
        jest wyjątek ValueError.
    """
    #
    # @todo -- tu, zamiast raise NotImplemented, trzeba napisać cały kod
    # źródłowy tak, aby zweryfikować dane i obliczyć pole powierzchni.
    #
    raise NotImplemented


pole_powierzchni = area(a = 4, b = 4, gamma=45)

print('pole powierzchni trójkąta =', pole_powierzchni)
