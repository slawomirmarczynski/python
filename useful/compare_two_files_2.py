#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Porównywanie zawartości dwóch plików ignorujące znaki specjalne.

Chcemy porównać czy dwa pliki tekstowe zawierają taką samą treść. Dopuszczamy
różnice takie jak dodatkowe spacje czy zmiany linii, ale litery muszą być takie
same. Pliki uznać chcemy także za różne jeżeli w jednym z nich będzie napisane
"tak samo", a w drugim "taksamo" (bez spacji pomiędzy wyrazami).

Program ilustruje: czytanie plików tekstowych i techniki pracy z nimi; pracę
z łańcuchami znaków jako tablicami znaków; użycie pętli while i instrukcji
warunkowych; definiowanie i użycie funkcji.

Uwaga, rozwiązanie tu przedstawione jest nadal niezbyt "pythoniczne".
Znacznie lepsze będzie pokazane w "wersji 3.0" programu.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

# Rozwiązanie prowizoryczne - zamiast pozyskiwać nazwy plików po uruchomieniu
# programu - nazwy plików są zapisane wprost w programie.
#
FILE_NAME1 = 'compare_two_files_plik1.txt'
FILE_NAME2 = 'compare_two_files_plik2.txt'


# Takie same operacje wykonywane więcej niż raz najlepiej zapisać jako funkcje
# (w Pythonie funkcje i procedury to to samo). Nawet jeżeli ciąg istrukcji jest
# tylko raz używany - ale ma określone działanie, służy konkretnemu celowi
# - to i tak sensowne jest zapisanie go jako funkcji.


def read_file_as_text(file_name):
    """
    Czytanie całej zawartości pliku tekstowego na raz.

    Parametry:
        file_name (łańcuch znaków): nazwa pliku jaki ma być przeczytany.

    Zwraca:
        text (łańcuch znaków): przeczytana zawartość pliku.
    """
    file = open(file_name)
    text = file.read()
    file.close()
    return text


def is_white_char(ch):
    """
    Sprawdzanie czy znak jest białym znakiem.

    Parametry:
        ch (znak): znak który chcemy sprawdzić.

    Zwraca:
        prawdę lub fałsz odpowiednio do tego czy znak był białym znakiem.
    """
    return ch == ' ' or ch == '\t' or ch == '\n'


text1 = read_file_as_text(FILE_NAME1)
text2 = read_file_as_text(FILE_NAME2)
i1 = 0
i2 = 0
len1 = len(text1)
len2 = len(text2)


# Początkowo zakładamy że pliki są jednakowe, jeżeli okaże się że nie są to
# zmienimy True na False:

files_contain_the_same_text = True


# Wielokrotnie, w pętli, dopóki nie zostaną osiągnięte koniec pierwszego tekstu
# i koniec drugiego tekstu, albo znajdziemy różnice w tekstach.
#
while i1 < len1 and i2 < len2 and files_contain_the_same_text:

    # Pomijamy wszystkie białe znaki jakie mogą być na początku.

    while i1 < len1 and is_white_char(text1[i1]):
        i1 += 1

    while i1 < len1 and is_white_char(text2[i2]):
        i2 += 1

    while i1 < len1 and i2 < len2:
        if text1[i1] != text2[i2]:
            ws1 = is_white_char(text1[i1])
            ws2 = is_white_char(text2[i2])
            if ws1 or ws2:  # oba znaki są białe
                break
            if not ws1 or not ws2:  # np. 'A' != 'x', 'A' != ' ' itp. różnice
                files_contain_the_same_text = False
                break
        else:
            i1 += 1  # będziemy badać kolejny znak z text1
            i2 += 1  # będziemy badać kolejny znak z text2


# Jeżeli jesteśmy tu to już wiemy jaki jest wynik

if files_contain_the_same_text:
    print('pomijając nieistotne różnice pliki są takie same')
else:
    print('pliki są istotnie różne')
