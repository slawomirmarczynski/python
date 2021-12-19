#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przepływ ciepła.

Problem fizyczny:


Sposób rozwiązania:


CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import numpy as np
from matplotlib import pyplot as plt

temp_lo = 25.0
temp_hi = 80.0

N = 20      # rozmiar siatki wzdłuż osi x
M = 100     # rozmiar siatki wzdłuż osi y
NM = N * M  # łączna liczba węzłów siatki

a = np.zeros((NM, NM))
b = np.zeros(NM)


def index_ij(i, j):
    return i * M + j


for i in range(N):
    for j in range(M):
        ij = index_ij(i, j)
        a[ij, ij] = 1
        if i != 0 and i != N - 1 and j != 0 and j != M - 1:
            if i > 0:
                a[ij, index_ij(i - 1, j)] = -0.25
            if i < N - 1:
                a[ij, index_ij(i + 1, j)] = -0.25
            if j > 0:
                a[ij, index_ij(i, j - 1)] = -0.25
            if j < M - 1:
                a[ij, index_ij(i, j + 1)] = -0.25
        else:
            b[ij] = temp_lo if i != 0 else temp_hi

solution = np.linalg.solve(a, b)
solution = np.reshape(solution, (N, M))

plt.contourf(solution)
plt.gca().set_aspect('equal')
plt.hot()
plt.colorbar()
plt.show()
