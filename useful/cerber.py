#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cerber - program do pilnowania zmian w plikach.

Program sprawdzający czy i jakie zmiany zaszły w zawartości danego
katalogu, tj. czy są nowe pliki oraz czy pliki zostały skasowane,
przeniesione, zmienione lub nazwane inaczej. Program działa w ten sposób
że nazwy plików i wartości funkcji skrótu (SHA-1) zapamiętuje w osobnym
pliku cerber.p i przy kolejnych uruchomieniach porównuje stan obecny
z tym co było zapamiętane oraz zapisuje plik cerber.p na nowo.

Obecna wersja nie jest doskonała.

Aby obliczyć wartości skrótu wczytuje całe pliki, dlatego jest
odpowiednia tylko dla niezbyt wielkich plików i może zawieść gdy natrafi
np. na wielogigabajtowe pliki multimedialne (filmy).

Problemem może być także wydajność jeżeli plików będzie dużo.
Zastosowane algorytmy, przy założeniu że mamy N plików bez zmian, mają
koszt O(N**2), tj. kwadratowy, bo porównują dane o każdym pliku nowym
z danymi o każdym pliku starym. Zastosowanie słowników umożliwiłoby czas
liniowy O(N), bo choć nadal mielibyśmy N plików do sprawdzenia,
ale koszt wyszukiwania w słowniku (hash map) jest O(1), czyli stały.
Przy 1000 plików mamy obecnie jednak tylko milion porównań. Dlatego
w obecnej wersji program da sobie radę z np. kontrolą plików jednego
projektu. Nie nadaje się do "wszystkich plików na komputerze PC",
których - jak można to oszacować - będzie nieco ponad milion.

