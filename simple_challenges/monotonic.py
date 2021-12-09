#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Napisz funkcję która, dla podanego jako lista ciągu liczb całkowitych, zwraca
(jako nową listę) najdłuższy podciąg niemalejący jaki wystąpił na tej liście.
Przykładowo jeżeli lista zawierałaby

        L = [1, 2, 3, -1, -2, 20, 30, 31, 31, 14, 7]

to powinna zwrócić [-2, 20, 30, 31, 31].

Przetestuj działanie tej funkcji w programie używając przypadkowo
wygenerowanych liczb.


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
