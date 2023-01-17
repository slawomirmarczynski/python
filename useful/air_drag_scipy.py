#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rzut ukośny - rozwiązanie problemu ruchu ciała w którym, oprócz ciężaru,
na ciało działa siła oporu powietrza. Wariant używający scipy i algorytmu RK4.

Problem fizyczny:

    Richard Feynman w swoim podręczniku sformułował taki problem: obliczyć jak
    leci pocisk wystrzelony z dużą prędkością uwzględniając opór powietrza
    zakładając że przy prędkości 300 metrów na sekundę ten opór jest dwukrotnie
    większy niż ciężar pocisku.

    Problem nie tylko w tym że równania ruchu są nieliniowe i mogą być trudne
    do rozwiązania analitycznego. Kłopotliwe jest też w jaki sposób powietrze
    stawia opór w czasie ruchu.

    Podręcznikowo opór powietrza jest proporcjonalny do prędkości: dwa razy
    szybciej porusza się ciało, dwa razy większa jest siła oporu. Ta prosta
    regułka dobrze opisuje ruch odbywający się z małą prędkością, taki jak np.
    powolne kołysanie się wahadła. Źródłem hamującej siły jest wtedy tarcie
    w warstwach powietrza.

    W rzeczywistości szybko poruszające się ciała (np. pociski karabinowe)
    raczej napotykają opór proporcjonalny do kwadratu prędkości. Czyli dwa razy
    większa prędkość to cztery razy większa siła oporu. Dlaczego? Powietrze
    nie nadąża rozstąpić się przed pociskiem i (przynajmniej częściowo) jest
    rozpędzane do prędkości pocisku. Wymaga to energii i stwarza siłę oporu.

    Ale dlaczego napisaliśmy "raczej"? Bo areodynamika jest dużo bardziej
    złożona niż możemy to tu wyjaśnić - przecież taki "szybki" pocisk będzie
    zwalniał, więc choć początkowo poruszał się z kwadratowym oporem to może
    z biegiem czasu zacząć poruszać się z oporem liniowym. Ba! Gdybyśmy nadali
    temu pociskowi prędkość ponaddźwiękową to pojawiłyby się nowe zjawiska
    (opór falowy) i sprawy skomplikowałyby się jeszcze bardziej. Nota bene,
    opór falowy był jeszcze nieznany gdy w latach 50-tych XX stulecia próbowano
    oblatywać naddźwiękowe samoloty - konstruktorzy nie wiedzieli dlaczego
    nie latają one tak, jak sobie to obliczali (stosując niepełne wzory).


Sposób rozwiązania:

    Program wykorzystuje do rozwiązywania równań różniczkowych zwyczajnych
    (ODE) z zadanymi warunkami początkowymi (IVP) zaawansowany algorytm
    adaptacyjny wykorzystujący metodę Runge-Kutty 4 rzędu i metodę Runge-Kutty
    5 rzędu (RK45).[1] Brzmi to jak coś bardzo trudnego, ale dzięki wywołaniu
    funkcji solve_ivp, jaka jest w bibliotece scipy, program staje się prostszy
    niż gdy samodzielnie rozpisujemy obliczenia używając stałokrokowej metody
    Eulera.

    RK45 to nie jest to kres możliwości solve_ivp, może ono wykorzystywać
    jeszcze inne algorytmy, ale zwykle RK45 wystarcza do praktycznych obliczeń,
    będąc czymś w rodzaju "industry standard" do rozwiązywania niekłopotliwych
    równań. Niektóre równania nie dają się jednak rozwiązać w ten sposób lub
    jeżeli otrzymuje się rozwiązania to bardzo niedokładne. Wtedy trzeba użyć
    innego "solvera", czyli po prostu w wywołaniu solve_ivp wybrać inny
    algorytm. Pomocne może być tzw. różniczkowanie od tyłu (BDF), czyli
    - w uproszczeniu - stosowanie metody różnic skończonych (FDM) nie dla
    przyrostów zmiennej niezależnej, ale dla jej spadków, niejako "wstecz
    w czasie".

    Ogólnie problemy rozwiązywania ODE mogą być nietrywialne i ich rozwiązanie
    może być bardzo trudne, a nawet niemożliwe. Z drugiej strony możliwość
    numerycznego rozwiązywania takich równań, zwłaszcza tych nie mających
    znanych rozwiązań analitycznych jest niezwykle ważna w inżynierii, gdyż
    tego rodzaju równania są modelem matematycznym wielu zjawisk i konstrukcji.



1. J. R. Dormand, P. J. Prince, "A family of embedded Runge-Kutta formulae",
   Journal of Computational and Applied Mathematics, Vol. 6, No. 1, pp. 19-26,
   1980.


CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import math
import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


# Używamy: prostokątnego układu dwóch współrzędnych (pomijamy siłę Coriolisa
# i fakt że Ziemia się obraca); jednostek SI (czyli kilogram, metr, sekunda);
# biblioteki numpy aby zwiększyć prędkość obliczeń oraz dlatego że dobrze
# współpracuje ona z biblioteką matplotlib.
#
# Dane takie jak poniżej można byłoby wprowadzać z konsoli funkcją input lub
# wczytywać z pliku, można byłoby dać programowi interfejs graficzny.
# Warto - zanim będziemy ulepszać program - zastanowić się czy rzeczywiście
# tego rodzaju ulepszenia, a przecież wymagające dodatkowego pracy programisty,
# są naprawdę potrzebne.

