#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zbiory i słowniki.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import random


# Zacznijmy od bardzo prostej rzeczy - mamy dwa ciągi liczb losowych
# i wypiszemy wszystkie te liczby które występują w obu ciągach. Zrobimy to
# najpiew na listach, następnie z użyciem zbiorów.
#
# Naiwne rozwiązanie z listami a i b mogłoby wyglądać tak:

def solution1(a, b):
    c = []
    for i in range(N):
        for j in range(N):
            if a[i] == b[j]:
                for k in range(len(c)):
                    if a[i] == c[k]:
                        break
                else:
                    c.append(a[i])
                break
    return c

# czyli dla każdej liczby z listy a szukamy takiej samej liczby na liście b.
# Zamiast dwóch pętli for możemy użyć tylko jednej, bo Python ma operator in
# sprawdzający czy coś jest na liście (ogólniej czy jest w kolekcji elementów).

def solution2(a, b):
    c = []
    for i in range(N):
        if a[i] in b and a[i] not in c:
            c.append(a[i])
    return c

# Oba powyższe rozwiązania w zasadzie różnią się niewiele - oba wymagają
# O(N**2) porównań. Gdy listy są krótkie nie ma to znaczenia. Gdy są długie
# zaczyna to być problemem. Listy po 100 tysięcy elementów każda zmuszają do
# nawet do dziesięciu miliardów porównań, a to już trochę musi potrwać.
#
# Efektywniejsze jest użycie innej niż lista struktury - takiej jak słownik lub
# takiej jak zbiór.
#
# Zbiory tworzy się podobnie jak listy, tylko że zamiast słowa list jest słowo
# set. Można oczywiście przekształcać, tak jak jest poniżej, listy na zbiory.
# Także operacje na zbiorach są trochę inne nż na listach, zamiast append jest
# add, można (jak poniżej) obliczać część wspólną dwóch zbiorów, sumę itd.

def solution3(a, b):
    a = set(a)
    b = set(b)
    return a & b

# Gdy uruchomiłem poniższy fragment kodu z użyciem profilera

N = 10000
A = [random.randint(1, N) for k in range(N)]
B = [random.randint(1, N) for k in range(N)]

s1 = solution1(A, B)  # 6900 milisekund
s2 = solution2(A, B)  #  870 milisekund
s3 = solution3(A, B)  #    1 milisekunda

print(len(s1))
print(len(s2))
print(len(s3))

# to okazało się że czasy wykonania wynosiły odpowiednio niemal 7 sekund dla
# solution1, około jedną sekundę dla solution2 i tylko jedną milisekundę dla
# solution3. W jaki sposób solution3 zyskuje aż tak bardzo na czasie?
#
# Gdy używamy zbiorów Python stosuje tzw. tablice mieszające (hash tables),
# więc nie musi w ogóle przeszukiwać całych list a jedynie sprawdza czy
# już ma element z daną wartością "hasza". Koszt czasowy takiej operacji jest
# stały, czyli O(1).
#
# Zbiory z założenie przechowują każdą wartość jako jeden element. Jeżeli do
# zbioru w którym już jest liczba 42 dorzucimy jeszcze raz 42, to zbiór się
# nie zmieni - liczba 42 może być odnotowana jako należąca do zbioru lub jako
# nie należąca, skoro już była w zbiorze to nie może być w zbiorze "bardziej".
#
# Aby policzyć ile razy każda z liczb z pierwszej listy wystąpiła na drugiej
# liście możemy użyć słownika, struktury danych podobnie efektywnej jak zbiór,
# ale wiążącej ze sobą klucz i wartość. W pewnym sensie słowniki (w niektorych
# innych językach nazywane mapami lub tablicami asocjacyjnymi) są uogólnieniem
# tablic. W tablicy indeksami elementów tablic są liczby całkowite,
# w słownikach indeksem elementu może być cokolwiek - nawet inny słownik.

def solution4(a, b):
    dictionary = {}
    for element in a:
        dictionary[element] = 0
    for element in b:
        if element in dictionary:
            dictionary[element] += 1
    return sorted(dictionary)

s4 = solution4(A, B)
print(s4)

# Czas wykonania na tym samym komputerze co poprzednio wyniósł około 1.5 ms,
# czyli jest porównywalny z tym który osiągnęliśmy dla zbiorów.
#
# Pozostaje wyjaśnić dlaczego nie mogliśmy użyć "zwykłych tablic". Owszem,
# w szczególnym przypadku, gdy zakres wartości generowanych liczb losowych
# byłby niewielki, np. od 0 do 1000, tablice mogłyby być dobrym rozwiązaniem.
# Jednakże gdy zakres ten jest duży, np. od 0 do 100 miliardów, to nawet
# dla krótkich ciągów (np. 5-elementowych) potrzebowalibyśmy gigantycznych
# tablic które i tak byłby prawie puste.
