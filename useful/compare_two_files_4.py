#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Porównywanie zawartości dwóch plików ignorujące znaki specjalne.

Chcemy porównać czy dawa pliki tekstowe zawierają taką samą treść. Dopuszczamy
różnice takie jak dodatkowe spacje czy zmiany linii, ale litery muszą być takie
same. Pliki uznać chcemy także za różne jeżeli w jednym z nich będzie napisane
"tak samo", a w drugim "taksamo" (bez spacji pomiędzy wyrazami).

Rozwiązanie "pythoniczne", czyli takie w którym wykorzystujemy regex'y oraz
specyficzne cechy języka Python aby program był prosty, czytelny i zwięzły.
Ten kod źródłowy jest taki sam jak poprzednio (compare_two_files_4.py),
ale usunięte są komentarze przeznaczone dla początkujacych.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import re

# @todo: Nazwy plików pobierać z argumentów wywołania programu.
#
FILE_NAME1 = 'plik1.txt'
FILE_NAME2 = 'plik2.txt'


def read_text(file_name):
    """
    Wczytywanie danych.

    Czytanie całej zawartości pliku tekstowego na raz. Wszystkie ciągi spacji,
    znaków nowego wiersza lub tabulacji są zamieniane na pojedyncze spacje.

    Parametry:
        file_name (łańcuch znaków): nazwa pliku jaki ma być przeczytany.

    Zwraca:
        text (łańcuch znaków): przeczytana i znormalizowana zawartość pliku.
    """
    with open(file_name) as file:
        text = file.read()
    text = text.strip()
    text = re.sub(r'\s+', '*', text)
    return text


text1 = read_text(FILE_NAME1)
text2 = read_text(FILE_NAME2)

if text1 == text2:
    print('pomijając nieistotne różnice pliki są takie same')
else:
    print('pliki są istotnie różne')
