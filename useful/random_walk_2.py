#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Błądzenie przypadkowe.

Błądzenie przypadkowe (random walking) jest uproszczonym modelem dyfuzji gazów
i podobnych zjawisk: cząstka jest przesuwana w każdym kroku w losowo wybranym
kierunku, dla uproszczenia (w modelu dwuwymiarowym) przesunięcia są tylko
wzdłuż osi x lub osi y i zawsze mają jednostkową długość.


CC-BY-NC-ND 2021 Sławomir Marczyński
"""

from math import sqrt
import numpy as np
from random import randint
from turtle import *
import numpy as np
from matplotlib import pyplot as plt


LICZBA_SYMULACJI = 15  # ile razy cała symulacja ma być powtarzana
LICZBA_KROKÓW = 300000  # ile kroków ma być wykonanych w jednej symulacji
ANIMACJA=False  # False dla przyspieszenia obliczeń wyłącza rysowanie
SKALA = 10
PRĘDKOŚĆ_ŻÓŁWIA = 0

# Użyjemy tablic numpy. Tablice numpy są znacznie wygodniejsze i wydajnejsze
# w obliczeniach niż zwykłe listy.
#
suma_kwadratów_odległości = np.zeros(LICZBA_KROKÓW)

if ANIMACJA:
    speed(PRĘDKOŚĆ_ŻÓŁWIA)
    colormode(255)

for numer_symulacji in range(LICZBA_SYMULACJI):

    if ANIMACJA:
        color(randint(0, 255), randint(0, 255), randint(0, 255))
        up()
        home()
        down()

    x, y = 0, 0

    for numer_kroku in range(LICZBA_KROKÓW):

        kierunek = randint(1, 4)
        if kierunek == 1:
            x += 1
        elif kierunek == 2:
            x -= 1
        elif kierunek == 3:
            y += 1
        else:
            y -= 1
        if ANIMACJA:
            goto(SKALA * x, SKALA * y)
        kwadrat_odległości = x**2 + y**2
        suma_kwadratów_odległości[numer_kroku] += kwadrat_odległości

wykonane_kroki = np.arange(1, LICZBA_KROKÓW + 1)  # od włącznie, do wyłącznie
odległości = np.sqrt(suma_kwadratów_odległości / LICZBA_SYMULACJI)
teoretycznie = np.sqrt(wykonane_kroki)

# Rysowanie przeliczonych danych na ekranie
#
# plt.plot(wykonane_kroki, odległości,
#          wykonane_kroki, teoretycznie)
plt.loglog(wykonane_kroki, odległości,
           wykonane_kroki, teoretycznie)

plt.grid('minor')

plt.title('Błądzenie przypadkowe')
plt.xlabel('numer kroku')
plt.ylabel('pierwiastek z kwadratu średniej odległości')
plt.legend(('symulacja', 'teoria'))

plt.savefig('ilustracja.png', dpi=100)

plt.show()

if ANIMACJA:
    #end()
    exitonclick()
    #bye()
