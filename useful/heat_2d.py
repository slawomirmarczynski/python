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

temp_lo = 20.0
temp_hi = 80.0

N = 40      # rozmiar siatki wzdłuż osi x
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


x = np.linspace(0, M / 10, M)
y = np.linspace(0, N / 10, N)


plt.contourf(x, y, solution)
plt.gca().set_aspect('equal')
plt.hot()
plt.colorbar()
plt.title('rozkład temperatur w płaszczyźnie xy')
plt.xlabel('x')
plt.ylabel('y')
plt.show()


plt.plot(x, solution[N // 2, :],
         x, (temp_hi + temp_lo) / 2 * np.ones(M))
plt.grid()
plt.title('rozkład temperatur w połowie grubości płytki')
plt.xlabel('x, mm')
plt.ylabel('temperatura, °C')
plt.legend(('model', 'połowa różnicy temperatur'))
plt.show()


plt.plot(y, solution[:, 1],
         y, solution[:, 10],
         y, solution[:, M // 4],
         y, solution[:, M // 2],
         y, temp_hi - (temp_hi - temp_lo) / N * 10 * y, '--')
plt.grid()
plt.title('rozkład temperatur w połowie grubości płytki')
plt.xlabel('y, mm')
plt.ylabel('temperatura, °C')
plt.legend(('wyniki dla x = 0.1 mm',
            'wyniki dla x = 1 mm',
            'wyniki dla x = 1/4 xmax',
            'wyniki dla x = 1/2 xmax',
            'linia prosta od t_min do t_max'))
plt.show()


print()
print(f'temperatura w centrum płytki wynosi {solution[N // 2, M // 2]} °C')
print()
