#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Są dwie listy z napisami (łańcuchami znaków) L1 i L2, np.:

    L1 = ["la", "to"]
    L2 = ["kot", "semafor", "tolerancja", "kalambur"]

Napisz funkcję która dla podanego jako lista ciągu liczb całkowitych, zwraca
(jako nową listę) najdłuższy podciąg niemalejący jaki wystąpił na tej liście.
Przykładowo jeżeli lista zawierałaby L = [1, 2, 3, -1, -2, 20, 30, 31, 31, 14,
7] to powinna zwrócić [-2, 20, 30, 31, 31]. Przetestuj działanie tej funkcji
w programie używając przypadkowo wygenerowanych liczb.

Przykładowe rozwiązanie poniżej nie jest efektywne (można to naprawić
zastępując pętlę for, w której begin przyjmuje kolejne wartości, pętlą while
przeskakującą już raz sprawdzone elementy listy), ale jest nieskomplikowane.

Warto zapamiętać schemat optymalizacji - przyjmujemy jakieś rozwiązanie jako
chwilowo najlepsze i systematycznie sprawdzamy czy można zastąpić go lepszym.


CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import random


L = [1, 2, 3, -1, -2, 20, 30, 31, 31, 14, 7]


def solution(list_):

    best_begin = 0
    best_end = 0
    best_length = 0

    n = len(list_)
    for begin in range(n):  # @todo: pętla while byłaby lepsza
        end = begin + 1
        while end < n and list_[end - 1] <= list_[end]:
            end += 1
            if end - begin > best_length:
                best_begin = begin
                best_end = end
                best_length = best_end - best_begin
        begin += 1

    return list_[best_begin:best_end]


print()
print('  dane =', L)
print('wyniki =', solution(L))
print()

random_sequence = [random.randint(1, 10) for i in range(20)]
print()
print('  dane =', random_sequence)
print('wyniki =', solution(random_sequence))
print()
