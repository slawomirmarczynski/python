#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Błądzene przypadkowe.

Błądzenie przypadkowe (random walking) jest uproszczonym modelem dyfuzji gazów
i podobnych zjawisk: cząstka jest przesuwana w każdym kroku w losowo wybranym
kierunku, dla uproszczenia (w modelu dwuwymiarowym) przesunięcia są tylko
wzdłuż osi x lub osi y i zawsze mają jednostkową długość.

Program, w tej wersji, ma dość niekonsekwentną strukturę - używa grafiki żółwia
(moduł turtle) do rysowania trajektorii cząstki, ale to biblioteka matplotlib
jest użyta do rysowania wykresu zależności średniej odległości po k krokach.
Podobnie w programie używane są listy wspórzędnych, a mogłyby być od razu użyte
wektory z biblioteki numpy (które świetnie współpracują z matplotlib). Wszystko
to wynika z chęci pokazania jak nawięcej technik możliwych do użycia z Pythonem
i jednocześnie zminimalizowania wysiłku programisty.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

from math import sqrt
from random import randint
from turtle import *
from matplotlib import pyplot as plt


LICZBA_SYMULACJI = 25  # ile razy cała symulacja ma być powtarzana
LICZBA_KROKÓW = 100000  # ile kroków ma być wykonanych w jednej symulacji
ANIMACJA=False  # False dla przyspieszenia obliczeń wyłącza rysowanie
SKALA = 10
PRĘDKOŚĆ_ŻÓŁWIA = 0

# Tworzymy listę, same zera, ale odpowiednio długą aby potem, w pętli, zbierać
# do niej dane z poszczególnych kroków symulacji.
# Odległości będą liczone od punktu o współrzędnych (0, 0).
#
suma_kwadratów_odległości = [0] * LICZBA_KROKÓW

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

wykonane_kroki = [0] * LICZBA_KROKÓW
odległości = [0] * LICZBA_KROKÓW
for numer_kroku in range(LICZBA_KROKÓW):
    wykonane_kroki[numer_kroku] = numer_kroku + 1
    odległości[numer_kroku] = sqrt(suma_kwadratów_odległości[numer_kroku] / LICZBA_SYMULACJI)

# Rysowanie przeliczonych danych na ekranie
#
plt.plot(wykonane_kroki, odległości)
plt.show()

if ANIMACJA:
    #end()
    exitonclick()
    #bye()
