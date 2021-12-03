#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
Porównywanie zawartości dwóch plików ignorujące znaki specjalne.

Chcemy porównać czy dawa pliki tekstowe zawierają taką samą treść. Dopuszczamy
różnice takie jak dodatkowe spacje czy zmiany linii, ale litery muszą być takie
same. Pliki uznać chcemy także za różne jeżeli w jednym z nich będzie napisane
"tak samo", a w drugim "taksamo" (bez spacji pomiędzy wyrazami).

Program ilustruje: czytanie plików tekstowych i techniki pracy z nimi; pracę
z łańcuchami znaków jako tablicami znaków; użycie pętli while i instrukcji
warunkowych.

Uwaga, rozwiązanie tu przedstawione jest niezbyt "pythoniczne". Znacznie lepsze
będzie pokazane w "wersji 3.0" programu.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""


# Rozwiązanie prowizoryczne - zamiast pozyskiwać nazwy plików po uruchomieniu
# programu - nazwy plików są zapisane wprost w programie.
#
FILE_NAME1 = 'plik1.txt'
FILE_NAME2 = 'plik2.txt'


# Otwieramy dwa pliki, w domyślnym trybie, czyli do odczytu.
#
file1 = open(FILE_NAME1)
file2 = open(FILE_NAME2)


# Czytamy pliki od razu w całości, bez dzielenia na linie a tym bardziej bez
# analizowania czytanych znaków.
#
text1 = file1.read()
text2 = file2.read()


# Zamykamy pliki - to jest konieczne, chyba że zaufamy Pythonowi że sam je
# zamknie gdy zakończy się cały program.
#
file1.close()
file2.close()


# Problem - mamy już nie dwa pliki, ale dwa teksty (text1 i text2), ale nadal
# nie rozwiązaliśmy problemu jak porównywać zgodnie z warunkami zadania.
# Spróbujemy po prostu z dwoma indeksami i1 i i2 wybierającymi elementy (znaki)
# z odpowiednio text1 i text2, tak jak poniżej.

i1 = 0
i2 = 0
len1 = len(text1)  # długość pierwszego tekstu
len2 = len(text2)  # długość drugiego tekstu


# Początkowo zakładamy że pliki są jednakowe, jeżeli okaże się że nie są to
# zmienimy True na False:

files_contain_the_same_text = True


# Wielokrotnie, w pętli, dopóki nie zostaną osiągnięte koniec pierwszego tekstu
# i koniec drugiego tekstu, albo znajdziemy różnice w tekstach.
#
while i1 < len1 and i2 < len2 and files_contain_the_same_text:

    # Pomijamy wszystkie białe znaki jakie mogą być na początku.

    while i1 < len1 and (text1[i1] == ' ' or text1[i1] == '\t' or text1[i1] == '\n'):
        i1 += 1

    while i1 < len1 and (text2[i2] == ' ' or text2[i2] == '\t' or text2[i2] == '\n'):
        i2 += 1

    # Sprawdzamy czy nie-białe znaki są takie same - jeżeli nie to pliki się
    # istotnie różnią - możemy dalej nie sprawdzać.
    #
    # Uwaga: jeżeli po nie-białych znakach będą jeszcze identyczne białe znaki
    # to oczywiście to nie przeszkadza aby pliki mogły być takie same. Dlatego
    # sprawdzanie możemy znacznie uprościć.

    while i1 < len1 and i2 < len2:
        if text1[i1] != text2[i2]:
            ws1 = text1[i1] == ' ' or text1[i1] == '\t' or text1[i1] == '\n'
            ws2 = text2[i2] == ' ' or text2[i2] == '\t' or text2[i2] == '\n'
            if ws1 or ws2:  # oba znaki są białe
                break
            if not ws1 or not ws2:  # np. 'A' != 'x', 'A' != ' ' itp. różnice
                files_contain_the_same_text = False
                break
        else:
            i1 += 1  # będziemy badać kolejny znak z text1
            i2 += 1  # będziemy badać kolejny znak z text2


# Jeżeli jesteśmy tu to już wiemy jaki jest wynik.

if files_contain_the_same_text:
    print('pomijając nieistotne różnice pliki są takie same')
else:
    print('pliki są istotnie różne')
