#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przepływ ciepła.

Problem fizyczny:

    Jak zmienia się temperatura wewnątrz płytki miedzianej o prostokątnym
    kształcie, obłożonej po obu stronach izolacją cieplną, której jedna krawędź
    ma temperaturę 100 stopni Celsjusza, a pozostałe krawędzie są utrzymywane
    w temperaturze 20 stopni.

    W szczególności jak znacznie (o ile procent) temperatura w geometrycznym
    środku płytki będzie różna od temperatury obliczonej jako średnia
    temperatura pomiędzy krawędziami równa (100 + 20) / 2, czyli 60 stopni?


Sposób rozwiązania:

    Przepływ ciepła następuje z miejsc o tempreraturze wyższej do tych gdzie
    temperatura jest niższa. Podgrzewając bryłę jednorodnego materiału z jednej
    strony, a z drugiej go chłodząc, osiągamy w różnych miejscach różne
    temperatury. Ogólnie, w 3D, czyli w zależności od np. współrzędnych x, y, z
    oraz czasu, problem nie jest łatwy do rozwiązania. Dlatego, dla uproszczenia
    zakładamy że interesuje nas stan ustalony, taki w którym nie ma zależności
    od czasu. Redukujemy go także do 2D, czyli pozostawiamy tylko współrzędne
    x, y. Możemy tak zrobić gdy bryła przewodząca jest izolowana cieplnie,
    tak że strumień ciepła nie przepływa wzdłuż osi z.

    Równanie paraboliczne przewodnictwa cieplnego ma postać αΔu = ∂u/∂t,
    gdzie α to współczynnik dyfuzji cieplnej, u to temperatura, Δ jest
    laplasjanem. Ok, laplasjan (Δ = ∇² = ∂²/∂x² + ∂²/∂y² + ∂²/∂z², czyli coś
    innego niż delta Δ) to raczej zaawansowany temat (nota bene przewodnictwo
    cieplne można też opisywać trochę trudniejszym równaniem hiperbolicznym).

    Dla nas jest ważne tylko że: po pierwsze gdy nie ma zmian w czasie (a więc
    ∂u/∂t = 0) równanie to upraszcza się do równania Laplace'a ∇²u = 0;
    po drugie, rozwiązaniami równania Laplace'a są tzw. funkcje harmoniczne,
    mające tę przyjemną cechę że ich wartość jest równa średniej z wartości
    w punktach sąsiednich. Można do tego także dojść (na siatce jak poniżej)
    pochodne zastępując różnicami skończonymi.

    Obliczenia przeprowadzamy na siatce punktów: N rzędów, M kolumn.
    Punkty z i-tego wiersza i j-tej kolumny numerujemy k = i + j * N, tak więc
    mamy k przebiegające od 0 do N*M-1, bo i jest od 0 do N-1, j od 0 do M-1.

    Punkt mający współrzędne (i, j) ma jako czterech najbliższych
    sąsiadów punkty (i-1, j), (i+1, j), (i, j-1), (i, j+1)... chyba że jest na
    brzegu siatki. Punkty brzegowe mają ustalone "ręcznie" temperatury.

    Tempreratury u spełniać muszą, dla odpowiednich i,j, równania:

        u(i,j) - c*u(i-1, j) - c*u(i+1, j) - c*u(i, j-1) - c*u(i, j+1) = b(k)

    gdzie c = 1/4. Wartości b(k) to temperatury na brzegu bryły (k odpowiada
    punktowi na brzegu), albo zero (dla punktów wewnętrznych).

    Oczywiście rozwiązania należałoby jeszcze przeskalować ze współrzędnych
    (i, j) do "zwykłych" (x, y). I jakoś zaprezentować w formie wykresów itp.

    Daje to, dla dość skromnej siatki 100x100 układ 10000 równań liniowych
    z 10000 niewiadomych. I być może nie jest to (nawet gdybyśmy użyli macierzy
    rzadkich) najlepszy możliwy sposób rozwiązywania. Ale obecne (rok 2022)
    możliwości komputerów, języka Python i jego bibliotek (NumPy i SciPy oraz
    Matplotlib), okazują się więcej niż wystarczające aby cały pomysł dało
    się zrealizować.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import numpy as np
from matplotlib import pyplot as plt

temp_lo = 20.0
temp_hi = 80.0

# Wybór nieparzystych N i M da węzeł dokładnie pośrodku płytki.

N = 41      # rozmiar siatki wzdłuż osi y
M = 101     # rozmiar siatki wzdłuż osi x
NM = N * M  # łączna liczba węzłów siatki

a = np.zeros((NM, NM))
b = np.zeros(NM)

# Tworzenie macierzy współczynników i wektora wyrazów wolnych układu równań
# liniowych a * u == b

for i in range(N):
    for j in range(M):
        k = i + j * N
        a[k, k] = 1
        if i != 0 and i != N - 1 and j != 0 and j != M - 1:
            if i > 0:
                a[k, i - 1 + j * N] = -0.25
            if i < N - 1:
                a[k, i + 1 + j * N] = -0.25
            if j > 0:
                a[k, i + (j - 1) * N] = -0.25
            if j < M - 1:
                a[k, i + (j + 1) * N] = -0.25
        else:
            b[k] = temp_lo if i != 0 else temp_hi


solution = np.linalg.solve(a, b)
solution = np.reshape(solution, (M, N))
solution = np.transpose(solution)


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
temp_average = (temp_lo + temp_hi) / 2
temp_center = solution[N // 2, M // 2]
rel_diff_temp = (temp_center - temp_average) / temp_average
print(f'temperatura w centrum płytki wynosi {solution[N // 2, M // 2]:.1f} °C')
print('różnica procentowa',
      '{:.1%}'.format(rel_diff_temp),
      'w porównaniu z przewidywaną temperaturą')
print()
