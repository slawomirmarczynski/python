#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Samochód może zabrać pewną liczbę przesyłek, ale tak aby ich łączna masa
nie przekraczała ustalonej wartości m = 200 kg. Rozmiar przesyłek jest
niewielki i nie ma znaczenia dla rozwiązania. Przesyłki są opisane jako lista
krotek (nazwa, masa), gdzie nazwa oznacza kod przesyłki a masa masę przesyłki,
przykładowo:

  L = [("A01X", 30), ("C31T", 250), ("W-345", 14), ("QQN", 110), ("A01X", 20),]

Napisz funkcję, która poda (jako listę zwracaną przez return) jakie przesyłki
należy załadować do samochodu aby przewieźć ich możliwie jak najwięcej już za
pierwszym razem. Napisz program który przetestuje tę funkcję i wypisze czy
wszystkie przesyłki można przewieźć w jednym kursie, czy może niektórych
przesyłek nie da się załadować.

Podana lista jest przykładowa, funkcja powinna działać z różnymi danymi.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""


L = [("A01X", 30), ("C31T", 250), ("W-345", 14), ("QQN", 110), ("A01X", 20)]


def solution(parcels, weight_limit=200):
    sorted_parcels = sorted(parcels, key=lambda x: x[1])
    parcels_to_take = []
    total_weight = 0
    for parcel in sorted_parcels:
        name, weight = parcel
        if total_weight + weight <= weight_limit:
            total_weight += weight
            parcels_to_take.append(parcel)
        else:
            break
    return parcels_to_take


cargo = solution(L)

print(L)
print(cargo)
if len(L) == len(cargo):
    print(f"tak, wszystkie {len(L)} przesyłki można przewieźć od razu")
else:
    print(f"nie, można przewieźć tylko {len(cargo)} przesyłek z {len(L)}")
