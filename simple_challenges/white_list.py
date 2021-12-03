#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PSą dwie listy z napisami (łańcuchami znaków) L1 i L2, np.:

    L1 = ["la", "to"]
    L2 = ["kot", "semafor", "tolerancja", "kalambur"]

Napisz funkcję która najpierw na podstawie tych dwóch list utworzy takie same
listy, ale zapisane małymi literami. Następnie funkcja ma wyszukać które napisy
z pierwszej listy są fragmentami drugiej. Jako wynik ma być zwracana lista
napisów mających przynajmniej jedno „trafienie”, czyli w naszym przykładzie
["tolerancja", "kalambur"]. Napisz program który przetestuje działanie tej
funkcji.

Przykładowe rozwiązanie poniżej nie jest szczególnie efektywne, ale jest
nieskomplikowane i prawdopodobnie wystarczające w większości praktycznych
zastosowań. Ma ono koszt O(N*M*K) gdzie N jest liczbą sylab, M liczbą słów,
a K jest liczbą liter w każdym słowie (maksymalną, ewentualnie średnią liczbą).

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

L1 = ["la", "to"]
L2 = ["kot", "semafor", "tolerancja", "kalambur"]


def solution(list1_, list2_):
    syllabes = []
    words = []
    for element in list1_:
        syllabes.append(element.lower())
    for element in list2_:
        words.append(element.lower())
    result = []
    for word in words:
        for syllabe in syllabes:
            if syllabe in word:
                result.append(word)
                break
    return result


print(solution(L1, L2))
