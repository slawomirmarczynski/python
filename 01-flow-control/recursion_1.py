#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rekurencja zamiast pętli for - przykład że nawet nie mając ani instukcji goto,
ani pętli for, while itp. - możemy powtarzać określoną liczbę razy wykonanie
wybranego fragmentu programu.

CC-BY-NC-ND 2020 Sławomir Marczyński
"""

# Najprostsze rozwiązanie (w Pythonie) to po prostu napisać::
#
#   for k in range(n):
#       print(k)
#
# ewentualnie można też użyć pętli while::
#
#   k = 0
#   while (k < n):
#       print(k)
#
# Jednak rozwiązanie poniżej zamiast iteracji używa rekurencji.

def fun(k, n):
    if k < n:
        print(k)
        fun(k + 1, n)


n = int(input('Napisz ile linijek ma być wypisanych: '))
fun(0, n)