CC-BY-NC-ND 2022 Sławomir Marczyński
"""

# pylint: disable=unused-variable, too-many-locals, line-too-long


import hashlib
import os
import pickle
import sys
from collections import defaultdict

DEFAULT_FOLDER = '.'
DIGESTS_FILE_NAME = 'cerber.p'

REPORT_LINES_LEN = 80


def load_digests(folder):
    """
    Odtworzenie danych o tym jakie pliki były w danym folderze.

    Jest czytany plik pikle ze wskazanego folderu i o nazwie w zmiennej
    globalnej DIGESTS_FILE_NAME. W tym pliku powinny być wszystkie
    niezbędne informacje o tym co było wcześniej i z czym będziemy
    porównywali stan obecny. Jest jednak możliwe że albo ten plik jest
    pusty (tzn. nie ma w nim wpisów na temat plików), albo nawet nie ma
    tego pliku. W takim przypadku funkcja load_digest() też zadziała,
    tyle że zwróci listę pustą.

    Argumenty:
        folder: nazwa folderu w którym ma być plik o nazwie podanej
            w DIGEST_FILE_NAME.

    Globalne:
        DIGESTS_FILE_NAME: nazwa pliku do przechowywania "pikla".

    Zwraca:
        albo listę zawierającą krotki opisujące kolejne pliki, utworzoną
        wcześniej przez dump_digests(), albo listę pustą jeżeli nie uda
        się przeczytanie "pikla".

    """
    # @todo: biblioteka pickle nie jest bezpieczna i być może należałoby
    #        mieć dane w innej postaci, np. w formacie JSON lub XML.

    digests_and_names_list = []
    try:
        file_name = os.path.join(folder, DIGESTS_FILE_NAME)
        with open(file_name, 'rb') as pickle_file:
            digests_and_names_list = pickle.load(pickle_file)
    except IOError:
        pass
    return digests_and_names_list


def dump_digests(digests_and_names_list, folder):
    """
    Zapis istotnych informacji o plikach.

    Zapisane informacje posłużą przy kolejnym uruchomieniu programu
    do sprawdzenia jakie zaszły zmiany co do plików.

    Argumenty:
        digests_and_names_list: lista krotek jaką trzeba zapisać;
        folder: katalog w którym należy zapisać plik o nazwie zadanej
            przez globalny DIGEST_FILE_NAME.

    Globalne:
        DIGESTS_FILE_NAME: nazwa pliku do przechowywania "pikla".

    """
    file_name = os.path.join(folder, DIGESTS_FILE_NAME)
    with open(file_name, 'wb') as pickle_file:
        pickle.dump(digests_and_names_list, pickle_file)


def create_digests(folder):
    """
    Sporządza listę wartości funkcji skrótu z nazwami ścieżek i plików.

    Argumenty:
        folder: nazwa folderu z którego (i z którego podfolderów) chcemy
            zbierać informacje.

    Zwraca:
        listę krotek, każda krotka zawiera wartość funkcji skrótu, nazwę
        pliku, nazwę folderu oraz połączone ze sobą nazwy folderu
        i pliku; w szczególnych przypadkach może to być lista pusta.
    """

    def create_digest(full_path_file_name):
        """
        Oblicza wartość funkcji skrótu dla jednego pliku.

        Argumenty:
            full_name: nazwa pliku dla którego ma być
                obliczony skrót.

        Zwraca:
            wartość funkcji skrótu.
        """
        algorithm = hashlib.sha1()  # można zastąpić inną funkcją skrótu
        with open(full_path_file_name, 'rb') as file_stream:
            file_bytes = file_stream.read()  # @todo: long files support
            algorithm.update(file_bytes)
        return algorithm.digest()

    forbidden = os.path.join(folder, DIGESTS_FILE_NAME)
    digests_and_names_list = []
    for folder_name, _, files_names in os.walk(folder):
        for file_name in files_names:
            full_name = os.path.join(folder_name, file_name)
            digest = create_digest(full_name)
            digest_and_names = digest, file_name, folder_name, full_name
            if full_name != forbidden:
                digests_and_names_list.append(digest_and_names)
    return digests_and_names_list


def report_removed(old_list, new_list):
    """
    Tworzenie raportu o plikach usuniętych.

    Jako plik usunięty jest określany taki plik, który był a którego
    już nie ma i nie ma (w obrębie zadanego folderu wraz z podfolderami)
    żadnego pliku który ma taką samą zawartość (tj. wartość funkcji
    skrótu). Innymi słowy: plik będzie usunięty jeżeli już go nie ma
    i nie ma danych które w nim były.

    Argumenty:
        old_list: lista krotek "starych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
        new_list: lista krotek "nowych" plików, każda krotka taka jak
            dla parametru old_list.

    Zwraca:
        listę par (krotek) z informacjami nt. usuniętego pliku i None
        (bo nie ma nowego pliku); lista ta może być pusta.
    """
    result = []
    for f_old in old_list:
        old_digest, old_name, old_path, old_full = f_old
        for f_new in new_list:
            new_digest, new_name, new_path, new_full = f_new
            if old_digest == new_digest or old_full == new_full:
                break
        else:
            result.append((f_old, None))
    return result


def report_new(old_list, new_list):
    """
    Tworzenie raportu o nowych plikach.

    Jako plik nowy jest określany taki plik, którego nie było (w obrębie
    zadanego folderu wraz z podfolderami) i to niezależnie od nazwy tego
    pliku. Po prostu liczy się zawartość pliku, a nie nazwa pliku.

    Argumenty:
        old_list: lista krotek "starych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
        new_list: lista krotek "nowych" plików, każda krotka taka jak
            dla parametru old_list.

    Zwraca:
        listę par (krotek), każda para to None i informacje na temat
        nowego pliku; lista ta może być pusta.
    """
    result = []
    for f_new in new_list:
        new_digest, new_name, new_path, new_full = f_new
        for f_old in old_list:
            old_digest, old_name, old_path, old_full = f_old
            if old_digest == new_digest or old_full == new_full:
                break
        else:
            result.append((None, f_new))
    return result


def report_changed(old_list, new_list):
    """
    Tworzenie raportu o zmodyfikowanych plikach.

    Jako plik zmodyfikowany jest określany taki plik, który było już
    zapisany w danym folderze i z daną nazwą, ale choć ani katalog ani
    nazwa nie uległy zmianie, to zawartość pliku jest już inna.

    Argumenty:
        old_list: lista krotek "starych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
        new_list: lista krotek "nowych" plików, każda krotka taka jak
            dla parametru old_list.

    Zwraca:
        listę par (krotek), każda para to None i informacje na temat
        aktualnego pliku; lista ta może być pusta.
    """
    result = []
    for f_new in new_list:
        new_digest, new_name, new_path, new_full = f_new
        for f_old in old_list:
            old_digest, old_name, old_path, old_full = f_old
            if old_digest != new_digest and old_full == new_full:
                result.append((None, f_new))
    return result


def report_renamed_only(old_list, new_list):
    """
    Tworzenie raportu o plikach ze zmienioną tylko nazwą.

    Jako plik ze zmienioną nazwą jest określany taki plik, którego
    zawartość nie uległa zmianie, ale który ma nadaną inną nazwę.

    Argumenty:
        old_list: lista krotek "starych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
        new_list: lista krotek "nowych" plików, każda krotka taka jak
            dla parametru old_list.

    Zwraca:
        listę par (krotek), każda para to informacje na temat pliku
        przed zmianą nazwy i informacje na temat pliku po zmiane nazwy;
        lista ta może być pusta.
    """
    result = []
    for f_new in new_list:
        new_digest, new_name, new_path, new_full = f_new
        for f_old in old_list:
            old_digest, old_name, old_path, old_full = f_old
            if old_digest == new_digest and old_path == new_path and old_name != new_name:
                result.append((f_old, f_new))
    return result


def report_moved_only(old_list, new_list):
    """
    Tworzenie raportu o plikach przeniesionych i/lub kopiach.

    Argumenty:
        old_list: lista krotek "starych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
        new_list: lista krotek "nowych" plików, każda krotka taka jak
            dla parametru old_list.

    Zwraca:
        listę par (krotek), każda para to informacje na temat pliku
        przed i informacje na temat pliku po; lista ta może być pusta.
    """
    result = []
    for f_new in new_list:
        new_digest, new_name, new_path, new_full = f_new
        file_changed_or_deleted = True
        for f_old in old_list:
            old_digest, old_name, old_path, old_full = f_old
            if old_digest == new_digest and old_path == new_path and old_name == new_name:
                file_changed_or_deleted = False
                break
        if file_changed_or_deleted:
            for f_old in old_list:
                old_digest, old_name, old_path, old_full = f_old
                if old_digest == new_digest and old_path != new_path and old_name == new_name:
                    result.append((f_old, f_new))
    return result


def report_duplicated(new_list):
    """
    Tworzenie raportu o obecnie zduplikowanych.

    Argumenty:
        new_list: lista list krotek "nowych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
    Zwraca:
        listę opisującą pliki zduplikowane; lista ta może być pusta.
    """
    result = []
    digest_dict = defaultdict(list)
    for f_new in new_list:
        new_digest, new_name, new_path, new_full = f_new
        digest_dict[new_digest].append(f_new)
    for f_list in digest_dict.values():
        if len(f_list) > 1:
            result.append(f_list)
    return result


def report_moved_and_renamed(old_list, new_list):
    """
    Tworzenie raportu o plikach przeniesionych ze zmianą nazwy.

    Argumenty:
        old_list: lista krotek "starych" plików, każda krotka powinna
            się składać z wartości funkcji skrótu, nazwy, ścieżki oraz
            pełnej nazwy pliku (czyli ścieżki i nazwy razem).
            Lista może być pusta, np. jeżeli nie było wcześniej żadnych
            plików.
        new_list: lista krotek "nowych" plików, każda krotka taka jak
            dla parametru old_list.

    Zwraca:
        listę par (krotek), każda para to informacje na temat pliku
        przed i informacje na temat pliku po; lista ta może być pusta.
    """
    result = []
    for f_new in new_list:
        new_digest, new_name, new_path, new_full = f_new
        for f_old in old_list:
            old_digest, old_name, old_path, old_full = f_old
            if old_digest == new_digest and old_path != new_path and old_name != new_name:
                result.append((f_old, f_new))
    return result


def print_report(description, result):
    """
    Przedstawianie raportów w czytelnej formie.

    Argumenty:
        description: tekst opisujący czego dotyczy raport.
        result: dane do raportowania w postaci listy par krotek, takich
            że każda taka krotka opisuje plik jako wartość skrótu,
            nazwę, ścieżkę i pełną nazwę pliku.

    Globalne:
        REPORT_LINES_LEN: ilość znaków z jakich ma się składać linia
            wypisywana jako pozioma linia "tabelki".
    """
    if result:
        print()
        print('=' * REPORT_LINES_LEN)
        print(len(result), description)
        print('-' * REPORT_LINES_LEN)
        first_old_file, first_new_file = result[0]
        list_ = []
        if first_old_file is not None and first_new_file is not None:
            for f_old, f_new in result:
                old_digest, old_name, old_path, old_full = f_old
                new_digest, new_name, new_path, new_full = f_new
                list_.append(old_full + ' -> ' + new_full)
        elif first_old_file is not None:
            for f_old, f_new in result:
                new_digest, new_name, new_path, new_full = f_old
                list_.append(new_full)
        elif first_new_file is not None:
            for f_old, f_new in result:
                old_digest, old_name, old_path, old_full = f_new
                list_.append(old_full)
        list_ = sorted(list_)
        for item in list_:
            print(item)


def print_duplicates(description, list_lists_duplicates):
    """
    """
    if list_lists_duplicates:
        print()
        print('=' * REPORT_LINES_LEN)
        print(len(list_lists_duplicates), description)
        print('-' * REPORT_LINES_LEN)
        for i, list_duplicates in enumerate(list_lists_duplicates, 1):
            j = 0
            for digest, name, path, full in list_duplicates:
                j += 1
                print(f"{i}.{j}. {full}")
            print()


def main():
    """
    Funkcja odpowiadająca za uruchomienie całego programu.

    Istotną przyczyną istnienia funkcji main() jest to że izoluje
    ona zmienne lokalne, które - gdyby nie main() - byłby zmiennymi
    globalnymi.
    """
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FOLDER

    old = load_digests(folder)
    new = create_digests(folder)

    tests = (('removed files', report_removed),
             ('new files', report_new),
             ('changed files', report_changed),
             ('moved files', report_moved_only),
             ('renamed files', report_renamed_only),
             ('moved and renamed files', report_moved_and_renamed))

    duplicates = report_duplicated(new)
    print_duplicates('duplicates', duplicates)

    changes_detected = False
    for description, procedure in tests:
        result = procedure(old, new)
        if result:
            changes_detected = True
            print_report(description, result)

    if changes_detected:
        dump_digests(new, folder)
    else:
        print('=' * REPORT_LINES_LEN)
        print('nothing changes')


if __name__ == '__main__':
    main()
