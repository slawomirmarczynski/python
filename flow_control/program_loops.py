#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zastosowanie pętli for i while w języku Python.

Instrukcje iteracji to w Pythonie pętla for i pętla while. Nie ma pętli
do-while, ale dzięki słowom kluczowym break oraz continue da się ją zastąpić
pętlą while.

Oczywiste przykłady można znaleźć w podręcznikach do nauki Pythona,
tu jest parę trudniejszych i mniej oczywistych.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import itertools
import math
import random


# Pętla for wydaje się trywialna, ale trzeba uważać, bo nie wszystko jest tak
# jak niektórych innych popularnych językach.
#
# W przykładzie poniżej będą wypisane tylko cztery gwiazdki - to że w zapisie
# pętli jest liczba pięć nie oznacza że zmienna k przyjmie wartość 5,
# bo w Pythonie range(a, b) oznacza zakres od a włącznie do b wyłącznie.

for k in range(1, 5):
    print('*')


# Podobna jak poniżej pętla w C++ wypisałaby tylko 4 i 104, w Pythonie będzie
# to 4, 104, 6, 106, 8 i 108. Jest tak dlatego że wartość k jest ponownie
# określana na początku pętli.

for k in range(4, 10, 2):
    print(k)
    k = k + 100
    print(k)


# Pętla może nie używać generatora range, tylko kolekcji wyliczalnych elementów
# takich jak listy, krotki, zbioru, słowniki itp. Tu używa krotki.

for k in 4, 6, 8:
    print(k)


# Pętla for może mieć więcej niż jedną "zmienną kontrolną" w taki oto sposób:

coordinates = [ (1, 2), (8, 1), (-1, 3), (2, 4)]
for x, y in coordinates:
    print(math.atan2(y, x))


# Dla ułatwienia numerowania elementów można użyć enumerate jak poniżej:

for k, coordinate in enumerate(coordinates, 1):
    print(k, coordinate)


# Aczkolwiek pętla for-all (for z kolekcją elementów) jest bardzo naturalna,
# to można używać także indeksów tak jak w przykładzie poniżej:

n = len(coordinates)
for k in range(n):
    x = coordinates[k][0]
    y = coordinates[k][1]
    print(math.atan2(y, x))

# Można też użyć iteratorów - obiektów specjalnie służących do iteracji.
# Tworzy się je używając iter(), następnie można pozyskiwać z nich kolejne
# elementy za pomoc next(). Iteratorów nie powinno się używać zamiast for-all,
# są one głównie po to aby można było względnie łatwo tworzyć własne klasy
# obiektów iterowalnych (programując obiektowo w Pythonie).

ci = iter(coordinates)
while True:
    try:
        coordinate = next(ci)
        x, y = coordinate
        print(math.atan2(y, x))
    except StopIteration:
        break


# Instrukcja break przerywa wykonanie pętli, ale tylko jednej pętli. Nie ma
# jakiegoś break-z-etykietą, nie ma też w Pythonie instrukcji goto. Dlatego,
# choć sensownym rozwiązaniem jest użycie instrukcji return lub biblioteki
# itertools, albo nawet instrukcji try-except, najlepiej po prostu pisać
# programy tak aby break nie było konieczne. Dotyczy to pętli for i while.

# print zostanie wywołane 5 razy

for i in range(5):
    for j in range(10):
        print(i, j)
        break

# print zostanie wywołane 1 raz

def foo():
    for i in range(5):
        for j in range(10):
            print(i, j)
            return
foo()

# print zostanie wywołane 1 raz

for i, j in itertools.product(range(5), range(10)):
    print(i, j)
    break

# print zostanie wywołane 1 raz

try:
    for i in range(5):
        for j in range(10):
            print(i, j)
            raise StopIteration
except StopIteration:
    pass


# Rozwiązanie z itertools jest ciekawe, bo zadziała także z continue,
# instrukcją która nakazuje przejście do następnej iteracji. Zwykle continue
# używa się z if, bo bezwarunkowo wykonywane prościej zastąpić usunięciem
# niepotrzebnego martwego kodu.

for i, j in itertools.product(range(5), range(10)):
    if (i > j):
        continue
    print(i, j)

# Lepiej jest jednak nie używać continue (jest to niemal goto) i nie nadużywać
# itertools (jeżeli to nie jest konieczne) - kod poniżej robi to samo co
# poprzedni przykład:

for i in range(5):
    for j in range(10):
        if (i <= j):
            print(i, j)


# Można używać for-else, else jest wywoływane gdy for skończy się "normalnie",
# tj. nie zostanie wywołane break.

data = [1, 2, 3, 4]

for d in data:
    if d == 99:
        print('znaleziono 99')
        break
else:
    print('nie znaleziono 99')


# Pętla while działa w dość oczywisty sposób, poniżej pokazane jest jak można
# jej użyć do oszacowania wartości "maszynowego epsilona".

epsilon = 1.0
while 1.0 + epsilon > 1.0:
    if 1.0 + epsilon / 2.0 == 1.0:
        print('epsilon =', epsilon)
    epsilon = epsilon / 2

# Nie ma w Pythonie instrukcji do-while, więc aby osiągnąć możliwość podjęcia
# decyzji w dowolnym miejscu przydaje się break i pętla while True:

epsilon = 1.0
while True:
    delta = epsilon / 2.0
    if 1.0 + delta == 1.0:
        print('epsilon =', epsilon)
        break
    epsilon = delta


# Podobnie jak for pętla while może mieć swoje else:

epsilon = 1.0
n = 3
while n > 0:
    delta = epsilon / 2.0
    if 1.0 + delta == 1.0:
        print('epsilon =', epsilon)
        break
    epsilon = delta
    n = n - 1
else:
    print(f'nie udało się uzyskać wyniku w 3 krokach')


# for i while są od siebie różne w tym, że for może być użyte w tzw.
# list comprehension,natomiast while nie może

L1 = [x for x in range(100, -1, -1)]  # nie istnieje takie coś z while
