#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lista jako spis rzeczy różnych.

W wielu językach programowania podstawową techniką zapamiętania wielu wartości
pod jedną nazwą jest umieszczenie ich w tablicy. W Pythonie są tablice jakieś
"zwykłe tablice", ale praktycznie nikt ich nie używa, bo prawie zawsze zamiast
nich stosuje się listy, albo struktury takie jak wektory i macierze jakie są
w bibliotece numpy (NUMerical PYthon), ewentualnie inne odpowiednie struktury
danych, w tym krotki, zbiory, słowniki.

Uwaga: ponieważ potrzebne będą dane do demonstracji jak działają listy, to
przyda się moduł random, dzięki któremu możemy generować liczby losowe oraz
używać ich w rozmaity sposób (np. do losowego wybierania elementóW, tasowania).

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import random


# Listę można zapisać wprost, podając jej elementy wewnątrz nawiasów []

list1 = [1, 2, 3, 4, 22]

# Nie ma konieczności nazywania listy list1 czy w podobny sposób. Nie wolno
# jednak użyć samego list, bo samo słowo list jest zarezerwowane. Lista może
# więc nazywać sie np. list1, a, b, random_numbers itp. itd.

a = [1, 2, 3]
b = [1, 10, 100, 1000]


# Podanie wszystkich elementów elementów jako literałów (czyli wypisując jawnie
# wartości jak powyżej) jest tylko jednym sposobem tworzenia listy.
#
# Inną jest przekształcenie czegoś co listą nie jest na listę, np. zbiór si
# może być z łatwością przekształcony na listę li:

si = {'raz', 'dwa', 'trzy'}
li = list(si)
print(li)

# Problemem dla początkujących może być przekształcanie słownika na listę.
# Gdy to robimy możemy dostać listę wyłączne kluczy, aby otrzymać listę par
# (klucz, wartość) trzeba się trochę postarać:

di = {1: 'raz', 2: 'dwa', 3: 'trzy'}
li1 = list(si)
li2 = list(di.items())
print(li1)
print(li2)


# Bardzo często najpierw tworzy się pustą listę i dopiero potem dopisuje się
# do niej kolejne wartości wywołując append. Poniżej jest tak utworzona lista
# 10 liczb losowych. Listę pustą można tworzyć albo za pomocą nawiasów [],
# albo używając list() w miejscu nawiasów [].

random_values = []
for k in range(10):
    random_values.append(random.random())

# Skrócona forma to tzw. list comprehension - zapis w którym pętla for wchodzi
# niejako do nawiasów definiujących listę. Tu przykład jak użyć tego aby zrobić
# listę 10 przypadkowych liczb:

random_values = [random.random() for k in range(10)]


# Elementy listy mogą być rozmaite, niekoniecznie muszą to być liczby całkowite
# - mogą to być też liczby zmiennoprzecinkowe, napisy będące ciągam znaków,
# funkcje, inne listy itd.

weird = [1, 'Ala ma kota', 3.14, [], ['tamta lista była', 'pusta']]


# Do elementów listy możemy uzyskać dostęp podobnie jak do elementów tablic
# w innych językach programowania. Podobnie jak w języku Matlab można wybierać
# fragment listy podając zakres indeksów oddzielony przecinkiem. Ujemne indeksy
# oznaczają numerację elementów od końca listy.

print('pierwszy element', weird[0])
print('drugi element', weird[1])
print('trzy ostatnie elementy', weird[-3:])


# Wygoda stosowania list nie ogranicza się do tego że nie trzeba podawać ich
# rozmiaru i że łatwo dopisywać kolejne elementy. Po prostu listy są obiektami
# klasy list, a przez to można na nich wykonywać różne operacje.
#
# Proste przykłady to użycie print z listą i określenie długości listy:

print(random_values)
n = len(random_values)
print('liczba elementów =', n)

# Podobnie nietrudne jest sortowanie listy, odwracanie kolejności elementów,
# wyciąganie z listy ostatniego elementu (operacja odwrotna do append).

