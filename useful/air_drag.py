#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rzut ukośny - rozwiązanie problemu ruchu ciała w którym, oprócz ciężaru,
na ciało działa siła oporu powietrza.

Richard Feynman w swoim podręczniku sformułował taki problem: obliczyć jak
leci pocisk wystrzelony z dużą prędkością uwzględniając opór powietrza
zakładając że przy prędkości 300 metrów na sekundę ten opór jest dwukrotnie
większy niż ciężar pocisku.

Problem nie tylko w tym że równania ruchu są nieliniowe i mogą być trudne
do rozwiązania analitycznego. Kłopotliwe jest też w jaki sposób powietrze
stawia opór w czasie ruchu.

Podręcznikowo opór powietrza jest proporcjonalny do prędkości: dwa razy
szybciej porusza się ciało, dwa razy większa jest siła oporu. Ta prosta regułka
dobrze opisuje ruch odbywający się z małą prędkością, taki jak np. powolne
kołysanie się wahadła. Źródłem hamującej siły jest wtedy tarcie w warstwach
powietrza.

W rzeczywistości szybko poruszające się ciała (np. pociski karabinowe) raczej
napotykają opór proporcjonalny do kwadratu prędkości. Czyli dwa razy większa
prędkość to cztery razy większa siła oporu. Dlaczego? Powietrze nie nadąża
rozstąpić się przed pociskiem i (przynajmniej częściowo) jest rozpędzane do
prędkości pocisku. Wymaga to energii i stwarza siłę oporu.

Ale dlaczego napisaliśmy "raczej"? Bo areodynamika jest dużo bardziej złożona
niż możemy to tu wyjaśnić - przecież taki "szybki" pocisk będzie zwalniał,
więc choć początkowo poruszał się z kwadratowym oporem to może z biegiem czasu
zacząć poruszać się z oporem liniowym. Ba! Gdybyśmy nadali temu pociskowi
prędkość ponaddźwiękową to pojawiłyby się nowe zjawiska (opór falowy) i sprawy
skomplikowałyby się jeszcze bardziej. Nota bene, opór falowy był jeszcze
nieznany gdy w latach 50-tych XX stulecia próbowano oblatywać naddźwiękowe
samoloty - konstruktorzy nie wiedzieli dlaczego nie latają one tak, jak sobie
to obliczali (stosując niepełne wzory).

Program ilustruje metodę Eulera, będącą uproszczoną metodę różnic skończonych
(finite difference method, w skrócie FDM), choć w Pythonie biblioteka scipy
oferuje znacznie lepsze schematy numeryczne. Faktycznie, metoda Eulera niezbyt
jest efektywna, zwłaszcza ze stałym krokiem (tak jak będzie użyta), jednak
dzięki temu że rozwiązujemy dość stabilne równania (czyli łatwe do numerycznego
rozwiązania) i możemy użyć małej wartości kroku w czasie, obliczenia będą
wystarczająco dokładne i nie zajmować dużo czasu pracy komputera.

Uwaga: program celowo nie używa konwencji nazw przyjmowanej zwykle w Pythonie
       - dzięki temu oznaczenia są prawie takie same jakie stosowane są przez
       fizyków.

CC-BY-NC-Nd 2021 Sławomir Marczyński
"""

import math
import numpy as np
from matplotlib import pyplot as plt


# Używamy: prostokątnego układu dwóch współrzędnych (pomijamy siłę Coriolisa
# i fakt że Ziemia się obraca); jednostek SI (czyli kilogram, metr, sekunda);
# biblioteki numpy aby zwiększyć prędkość obliczeń oraz dlatego że dobrze
# współpracuje ona z biblioteką matplotlib.

t_end = 25  # czas sumulacji, sekundy
h = 0.001  # krok symulacji, sekundy
g = 9.81  # przyspieszenie grawitacyjne normalne, metry na sekundę kwadrat
m = 0.1  # masa ciała
coef = 2 * m * g / 300**2
alpha = math.radians(30)  # kąt w radianach (przeliczony ze 30 stopni)
v0 = 300  # prędkość początkowa w metrach na sekundę

def compute_acceleration(vx, vy):

    Px = 0  # ciężar ciała, składowa pozioma, niutony
    Py = - m * g  # ciężar ciała, składowa pionowa, niutony
    v = math.sqrt(vx**2 + vy**2)  # wartość prędkości (prędkość styczna)
    Q = coef * v**2  # wartość siły oporu powietrza, niutony
    Qx = - Q * vx / v  # składowa pozioma oporu powietrza, niutony
    Qy = - Q * vy / v  # składowa pionowa oporu powietrza, niutony
    Fx = Px + Qx  # wypadkowa siła, składowa pozioma
    Fy = Py + Qy  # wypadkowa siła, składowa pionowa
    ax = Fx / m  # przyspieszenie poziome, 2 zasada dynamiki Newtona
    ay = Fy / m  # przyspieszenie pionowe, 2 zasada dynamiki Newtona
    return ax, ay


t = np.arange(0, t_end, h)
n = len(t)
x = np.zeros(n)
y = np.zeros(n)
vx = np.zeros(n)
vy = np.zeros(n)
ax = np.zeros(n)
ay = np.zeros(n)

x[0] = 0
y[0] = 0
vx[0] = v0 * math.cos(alpha)
vy[0] = v0 * math.sin(alpha)
ax[0], ay[0] = compute_acceleration(vx[0], vy[0])

for i in range(1, n):
    x[i] = x[i - 1] + vx[i - 1] * h
    y[i] = y[i - 1] + vy[i - 1] * h
    vx[i] = vx[i - 1] + ax[i - 1] * h
    vy[i] = vy[i - 1] + ay[i - 1] * h
    ax[i], ay[i] = compute_acceleration(vx[i - 1], vy[i - 1])


plt.plot(x, y)
plt.grid()
plt.title('trajektoria')
plt.xlabel('x, metry')
plt.ylabel('y, metry')
plt.show()

plt.plot(t, m * np.sqrt(vx**2 + vy**2))
plt.grid()
plt.title('energia pocisku')
plt.xlabel('czas, sekundy')
plt.ylabel('energia, dżule')
plt.show()
