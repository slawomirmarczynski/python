#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mamy zgłoszenia podejrzanych SMS-ów: słownik, którego kluczami są dane
kontaktowe zgłaszających spam, a wartościami przypisanymi do tych kluczy
listy numerów telefonów zapisanych jako liczby całkowite. Być może niektóre
zgłoszenia są fałszywe, dlatego chcemy wypisać te numery telefonów, które
były nadesłane przez przynajmniej trzech różnych zgłaszających.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

data = {'Jan Kowalski': [555555011, 555555012, 555555013],
        'Anna Nowak': [555555111, 555555012, 555555099],
        'Gal Anonim': [555555011, 555555012]}

# Zasadniczo powinno się importować wszystkie potrzebne moduły na początku
# programu, bo taki jest zwyczaj (i łatwiej wtedy zorientować się co jest
# importowane), ale instrukcja import może być użyta także wewnątrz programu.

from collections import Counter

counter = Counter()

for key in data:

    # Dość złożona operacja: znajdujemy listę wartości przypisaną do danego
    # klucza i przekształcamy ją w zbiór. W ten sposób eliminujemy ewentualne
    # wielokrotne zgłoszenia z jednego źródła.
    #
    unique_values = set(data[key])
    counter.update(unique_values)

for number in counter:
    if counter[number] >= 3:
        print(number)