print(sorted(random_values))
print(random_values.reverse())
print(random_values.pop())

# Średnio zaawansowane to np. liczenie ile razy wystąpił dany element, lub
# jaki ma numer na liście (pierwszy element ma numer 0, drugi 1 itd.)

print(weird.count(3.14))
print(weird.index(3.14))

# Bardziej skomplikowane to np. wyszukiwanie liczby elementów jakie spełniają
# kryterium używając wyrażenia lambda i filtrowania:

print(len(list(filter(lambda x: x > 0.5, random_values))))

# Operacji na listach jest naprawdę sporo (w tym takie jak znajdowanie
# najmniejszego lub największego elementu, sumowanie itd.), spis wszystkich
# jest w referencyjnej dokumentacji do Pythona.


# W Pythonie szczególnie często używa się tzw. krotek (po angielsku tuples),
# które od list różnią się tym że nie mogą być modyfikowane. Nie oznacza to
# że nic się nie da zmienić, ale raczej że jeżeli coś chcemy zmienić to możemy
# to zrobić tylko tworząc nową krotkę.

first = (2, 3, 'punkt A')
first = (2.5, 3, 'punkt A')

# Zmienna first najpierw była krotką zawierającą jako pierwszy element 2,
# potem jednak utworzyliśmy nową krotkę i tę nową krotkę teraz trzymamy w first
# - gdyby to była lista, to moglibyśmy zrobić to tak:

first = [2, 3, 'punkt A']
first[0] = 2.5

# Ale ponieważ użyliśmy krotek to musieliśmy utworzyć całą nową krotkę,
# ewentualnie moglibyśmy żonglować tak jak poniżej:

first = (2, 3, 'punkt A')
first = list(first)
first[0] = 2.5
first = tuple(first)

# choć to zupełnie nieopłacalne - przekształcanie krotki w listę i na odwrót
# listy w krotkę można uznać za bezcelowe, bo łatwej użyć tylko listy.


# Pojawia się więc pytanie: po co używać "gorszych list" będących krotkami,
# skoro zasadniczo listy są w stanie zastąpić krotki i mogą jeszcze więcej?!
#
# Uzasadnieniem jest możliwość poinformowania kompilatora Pythona o tym że
# możliwe są pewne optymalizacje, a co więcej - zwykle ta niezmienność krotek
# nie jest w ogóle problemem.
#
# Przykładowo mamy funkcję która ma zwracać dwie rzeczy - liczbę jedynek
# i liczbę zer w łańcuch znaków. Łatwo to zrobić używając krotki (ew. listy)
# - po prostu funkcja zwróci krotkę dwuelementową.

def bdc(s):
    return s.count('1'), s.count('0')

# Zwróćmy uwagę że krotka jest napisana bez nawiasów () - pisząc krotkę można
# nie pisać nawiasów jeżeli to nie prowadzi do nieporozumień.


# Innym zastosowaniem krotek jest pakowanie/rozpakowywanie danych, na przykład
# mając adres (będący łańcuchem znaków) i numer portu (liczbę) można spakować
# je razem jako jedną krotkę:

FULL_ADDRESS = 'localhost', 80

# a nawet użyć krotki do czegoś takiego

a, b, c, d = 1, 2, 3, 4


# Klasycznym pythonowskim sposobem na zamianę wartości w zmiennych jest użycie
# krotki - da się to zrobić w jednej linijce i to bez tymczasowej zmiennej:

a, b = b, a


# W zasadzie na krotkach działają prawie wszystkie operacje jakie działają
# na listach, choć nie zawsze rezultatem będą krotki. Na przykład wywołując

print(sorted((1, 3, 2, 0)))

# zobaczymy że po sortowaniu będziemy mieli listę, a nie krotkę. Oczywiście
# nie zadziałają operacje modyfikujące krotkę (pamiętajmy krotki są immutable).
