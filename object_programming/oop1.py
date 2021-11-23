#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programowanie obiektowe - tworzenie nowego typu obiektów.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

# Obiekty są bytami mającym stan i behawior. W żargonie programistów używa się
# określeń pola, metody i składowe. Za stan obiektu odpowiadają pola, czyli po
# prostu zmienne powiązane z obiektem. Funkcje określone wewnątrz obiektu to
# metody i to one odpowiadają za zachowania obiektu czyli behawior. Wszystko
# razem - pola wraz z metodami - ma wspólną nazwę składowych.
#
# W żargonie pythonistów na składowe mówi się też atrybuty. Warto też pamiętać
# że Python jest językiem dynamicznym, więc w każdej chwili, jeżeli zechcemy,
# możemy modyfikować atrybuty obiektu. I że w Pythonie wszystko jest obiektem,
# nawet "zwykłe liczby", więc do wszystkiego możemy przypisywać atrybuty.


# -----------------------------------------------------------------------------

# Najpierw tworzymy klasę obiektów. Ta część jest zwykle dość pracochłonna,
# nawet jeżeli nie byłoby aż tyle komentarza (komentarz po # jest tu ekstra
# objaśnieniem dla początkujących).

class YesNoUnknown:
    """
    Klasa obiektów mogąca być określać odpowiedź jako tak, nie, niewiem.

    Zwykłe True/False nie nadaje się do tego, bo opisuje logikę z dwoma
    stanami, a nam jest potrzebna logika trójstanowa i jeszcze coś więcej...
    """

    # Definiowane wewnątrz klasy __init__() jest przez początkujących określane
    # konstruktorem. Doświadczeni pythoniści słusznie jednak nazywają tę metodę
    # inicjalizatorem, ponieważ to nie jest konstruktor, co wynika ze specyfiki
    # Pythona. Gdy tworzony jest nowy obiekt (w tym przypadku klasy
    # YesNoUnknown) najpierw jest wywoływany konstruktor (którego tu nie widać)
    # i tworzony jest obiekt jako taki, a następnie jest wywoływana metoda
    # __init__() czyli inicjalizator. Innym sposobem może być użycie tzw.
    # fabryk obiektów - także w Pythonie da się to zrobić.
    #
    # Tym razem __init__() jest nieskomplikowany - przepisuje wartość parametru
    # value na pole (zmienną podczepioną jako atrybut obiektu) self._value.
    # Znak podkreślenia na początku nazwy (po kropce) określa że self._value
    # jest chronione - tj. że nie może (nie powinno) być zmieniane nigdzie poza
    # metodami klasy w której jest zdefiniowane. Uwaga: klasy nie obiektu
    # - można odwoływać się z obiektu a do pola _value w innym obiekcie b
    # - byleby oba były tej samej klasy.
    #
    # Dynamiczność Pythona - pola obiektu są tworzone po prostu przez
    # przypisanie wartości - nie ma deklaracji, jakiejś specjalnej notacji.
    # Po prostu używa się self.nazwa_pola i już mamy. Przy tym self oznacza
    # "ten obiekt". Na upartego można zamiast self pisać this (jak w innych
    # językach), ale obyczaj nakazuje pisać self (IDE odwdzięczy się
    # pokolorowaniem przez analizator składni).

    def __init__(self, value=None):
        self._value = value

    # Rzecz w programowaniu obiektowym dość typowa: metoda przekształcająca
    # obiekt na czytelny dla człowieka napis. To samo w Javie robi się metodą
    # toString(). W Pythonie zarezerwowana jest do tego "magiczna metoda"
    # (czyli specjalnego przeznaczenia, wyróżniona przez po dwa znaki
    # podkreślenia na początku i na końcu) __str__().

    def __str__(self):
        if self._value is None:
            return 'unknown'
        elif self._value:
            return 'yes'
        else:
            return 'no'

    # Trzy funkcje "gettery" (prawidłowa polska "gettera" nazwa to akcesor)
    # których zadaniem jest dostarczyć prostych odpowiedzi. Zwykle takie
    # funkcje (zwłaszcza w Javie) mają nazwę zaczynającą się od get, chyba że,
    # tak jak tutaj, mają zwracać wartości logiczne prawd/fałsz. Wtedy używa
    # się is, czyli np. is_true.

    def is_true(self):
        if self._value is None:
            return False
        else:
            return self._value

    def is_false(self):
        if self._value is None:
            return False
        else:
            return not self._value

    def is_unknown(self):
        if self._value is None:
            return True
        else:
            return False

    # Kolejne funkcje to "settery" (poprawnie mutatory), które pozwalają
    # zmieniać stan obiektów klasy jaką właśnie tworzymy.
    #
    # Uwaga: użycie akcesorów i mutatorów nie zawsze jest najlepszym pomysłem
    # w Pythonie, czasem znacznie wygodniej jest po prostu wprost odwoływać się
    # do atrybutu (czyli pola) obiektu. Dlaczego tym razem używamy takich
    # get/set? Aby mieć pewność że przez przypadek wartość self._value
    # nie będzie inna niż jedna z trzech możliwych: True, False, None.

    def set_false(self):
        self._value = False

    def set_true(self):
        self._value = True

    def set_unknown(self):
        self._value = None


# -----------------------------------------------------------------------------

# Teraz jest ta łatwiejsza i przyjemniejsza część programu - tworzenie obiektóW
# i ich używanie do tego do czego są nam potrzebne - tym razem jest to jakiś
# taki nie najlepszy i nieco źle zaimplementowany algorytm zgadywania czy
# trafiliśmy na liczbę pierwszą. Po prostu próbujemy dzielić przypadkową liczbę
# - jeżeli jest większa niż 100 - przez przypadkowe dzielniki (nie większe niż
# połowa tej liczby i większe niż - jeżeli jest podzielna to na pewno nie jest
# liczbą pierwszą. Natomiast jeżeli jest mniejsza lub równa 100 - dzielimy ją
# przez wszystkie liczby mniejsze od niej i większe niż 2. To naprawdę niezbyt
# dobry algorytm, ale chcemy tu tylko zilustrować możliwości naszej klasy.


import random

M = 1000
N = 1000

n = random.randint(2, M)
result = YesNoUnknown()

if n > 100:
    for i in range(N):
        if n % random.randint(2, M // 2) == 0:
            result.set_false()
            break
else:
    for k in range(2, n // 2):
        if n % k == 0:
            result.set_false()
            break
    else:
        result.set_true()

print(f'n = {n}  result of the test: {result}')
