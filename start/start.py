#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program w języku Python 3, wypisujący "Hello World", nieco bardziej
skomplikowany, bo ma tzw. shebang (dwie pierwsze linie komentarza zawierające
wskazówkę że program jest napisany w Pythonie 3 i określające sposób kodowania
znaków w pliku źródłowym jako utf-8) oraz instrukcję warunkową rozpoznającą
czy został uruchomiony jako program (wtedy zmienna __main__ zawiera napis
'__main__'), czy może załadowany jako biblioteka (wtedy w zmiennej __main__
byłoby 'program2'). Jak widać w programie są teraz komentarze.

W praktyce: shebang nie jest konieczny, zwłaszcza jeżeli nie używamy Linuksa
lub Uniksa; kodowanie znaków i tak domyślnie jest przyjmowane jako utf-8 (czyli
także ASCII, bo pliki z kodowaniem ASCII są zgodne z uft-8); rozpoznawanie czy
moduł w Pythonie jest lub nie jest załadowany jako biblioteka nie przyda się
nam jeżeli i tak nie będziemy używali go jako biblioteki.
"""

if __name__ == '__main__':
    print('hello')