t_end = 10 * 60  # czas sumulacji, sekundy; to nie jest czas obliczeń!
h = 0.001  # krok symulacji, sekundy
g = 9.81  # przyspieszenie grawitacyjne normalne, metry na sekundę kwadrat
m = 0.01  # masa ciała
coef = 2 * m * g / 300**2
alpha = math.radians(30)  # kąt w radianach (przeliczony ze 30 stopni)
v0 = 300  # prędkość początkowa w metrach na sekundę


def dqdt(t, q):
    """
    Funkcja obliczająca pochodne dq/dt na jakie jest rozpisane równanie ODE.

    Parametry:
        t: czas, sekundy.
        q: zmienne zależne - kolejno współrzędna pozioma, współrzędna pionowa,
           pozioma składowa prędkości, pionowa składowa prędkości (jednostki SI
           odpowiednio metry i metry na sekundę).

    Zwraca:
        vx: prędkość pozioma.
        vy: prędkość pionowa.
        ax: przyspieszenie poziome.
        ay: przyspieszenie pionowe.

    """
    x, y, vx, vy = q
    v = math.sqrt(vx**2 + vy**2)  # wartość prędkości (prędkość styczna)
    Px = 0  # ciężar ciała, składowa pozioma, niutony
    Py = - m * g  # ciężar ciała, składowa pionowa, niutony
    Q = coef * v**2  # wartość siły oporu powietrza, niutony
    Qx = - Q * vx / v  # składowa pozioma oporu powietrza, niutony
    Qy = - Q * vy / v  # składowa pionowa oporu powietrza, niutony
    Fx = Px + Qx  # wypadkowa siła, składowa pozioma
    Fy = Py + Qy  # wypadkowa siła, składowa pionowa
    ax = Fx / m  # przyspieszenie poziome, 2 zasada dynamiki Newtona
    ay = Fy / m  # przyspieszenie pionowe, 2 zasada dynamiki Newtona
    return vx, vy, ax, ay


def hit_ground(t, q):
    """
    Funkcja decydująca kiedy przerwać obliczenia.

    Parametry:
        t: czas, sekundy.
        q: zmienne zależne - kolejno współrzędna pozioma, współrzędna pionowa,
           pozioma składowa prędkości, pionowa składowa prędkości (jednostki SI
           odpowiednio metry i metry na sekundę).

    Zwraca:
        y: współrzędna pionowa, czyli wysokość, w metrach; solve_ivp przerwie
           obliczenia w miejscu w którym y będzie równe zeru.
    """
    x, y, vx, vy = q
    return y


hit_ground.terminal = True  # przerwać obliczenia gdy hit_ground jest zero ale
hit_ground.direction = -1   # tylko wtedy gdy hit_ground zmienia się z + na -


q0 = 0, 0, v0 * math.cos(alpha), v0 * math.sin(alpha)

solution = solve_ivp(dqdt, (0, t_end), q0,
                     t_eval=np.arange(0, t_end, 0.1),
                     events=hit_ground,
                     first_step=0.0001, max_step=0.001)


# W zasadzie wszystko mamy już w solution, ale wygodniej będzie przepakować to
# do zmiennych mających łatwe do zrozumienia nazwy.

t = solution.t
x, y, vx, vy = solution.y
v = np.sqrt(vx**2 + vy**2)

# Obliczamy energie kinetyczną, potencjalną i całkowitą. Energia całkowita
# nie jest stała, bo układ nie jest zachowawczy - siła oporu powietrza hamując
# ruch powoduje przekazanie energii do powietrza wprawiając je w ruch,
# a ostatecznie wzrośnie temperatura i energia wewnętrzna powietrza.

E_kinetic = m / 2 * v**2  # klasyczny wzór, nierelatywistyczny, dżule
E_potential = m * g * y  # w pobliżu powierzchni Ziemii, dżule
E_total = E_kinetic + E_potential  # dżule

# Obliczamy drogę (wzdłuż trajektorii) przebytą przez ciało. Te obliczenia
# nie są bardzo dokładne, bo używamy uproszczonego algorytmu: zastępujemy
# łuki krzywej przez odcinki łamanej. Jeżeli wyniki mamy stablicowane dość
# gęsto to ewentualne błędy będą niewielkie.

dx = np.diff(x)  # obliczanie różnic pomiędzy elementami
dy = np.diff(y)  # obliczanie różnic pomiędzy elementami
ds = np.sqrt(dx**2 + dy**2)  # obliczanie długości odcinków, wz. Pitagorasa
s = np.cumsum(ds)  # cumsum jest (niemal) operacją odwrotną do diff
s = np.insert(np.cumsum(ds), 0, 0)  # dopisujemy 0 do s aby len(s) == len(t)


# Wykresy

plt.plot(x, y)
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
plt.grid()
plt.title('trajektoria')
plt.xlabel('x, metry')
plt.ylabel('y, metry')
plt.show()

plt.plot(t, E_kinetic, t, E_potential, t, E_total)
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
plt.grid()
plt.title('energia pocisku')
plt.xlabel('czas, sekundy')
plt.ylabel('energia, dżule')
plt.legend(('kinetyczna', 'potencjalna', 'całkowita'))
plt.show()

plt.plot(s, E_kinetic, s, E_potential, s, E_total)
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
plt.grid()
plt.title('energia pocisku')
plt.xlabel('przebyta droga, metry')
plt.ylabel('energia, dżule')
plt.legend(('kinetyczna', 'potencjalna', 'całkowita'))
plt.show()

plt.plot(s, v)
plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
plt.grid()
plt.title('prędkość pocisku')
plt.xlabel('przebyta droga, metry')
plt.ylabel('prędkość, metry na sekundę')
plt.show()
