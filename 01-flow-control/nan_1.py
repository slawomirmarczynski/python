#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przykład nieoczywistego działania instrukcji warunkowej.

Dla dwóch liczb rzeczywistych a oraz b może zajść tylko jedna z trzech
możliwości - albo a jest większa niż b, albo b jest większa niż a, albo obie
te liczby są sobie równe. W Pythonie, podobnie jak w wielu innych językach
programowania, można przeprowadzać obliczenia na liczbach zmiennoprzecinkowych,
które są zwykle, choć błędnie, utożsamiane z liczbami rzeczywistymi.

Dlaczego błędnie? Po pierwsze, liczb rzeczywistych jest nieskończenie wiele.
Natomiast różnych wartości zmiennoprzecinkowych (przy założonej z góry liczbie
bitów) jest skończona ilość. Dowód: jest tylko 2**n różnych kombinacji jeżeli
ciąg składa się z n bitów. Po drugie, liczby zmiennoprzecinkowe reprezentują
wyłącznie liczby wymierne, a liczby rzeczywiste (w sensie matematycznym)
zawierają także liczby niewymierne (takie jak pi). Po trzecie - zgodnie ze
standardem IEEE 754 - liczby zmiennoprzecinkowe (w informatyce) mogą także
reprezentować szczególne wartości takie jak nieskończoność i nie-liczby
(Not-a-Number, w Pythonie zapisywane jako nan). NaN można sobie wyobrazić jako
- znaną z matematyki - wartość nieoznaczoną, taką jak 0/0 czy iloraz dwóch
nieskończoności. NaN może pojawić się jako rezultat obliczeń, albo być wprost
wykorzystana jako "zastępcza wartość" zamiast brakujących danych.

Porównując NaN z czymkolwiek, nawet z NaN, zawsze otrzymuje się jako wynik
fałsz (czyli False). Może to powodować zupełnie nieoczekiwane przez mniej
doświadczonych programistów działanie programów. Przykłady są poniżej.

CC-BY-NC-ND 2020 Sławomir Marczyński
"""

from math import nan

print()
print('Testowanie zachowania się nie-liczb (NaN) w operacjach porównywania')
print()

a = nan  # zmienna a przechowuje wartość Not-a-Number
b = nan  # zmienna b przechowuje wartość Not-a-Number, taką samą jak a

print('a =', a)
print('b =', b)
print()

if a != b:  # jeżeli a jest różne od b (wydaje się że powinno być takie samo)
    print('Niemożliwe... a jest różne od b')

if a != a:  # jeżeli a jest różne od a (wydaje się że powinno być takie samo)
    print('Niemożliwe... a jest różne od a')


if a < b:
    print('a jest mniejsze niż b')
elif a > b:
    print('a jest większe niż b')
elif a == b:
    print('a jest równe b')
else:
    print('Niemożliwe... a nie jest ani większe, ani mniejsze, ani równe b')


if a < 0:
    print('a jest mniejsze niż b')
elif a > 0:
    print('a jest większe niż b')
elif a == 0:
    print('a jest równe b')
else:
    print('Niemożliwe... a nie jest ani większe, ani mniejsze, ani równe zeru')


if a == False:
    print('prawdą jest że a == False')
else:
    print('nieprawdą jest że a == False')

if a != False:
    print('prawdą jest że a != False')
else:
    print('nieprawdą jest że a != False')

if a == True:
    print('prawdą jest że a == True')
else:
    print('nieprawdą jest że a == True')

if a != True:
    print('prawdą jest że a != True')
else:
    print('nieprawdą jest że a != True')


print()
print('czyli nan nie jest w porównaniach ani True ani False')
print('jednak użyte bezpośrednio po if zachowuje się jakby', end=' ')

if a:
    print('było True')
else:
    print('było False')
