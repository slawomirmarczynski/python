#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lista L składa się z list które są listami czterech par współrzędnych x, y.

Przykładowo:

    L = [ [[1, 2], [2, 3], [4, 2], [118, 9]],
         [[0, 1], [1, 0], [1, 1], [0, 0]] ]

Napisz funkcję która zwróci jako wynik swojego działania listę tych list
czteroelementowych których współrzędne są wierzchołkami kwadratów. dla podanej
powyżej listy będzie to

    [[0, 1], [1, 0], [1, 1], [0, 0]]]

bo podane punkty mogą być (kolejność nie ma znaczenia) wierzchołkami kwadratu.

Wskazówka: oblicz ze wzoru Pitagorasa odległości pomiędzy punktami – jeżeli są
to wierzchołki kwadratu to boki i przekątne będą miały odpowiednie długości.

CC-BY-NC-Nd 2021 Sławomir Marczyński
"""

import itertools
from math import sqrt, isclose


def solution(polygons):
    def distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    squares = []
    for polygon in polygons:
        if len(polygon) == 4:
            vertices_permutations = itertools.permutations(polygon)
            for A, B, C, D in vertices_permutations:
                AB = distance(A, B)
                BC = distance(B, C)
                CD = distance(C, D)
                AD = distance(A, D)
                AC = distance(A, C)
                BD = distance(B, D)
                if (isclose(AB, BC) and isclose(AB, CD) 
                        and isclose(AB, AD) and isclose(AC, BD) 
                        and isclose(sqrt(2) * AB, AC))
                        and isclose(sqrt(2) * AB, BD)):
                    squares.append(polygon)
                    break
    return squares


L = [[[1, 2], [2, 3], [4, 2], [118, 9]],
     [[0, 1], [1, 0], [1, 1], [0, 0]]]

print(L)
print(solution(L))
