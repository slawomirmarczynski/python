#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dana jest lista list, czyli po prostu lista której elementami są listy, np.:

    L = [["tuleja", "popychacz"], ["panel", "przekładnia"],
         ["cięgno", "przekładnia"], ["zawór"]]

Każdy element tej listy to lista części które musiały być wymienione w czasie
kolejnej awarii. Czyli pierwsza naprawa wymagała wymiany tulei i popychacza,
druga panelu i przekładni itd. Napisz funkcję która na podstawie tego rodzaju
danych w odpowiedniej kolejności wypisze elementy ulegające awariom. Elementy
bardziej zawodne mają być wypisane na początku, elementy ulegające awariom
rzadziej na końcu. Przy każdym elemencie należy wypisać ile razy był wymieniany

CC-BY-NC-ND 2021 Sławomir Marczyński
"""


L = [["tuleja", "popychacz"],
     ["panel", "przekładnia"],
     ["cięgno", "przekładnia"],
     ["zawór"]]


def solution(reports):

    parts = {}
    for report in reports:
        for part in report:
            if part not in parts:
                parts[part] = 1
            else:
                parts[part] += 1
    replaced_parts_list = list(parts.items())
    sorted_replaced_parts_list = sorted(replaced_parts_list,
                                        key=lambda x: (x[1], x[0]),
                                        reverse=True)
    for name, count in sorted_replaced_parts_list:
        print(f'element {name:20} raportowano {count} razy')


solution(L)
