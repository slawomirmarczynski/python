#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Przykład, pokazujący jak w języku Python współpracują funkcje, instrukcje
i wyrażenia warunkowe oraz pętle while.

Moduł z procedurami tworzący małą biblioteczkę funkcji znakomicie
upraszczającymi osiągnięcie założonego celu: umożliwienia wprowadzania
domyślnych wartości podpowiadanych w czasie interaktywnej współpracy z
użytkownikiem.

Jest tu użyty pomysł architektoniczny: zamiast tworzyć (być może pomagając
sobie techniką copy-paste) wiele bliźniaczo podobnych funkcji... jest
tworzona jedna funkcja, którą można jednakże tak skonfigurować, aby mogła
obsłużyć różne przypadki. Dla uniknięcia nadmiernej komplikacji tworzymy
też fasadowe funkcje o oczywistych nazwach, mających proste parametry.
Funkcje te jednak nie wykonują same pracy, a jedynie przekazują ją do funkcji
implementującej. W ten sposób program jest krótszy, unika się powielania kodu
(efektu copy-paste), łatwiej jest uniknąć błędów i łatwiej jest wprowadzać
ewentualne zmiany/ulepszenia.

CC-BY-NC-ND 2023 Sławomir Marczyński
"""

# Dlaczego funkcja _input_value(...) ma nazwę zaczynającą się od znaku
# podkreślenia? Ma to być sugestia, że funkcja ta jest przeznaczona na
# wewnętrzny (prywatny/chroniony) użytek modułu.

def _input_value(prompt, type_, default=None):
    """
    Czyta aż do skutku wartość zadanego typu.

    Argumenty:
        prompt: tekst wypisywany jako podpowiedź dla użytkownika.
        type_: typ jaki ma być zwracany przez funkcję.
        default: domyślna wartość, która będzie proponowana użytkownikowi.

    Zwraca:
        przeczytaną wartość typu określonego przez type_.
    """
    value = None
    while value is None:
        if default is None:  # nie ma wartości domyślnej
            string = input(f"{prompt}: ")
        else:  # jest wartość domyślna, proponujemy ją użytkownikowi
            string = input(f"{prompt} [{default}]: ")
        string = string.strip()  # usuwamy spacje na początku i na końcu
        try:
            value = type_(string) if string else default
        except ValueError:
            pass
    return value


def input_int(prompt, default=None):
    """
    Czyta aż do skutku wartość typu int.

    Argumenty:
        prompt: tekst wypisywany jako podpowiedź dla użytkownika.
        default: domyślna wartość, która będzie proponowana użytkownikowi.

    Zwraca:
        przeczytaną wartość typu int.
    """
    return _input_value(prompt, int, default)


def input_float(prompt, default=None):
    """
    Czyta aż do skutku wartość typu float.

    Argumenty:
        prompt: tekst wypisywany jako podpowiedź dla użytkownika.
        default: domyślna wartość, która będzie proponowana użytkownikowi.

    Zwraca:
        przeczytaną wartość typu float.
    """
    return _input_value(prompt, float, default)


def input_str(prompt, default=None):
    """
    Czyta aż do skutku wartość typu str.

    Argumenty:
        prompt: tekst wypisywany jako podpowiedź dla użytkownika.
        default: domyślna wartość, która będzie proponowana użytkownikowi.

    Zwraca:
        przeczytaną wartość typu str.
    """
    return _input_value(prompt, str, default)
