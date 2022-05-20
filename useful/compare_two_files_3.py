#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Porównywanie zawartości dwóch plików ignorujące znaki specjalne.

Chcemy porównać czy dwa pliki tekstowe zawierają taką samą treść. Dopuszczamy
różnice takie jak dodatkowe spacje czy zmiany linii, ale litery muszą być takie
same. Pliki uznać chcemy także za różne jeżeli w jednym z nich będzie napisane
"tak samo", a w drugim "taksamo" (bez spacji pomiędzy wyrazami).

Rozwiązanie "pythoniczne", czyli takie w którym wykorzystujemy regex'y oraz
specyficzne cechy języka Python aby program był prosty, czytelny i zwięzły.

Uwaga: program nie będzie działał prawidłowo jeżeli nie będzie plików z danymi,
albo jeżeli te pliki będą zbyt duże i nie będą mogły zmieścić się w pamięci RAM
Nie oznacza to że napisanie programu który porównuje ze sobą pliki np. 1000
terabajtowe jest niewykonalne. Po prostu tworząc nasz program zakładaliśmy że
ma być maksymalnie prosty (bez dodatkowych zabezpieczeń, interfejsu graficznego
itp. udogodnień) i że maksymalna wielkość plików będzie wynosiła kilkanaście
megabajtów przy dostępnej pamięci RAM rzędu jednego gigabajta.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import re

# Definicje stałych globalnych
#
# Rozwiązanie prowizoryczne - zamiast pozyskiwać nazwy plików po uruchomieniu
# programu - nazwy plików są zapisane wprost w programie.
#
FILE_NAME1 = 'plik1.txt'
FILE_NAME2 = 'plik2.txt'

# Takie same operacje wykonywane więcej niż raz najlepiej zapisać jako funkcje
# (w Pythonie funkcje i procedury to to samo). Nawet jeżeli ciąg istrukcji jest
# tylko raz używany - ale ma określone działanie, służy konkretnemu celowi
# - to i tak sensowne jest zapisanie go jako funkcji.


def read_text(file_name):
    """
    Wczytywanie danych.

    Czytanie całej zawartości pliku tekstowego na raz. Wszystkie ciągi spacji,
    znaków nowego wiersza lub tabulacji są zamieniane na pojedyncze spacje.

    Parametry:
        file_name (łańcuch znaków): nazwa pliku jaki ma być przeczytany.

    Zwraca:
        text (łańcuch znaków): przeczytana i znormalizowana zawartość pliku.
    """
    # Zamiast używać open-close lepiej jest użyć konstrukcji z with.

    with open(file_name) as file:
        text = file.read()

    # Wyszukiwanie i zamiana ciągów białych znaków? Najprościej zrobić to
    # używając standardowej biblioteki re, czy wyrażeń regularnych (regular
    # expression). W ten sposób da się to zrobić w jednej linijce.
    #
    # re.sub(wzorzec, zamiennik, tekst) działa tak że wyszukuje w tekście
    # tekst fragmentow pasujących do wzorca i zamienia je na zamiennik.
    # Wzorzec zapisuje się podając jakie znaki mają być rozpoznane. Można przy
    # tym używać specjalnych kodów: kropka oznacza dowolny znak, \d dowolną
    # cyfrę od 0 do 9, \w literę, \s jakikolwiek biały znak, + określa że
    # dopasowanie ma być do przynajmniej jednego lub więcej wystąpienia itp.
    # Pełny opis jest dostępny https://docs.python.org/3/howto/regex.html,
    # pomocna może też być jedna z wielu stron internetowych umożliwiająca
    # działania on-line, np.: https://regex101.com/
    #
    # Dlaczego regex'y (regular expression, wyrażenia regularne) warto poznać?
    # Bo są użyteczne, względnie łatwe w użyciu i można je stosować nie tylko
    # w Pythonie, ale także w wielu innych językach programowania.
    #
    # Uwaga: trzy linijki poniżej można zmieścić w jednej, po prostu
    #
    #           return re.sub(r'\s+', '*', text.strip())
    #
    # ale kod źródłowy programu, choć krótszy, nie będzie bardziej czytelny.
    #
    # Warto też zauważyć że używamy raw-string'u gdy piszemy r'abcd' zamiast
    # zwykłego łańcucha 'abcd'. W zwykłym łańcuchu znak backslash (ukośnika
    # odwrotnego), ma specjalne znaczenie jako część zapisu znaku kontrolnego.
    # W raw-string'u backslash to po prostu taki sam znak jak każdy inny.
    # Dlatego gdybyśmy nie użyli litery r jako przedrostka to musielibyśmy
    # napisać return re.sub('\\s+', '*', text.strip()), tj. użyć dwóch znaków
    # backslash zamiast jednego. Podstawowe znaki kontrolne jakie można uzyskać
    # pisząc backslash to znak tabulacji \t oraz znak nowej linii \n.

    text = text.strip()  # usuwanie początkowych i końcowych białych znaków
    text = re.sub(r'\s+', '*', text)  # zamiana ciagu białych znaków na spację
    return text


# Główna część programu w której zaczyna coś się dziać.

text1 = read_text(FILE_NAME1)
text2 = read_text(FILE_NAME2)

# Teraz wystarczy tylko zwykłe porównanie

if text1 == text2:
    print('pomijając nieistotne różnice pliki są takie same')
else:
    print('pliki są istotnie różne')
