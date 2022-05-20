#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Obliczanie regresji liniowej - przykład użycia bibliotek numpy i scipy
do obliczeń oraz matplotlib do rysowania.

Python jest łatwym do nauczenia się językiem, a dzięki bibliotekom można
efektywnie wykonywać w nim nawet skomplikowane obliczenia. Biblioteka numpy,
przeznaczona do obliczeń na wektorach i macierzach, może z powodzeniem
rywalizować z Matlabem (Matlab jest programem komercyjnym, numpy jest darmowe).
Biblioteka scipy uzupełnia numpy, my z niej importujemy tu moduł stats.
Matplotlib jest biblioteką, dzięki której można w Pythonie łatwo narysować
wykresy, mającą funkcjonalność zbliżoną (a nawet większą) do możliwości
graficznych Matlaba.

CC-BY-NC-ND 2017, 2021 Sławomir Marczyński
"""

import math
import matplotlib.pyplot
import numpy
from scipy import stats


# Krótkie wprowadzenie do tego co robi program

print()
print('Obliczanie regresji liniowej')
print()


# Czytanie danych

DATA_FILE_NAME = 'linear_regression_data.txt'
print('dane są czytane z pliku', DATA_FILE_NAME)
x, y = numpy.loadtxt(DATA_FILE_NAME, unpack=True)


# Obliczanie współczynników regresji y = a * x + b

n = len(x)

CONFIDENCE = 0.95
tcoeff = stats.t.ppf(CONFIDENCE, n - 2)
print('poziom ufności = ', CONFIDENCE * 100.0, '%')
print('współczynnik Studenta = ', tcoeff)

a, b, r, p_value, da = stats.linregress(x, y)
da = tcoeff * da
db = da * math.sqrt(numpy.sum(x**2) / n)

print('a = {:.4} ± {:.2}  ({:.4}%)'.format(a, da, da/math.fabs(a) * 100.0))
print('b = {:.4} ± {:.2}  ({:.4}%)'.format(b, db, db/math.fabs(b) * 100.0))
print('r =', r)
print('p-value =', p_value)


# Obliczanie dopasowanych krzywych

NPTS = 500
x1 = numpy.min(x)
x2 = numpy.max(x)
little_more = (x2 - x1) * 0.10
x1 = x1 - little_more
x2 = x2 + little_more
x_step = (x2 - x1) / (NPTS - 1)

xi = numpy.linspace(x1, x2, NPTS)
yi = a * xi + b
var = numpy.var(x, ddof=1)
delta_conf = da * numpy.sqrt(var + (xi - numpy.mean(x))**2)
delta_pred = da * numpy.sqrt((n - 1) * var + (xi - numpy.mean(x))**2)
yi_conf_lo = yi - delta_conf
yi_conf_hi = yi + delta_conf
yi_pred_lo = yi - delta_pred
yi_pred_hi = yi + delta_pred


# Rysowanie wykresów

matplotlib.pyplot.plot(xi, yi, 'r-',
                       xi, yi_conf_lo, 'g--',
                       xi, yi_pred_lo, 'c:',
                       xi, yi_conf_hi, 'g--',
                       xi, yi_pred_hi, 'c:',
                       x, y, 'bo')
matplotlib.pyplot.grid()
matplotlib.pyplot.title('Regresja liniowa')
matplotlib.pyplot.xlabel('zmienna niezależna')
matplotlib.pyplot.ylabel('zmienna zależna')
matplotlib.pyplot.show()
