#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Porównanie różnych algorytmów sortowania.

Algorytmy sortowania były modnym tematem w latach 70-tych. Obecnie nie ma zwykle
potrzeby implementować ich samodzielnie - Python ma funkcję sorted potrafiącą
posortować niemal wszystko, można też używać dla list metody sort.

Dlaczego więc?

1. Aby pokazać jak wyglądają "klasyczne" algorytmy sortowania.
2. Aby móc sprawdzić na testowych danych jaka jest wydajność tych algorytmów
   i porównać ją z tym co oferuje funkcja sorted() z biblioteki standardowej.

Uwaga:

    Program wykorzystuje standardowy w Pythonie generator liczb pseudolosowych,
    tzw. Mersenne Twister. Jest to bardzo dobry generator, lepszy niż stosowany
    w bibliotece standardowej języka C rand, ale ani nie generuje prawdziwych
    liczb losowych, ani nie jest bezpieczny w sensie kryptograficznym.

CC-BY-NC-ND 2022 Sławomir Marczyński
"""

import random


def generate_test_data(n=100, low=1, high=100):
    """
    Generowanie danych testowych.

    Dane testowe mają postać listy liczb.

    Parametry:

        n (int): ilość danych do wygenerowania, powinna być większa niż 0
        low (int): najmniejsza liczba jaka może być wygenerowana
        high (int): największa liczba jaka może być wygenerowana

    Zwraca:

        listę n liczb z przedziału od low do high
    """

    # To samo można napisać krócej, ale być może w mniej zrozumiały sposób::
    #
    #   return [random.randint(low, high) for i in range(N)]
    #
    # czyli używając tzw. list comprehension.
    #
    # Rozwiązanie poniżej - ze zwykłą pętlą for i dopisywaniem kolejnych
    # wartości przez append jest nieco dłuższy - działa równie dobrze.
    #
    test_data = []
    for i in range(n):
        value = random.randint(low, high);
        test_data.append(value)
    return test_data


def insertion_sort(a):
    """
    Sortowanie listy a algorytmem sortowanie przez wstawianie (insertion sort).

    Insertion sort polega na przesuwaniu elementów w lewo z rozpychaniem danych
    w prawo. W najgorszym razie musimy przesunąć N elementów za każdym razem
    przesuwając średnio N/2 elementów w prawo, co daje koszt czasowy, inaczej
    time complexity, równy O(N**2). Algorytm jest stabilny, tzn. nie przestawia
    elementów jeżeli są już posortowane.
    """
    n = len(a)
    for i in range(n):
        element = a[i]
        j = i
        while a[j - 1] > element and j:
            a[j] = a[j - 1]
            j -= 1
        a[j] = element
    return a


def selection_sort(a):
    """
    Sortowanie przez wybieranie (selection sort).

    Selection sort polega na wybieraniu kolejnych elementów od lewej i zamianie
    ich przez element po prawej (jeżeli jest mniejszy, sprawdzane są wszystkie).
    Odmianą tego algorytmu jest wybieranie od prawej i zamiana przez większy.
    Można te dwa warianty połączyć. Algorytm jest niestabilny - tzn. wielokrotne
    sortowanie może przestawiać już posortowane elementy. Koszt O(N**2).
    """
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
    return a


def bubble_sort(a):
    """
    Sortowanie bąbelkowe (bubble sort).

    Przechodzimy przez listę elementów wiele razy, za każdym razem zamieniając
    kolejność sąsiednich elementów jeżeli są w złej kolejności. Przestajemy gdy
    kolejność wszystkich jest dobra. Złożoność jest O(N**2), stabilny.
    W praktyce jest to gorszy algorytm niż insertion sort, jedyne sensowne
    zastosowanie to poprawianie uporządkowania prawie uporządkowanych danych
    (tj. takich że zamieniona jest kolejność dwóch sąsiednich elementów).
    """
    n = len(a)
    run = True
    while run:
        run = False
        for i in range(1, n):
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                run = True
    return a


def quick_sort(a):
    """
    Sortowanie szybkie (quicksort).

    Sortowanie szybkie jest zwykle szybkie, tzn. ma koszt O(N*log(N)), ale...
    dla złośliwie spreparowanych danych może mieć koszt O(N**2). Cały wic w tym
    jak dobieramy wartość pivot - jeżeli uda nam się trafić tak aby left i right
    były mniej więcej jednakowej długości, to dobrze. Wybór wartości pivot można
    rozwiązać inaczej niż pokazane jest to poniżej. Zwykle "quicksort" jaki
    możemy znaleźć w bibliotekach (np. w języku C) ma udoskonalenia, np. łączyć
    w sobie sortowanie szybkie i sortowanie przez wstawianie. Piękno algorymu
    zawiera się w rekurencji, a to oznacza że (naiwna) implementacja nie jest
    zgodna ze standardem MISRA i nie jest zalecana przez NASA dla statków
    kosmicznych. Po prostu w patologicznych przypadkach posortowanie iluś tam
    tysięcy liczb doprowadzi do iluś tam tysięcy zagnieżdżonych wywołań
    rekurencyjnych, a to doprowadzić do przepełnienia stosu, czyli katastrofy.

    Niestabilny, przestawia kolejność już posortowanych elementów.
    """
    n = len(a)
    if n < 2:
        return a
    pivot = a[0]
    remains = a[1:]
    left = [element for element in remains if element <= pivot]
    right = [element for element in remains if element > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


data = generate_test_data(20)
for alg in insertion_sort, selection_sort, bubble_sort, quick_sort, sorted:
    print(alg(data))
