#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wypisywanie listy z listami które mogą składać się z list które ... itd.

Podobny przykład jest w książce "Python. Rusz głową!" Paula Barrego,
dowcip w tym że chcemy wypisać te listy w uporządkowanej (posortowanej)
kolejności.

CC-BY-NC-ND 2022 Sławomir Marczyński
"""

# Przykładowa - trudna do posortowania! - lista. Problem w tym że pomieszane
# są elementy będące listami, elementy będące łańcuchami znaków i elementy
# będące liczbami całkowitymi... a Python nie chce porównywać list i łańcuchów,
# nie potrafi też porównać liczb i łańcuchów (czyli co jest większe 1 czy "1").

L = ['Łańcuch znaków', ['Bob', [9, 8, 7]], ['Ala', [1, 2, 3]], 'albo', 4, []]

def print_nice(data, ident=0):

    # Wielkość (w spacjach) wcięcia przy wypisywaniu kolejnego poziomu.

    PRINT_NICE_IDENT = 4

    def key_function(x):
        islist = isinstance(x, list)
        if islist:
            x = x[0]
        for idx, ev in enumerate((int, str)):
            try:
                value = ev(x)
                return islist, idx, value
            except:
                pass
        return islist, -1, -1

    if not data:
        return

    try:
        data.remove('')
    except:
        pass

    try:
        data.remove([])
    except:
        pass

    for element in sorted(data, key=key_function):
        if isinstance(element, list):
            print_nice(element, ident + PRINT_NICE_IDENT)
        else:
            print(' '*ident, element, sep='')


print_nice(L)
