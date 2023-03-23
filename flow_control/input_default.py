#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przykład, pokazujący jak w języku Python współpracują funkcje, instrukcje
i wyrażenia warunkowe oraz pętle while.

Większość ciekawych (jeżeli ciekawią nas szczegóły implementacji) rzeczy
jest w module `input_default_module`, który jest w osobnym pliku. Dzięki
temu ta część programu, która jest poniżej, może pozostać prosta i czytelna.
Być może najtrudniejszym tu fragmentem jest ostatnia instrukcja, w której
print wypisuje tzw. f-string: tekst pomiędzy znakami cudzysłowu jest po
prostu napisem, w którym fragmenty w nawiasach klamrowych są ewaluowane
jako wyrażenia w Pythonie.

CC-BY-NC-ND 2023 Sławomir Marczyński
"""

import math

from input_default_module import input_int, input_float, input_str


n = input_int("liczba całkowita n", default=10)
x = input_float("liczba zmiennoprzecinkowa", default=math.pi)
s = input_str("napis", default="napis ćwiczebny")

print("n =", n)
print("x =", x)
print("s =", s)

print(f"{s}:  {n} * {x} = {n * x}")
