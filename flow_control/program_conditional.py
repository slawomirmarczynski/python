#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zastosowanie instrukcji warunkowej i wyrażenia warunkowego w języku Python.

Instrukcja warunkowa zapisywana jest przy pomocy słów kluczowych if, elif
i else. Te same słowa kluczowe są używane do tworzenia wyrażeń warunkowych.
Nie istnieje w Pythonie instrukcja switch (uznano ją za zbędną i była to dobra
decyzja).Oczywiste przykłady można znaleźć w podręcznikach do nauki Pythona,
tu jest parę trudniejszych i mniej oczywistych.

CC-BY-NC-ND 2021 Sławomir Marczyński
"""

import math  # funkcje matematyczne takie jak sin, cos i nie tylko
import random  # generowanie liczb pseudolosowych

a = random.randint(1, 10)  # przypadkowa liczba z przedział od 1 do 10 (włącznie)


# Instrukcji warunkowej zasadniczo nie pisze się w jednej linijce programu,
# bo chociaż to jest poprawne składniowo, to nie jest - w ocenie pythonistów
# - eleganckie.

if a > 0: print('A jest większe od zera'); print('sprawdziliśmy to')



# Jedna z "tych fajnych rzeczy w Pythonie" - naturalny zapis zamiast naużywania
# operatora and do sprawdzania czy wartość mieści się w zakresie.

if 0 < a < 10:
    print("wartość jest większa niż zero i mniejsza niż dziesięć")


# Czy można pominąć if i napisać tylko else? Niezupełnie tak, ale możemy
# spróbować użyć instrukcji pass w taki sposób jak poniżej.

if 0 < a < 10:
    pass
else:
    print("nieprawdą jest że wartość jest większa niż 0 i mniejsza niż 10")


# Uciekanie if-ów w prawo można zwykle ograniczyć przez użycie elif, warto też
# po prostu przemyśleć czy nie da się zręczniej zapisać takiego fragmentu
# programu niż powielając copy-paste instrukcje.
# Zobaczmy jak to wygląda z if-else

if a > 10:
    print('a jest większe niż dziesięć')
else:
    if a > 9:
        print('a jest większe niż dziewięć')
    else:
        if a > 8:
            print('a jest większe niż osiem')
        else:
            if a > 5:
                print('a jest większe niż pięć')

# a teraz z if-elif

if a > 10:
    print('a jest większe niż dziesięć')
elif a > 9:
    print('a jest większe niż dziewięć')
elif a > 8:
    print('a jest większe niż osiem')
elif a > 5:
    print('a jest większe niż pięć')

# i jeszcze raz to samo, ale w zupełnie innym stylu - zamiast wielu if'ów
# tylko jeden, za to osadzony wewnątrz pętli przeglądającej przygotowaną
# krotkę z wartościami do porównywania.

levels = (10, 'dziesięć'), ( 9, 'dziewięć'), ( 8, 'osiem'), ( 5, 'pięć')
for value, string in levels:
    if a > value:
        print('a jest większe niż', string)
        break


# W Pythonie jest tendencja do rezygnowania z else jeżeli to samo można
# osiągnąć prościej. Na przykład definicje funkcji foo1 i foo2 poniżej

def foo1(x):
    if x > 0:
        return 1
    else:
        return 2

def foo2(x):
    if x > 0:
        return 1
    return 2

# dają efektywnie to samo, choć w foo2() nie ma else.


# Zwykłe porównywanie liczb może niekiedy prowadzić do zadziwiających efektów.
# Wynikać może to z błędów zaokrągleń w obliczeniach i/lub porównywania z NAN,
# czyli symbolem nieoznaczonym not-a-number.

eps = 1.0E-30
if 1.0 + eps == 1.0:
    print('1.0 + eps to tyle samo co 1.0')

nan = math.nan
if nan > 0:
    print('większe')
elif nan < 0:
    print('mniejsze')
elif nan == 0:
    print('równe')
else:
    print('ani mniejsze, ani większe, ani równe zero')


# Dla liczb zmiennoprzecinkowych wskazane jest aby porównania przeprowadzać
# ostrożnie, uwzględniając możliwość błędów zaokrągleń i skończoną precyzję
# wyników. Funkcja math.isclose(), która do tego służy, jest dość skomplikowana
# - można używać jej z domyślnymi wartościami tolerancji lub dostroić.

value = 0.999999999999
print('value wynosi', value)
if value == 1.0:
    print('value jest równe dokładnie 1.0')
else:
    print('value nie jest równe dokładnie 1.0')

if math.isclose(value, 1.0):
    print('value jest niemal równe 1.0')


# Porównywać można nie tylko "zawartość" ale także identyczność (operator is)
# i nieidentyczność (operator is not) obiektów.

lista1 = [1, 2, 3]
lista2 = [1, 2, 3]

if lista1 == lista2:
    print('elementy list są jednakowe')

if lista1 is not lista2:
    print('choć listy są odrębnymi obiektami')


# Zamiast instrukcji warunkowej możemy używać wyrażenia warunkowego, przykład
# poniżej - rekurencyjna definicja silni. Lepiej jednak używać math.factorial()

def silnia(n):
    return n * silnia(n - 1) if n > 0 else 1


# Inne zastosowanie wyrażenia warunkowego - list comprehension:

lista = [k for k in range(1, 100) if k % 2 == 0 or k % 3 == 0]
print(lista)


# W Pythonie obliczanie, od lewej do prawej, wartości wyrażeń logicznych
# ogranicza się do tego co niezbędne aby uzyskać wynik (krótka ścieżka).
#
# Dlatego w poniższym przykładzie

short = foo1(100) < 0 and foo2(100) < 0

# nie zostanie w ogóle wywoływana funkcja foo2(), bo już sprawdzenie pierwszej
# nierówności da wynik False, więc wywołanie foo2(100) będzie przez to zbędne.
#
# Można to wykorzystać do warunkowego wykonania instrukcji bez pisania if, np.

def op1():
    print('wywołane jest op1');
    return True

def op2():
    print('wywołane jest op2');
    return True

(a > 5 and op1()) or op2()

# zamiast (bardziej czytelnego)

if a > 5:
    op1()
else:
    op2()


# Efekt osiągany użyciem if można także osiągnąć przez zastosowanie słowa
# kluczowego while, chociaż nie jest to być może oczywiste i intuicyjne:

while a > 5:
    print('a jest większe niż 5')
    break

# Zamiast break mogłoby być return albo w inny sposób przerwanie kolejnej
# iteracji (np. przez podstawienie a = 0).

# Jeszcze bardziej dziwacznym rozwiązaniem może być celowe wywołanie błędu
# aby uzyskać warunkowe wykonanie kodu:

try:
    b = 1 / (a - 5)
except:
    print('a jest równe 5')

# Tego rodzaju triki mogą działać, ale nie są dobrą praktyką programowania.


# Dobrą praktyką jest natomiast unikanie instrukcji warunkowych tam gdzie
# są zbędne, przykładowo fragment:

y = math.cos(a) if a > 0 else math.cos(-a)

# można zastąpić przez

y = math.cos(math.fabs(a))

# a najlepiej, ponieważ funkcja cosinus jest parzysta, przez

y = math.cos(a)


# W niektórych przypadkach instrukcję warunkową zastępuje się asercją, np.:

assert a >= 0

# sprawdzi czy a jest większe niż zero. Robi się tak po to aby w trakcie prac
# nad programem wyłapać błędy (takim błędem mogłaby być ujemna wartość a) bez
# konieczności dopisywania dodatkowego kodu wypisującego komunikat itd.
# Wszystkie asercje można wyłączyć włączając optymalizację w kompilatorze,
# a w ten sposób nieco zwiększyć prędkość działania programu gdy ten będzie już
# przekazany użytkownikom. Instrukcji if nie można wyłączyć, nie ma też
# w Pythonie takich rzeczy jak preprocesor znany z języka C dający możliwość
# określania które linijki kodu źródłowego mają być użyte a które pominięte
# przez kompilator.


# Python jest językiem obiektowym (OOP) i niezależnie od tego językiem mającym
# funkcje first class. Daje to możliwości zastępowania instrukcji warunkowej
# znacznie bardziej zaawansowanymi technikami, w tym opisanymi w doskonałym
# podręczniku "Design patters" (GoF). Wadą takich rozwiązań jest że mogą być
# mniej czytelne. Poniżej przykład złego użycia instrukcji warunkowej if oraz
# wskazówka jak zrobić to poprawnie.

def foo(a, b, switch):
    if switch == 1:
        return a * a - b * b * b
    else:
        return a * a * a - b * b

print(foo(5.1, 5.2, 1))
print(foo(-0.1, 0.01, 2))

# Jak widać funkcja foo wykonuje zupełnie różne obliczenia w zależności od tego
# jaka jest wartość parametru switch. Dzieje się to przez użycie wewnątrz niej
# instrukcji warunkowej if-else. Gdy jednak popatrzymy na to jak funkcja foo()
# jest używana to zauważymy że znacznie lepiej jest zdefiniować dwie różne
# funkcje takie jak foo1() i foo2()

def foo1(a, b):
    return a * a - b * b * b

def foo2(a, b):
    return a * a * a - b * b

print(foo1(5.1, 5.2))
print(foo2(-0.1, 0.01))

# a w ten sposób wyeliminować if-else a także uprościć program. Podobnie taki
# fragment jak poniżej:

for i in range(1, 5):
    if i == 1:
        # ... tu jakieś instrukcje
    elif 1 < i < 4:
        # ... tu jakieś instrukcje
    elif i == 4:
        # ... tu jakieś instrukcje

# Poprawnie należałoby napisać

    i = 1:
    # ... tu jakieś instrukcje
    for i in range(2, 4):
        # ... tu jakieś instrukcje
    i = 4:
    # ... tu jakieś instrukcje

# ewentualnie jeżeli i nie jest potrzebne to nawet jeszcze krócej, bez i = 1,
# bez i = 4.
