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

L = ['Łańcuch znaków', ['Bob', [9, 8, 7]], ['Ala', [1, 2, 3]],
     'albo', '',  4, []]

def print_nice(data, ident=0):
    """
    Wypisywanie, ze wcięciami, list zagnieżdżonych.

    Parametry:
        data: co ma być wypisane.
        ident: początkowa wartość wcięcia (domyślnie 0, czyli bez wcięcia).
    """

    # Wielkość (w spacjach) wcięcia przy wypisywaniu kolejnego poziomu.

    PRINT_NICE_IDENT = 4

    def key_function(x):
        """
        Funkcja przyporządkująca kolejność elementów jako krotkę.

        Parametry:
            x: element.
        """
        islist = isinstance(x, list)
        if islist:
            x = x[0] if x else None;
        for idx, ev in enumerate((int, str)):
            try:
                value = ev(x)
                return islist, idx, value
            except:
                pass
        return islist, -1, -1

    # Bierzemy kolejne elementy z posortowanej (na jednym poziomie) liście.
    # Jeżeli taki element jest listą to rekurencyjnie wywołujemy print_nice,
    # jeżeli listą nie jest to wypisujemy go.

    for element in sorted(data, key=key_function):
        if isinstance(element, list):
            print_nice(element, ident + PRINT_NICE_IDENT)
        else:
            # Warunek if poniżej sprawdza czy jest realnie coś do wypisania,
            # czy też może element będzie łańcuchem pustym lub ciągiem spacji.
            if len(str(element).strip()):
                print(' '*ident, element, sep='')


# Tu uruchamiamy napisaną funkcję dla listy L

print_nice(L)
