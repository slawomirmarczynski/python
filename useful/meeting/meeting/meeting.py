#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wyszukiwanie terminu spotkania dla (dużej) grupy osób, program w języku Python.

CC-BY-NC-ND 2024 Sławomir Marczyński
"""

import re
from collections import defaultdict
from datetime import datetime, time, timedelta

# @todo: Program mógłby wyszukiwać terminy mając na względzie dodatkowe
#        postulaty, takie jak np. przedkładanie tych dni w których obciążenia
#        uczestników innymi zajęciami są względnie małe.
#        Albo na odwrót: nie wyznaczanie terminu spotkania w dniu, w którym
#        znaczna część potencjalnych uczestników nie ma innych zajęć.
#
# @todo: Interfejs graficzny w tkinter.
#
# @todo: Czytanie z plików ICS.
#
# @todo: Testy jednostkowe (także jako doctest).

MEETING_DURATION = timedelta(hours=1)  # @todo: dać możliwość wyboru
FILE_NAME = "input4.txt"  # @todo: dać możliwość wyboru
WORKDAY_BEGIN = time(hour=8)  # dzień pracy od 8:00 do 16:00
WORKDAY_END = time(hour=16)  # dzień pracy od 8:00 do 16:00


def read_data(file_name):
    """
    Funkcja czytająca dane z pliku o podanej nazwie.

    Args:
        file_name: nazwa pliku jako łańcuch znaków. Plik powinien być plikiem
            tekstowym z kodowaniem UTF-8, powinien zawierać dane zapisane
            jako bloki linii z tekstem rozdzielone pustymi liniami. Każdy
            blok zaczyna się linią z zapisanym imieniem i nazwiskiem
            pracownika (ewentualnie innymi identyfikatorem), po którym
            następują linie już zajętych terminów w postaci::

                2024-04-12 15:00:00 2024-04-12 15:20:00

            czyli dat i godzin początku i końca zajętego terminu, zapisanych
            w formacie ISO8601 (z odstępem zamiast litery T pomiędzy datą
            a godziną).

    Returns:
        Słownik, którego kluczami są imiona i nazwiska pracowników
        (ewentualnie inne identyfikatory), a wartościami listy terminów
        zajętych. Każdy taki termin jest krotką (begin, end), gdzie begin
        to data i czas rozpoczęcia, a end to data i czas zakończenia.
    """

    # Uproszczony wzorzec dla daty i czasu zapisanych jako linie
    #
    #   2024-04-12 15:00:00 2024-04-12 15:20:00
    #
    # Kompilacja wyrażeń regularnych (regex) jest techniką optymalizacji,
    # która przyspiesza przetwarzanie. Gdy wyrażenie regularne jest
    # kompilowane, Python tworzy obiekt do dopasowywania wzorców wielokrotnie
    # bez konieczności ponownego, czasochłonnego, parsowania wzorca za każdym
    # razem. (REGEX-y są nieco skomplikowane, ale zwykle i tak dużo łatwiej
    # jest ich użyć, niż próbować analizować tekst bez ich pomocy.)
    #
    # Wzorzec jest uproszczony, bo nie weryfikuje czy ma do czynienia
    # z cyframi. Jednak dzięki temu łatwiej zrozumieć jego strukturę.
    # Kropka oznacza dowolny znak, zastąpienie jej przez \d (oznaczającą
    # dowolną cyfrę) dałoby lepsze sprawdzanie danych.
    #
    pattern = re.compile("(....-..-.. ..:..:..) (....-..-.. ..:..:..)")

    booked = defaultdict(list)

    # Otwieramy plik, instrukcja with sama zatroszczy się potem o zamknięcie,
    # tak że nie potrzebujemy wywoływać close(). Bardzo ważne jest użycie
    # parametru encoding z odpowiednią wartością, tak aby poprawnie czytać
    # litery występujące w języku polskim. Unicode z kodowaniem UTF-8 obejmuje
    # wszystkie języki znane na świecie, a więc i język polski.
    #
    with open(file_name, encoding="utf8") as file:

        # Zmienna inside_block jest używana do śledzenia, czy jesteśmy w bloku
        # linii (ciągu niepustych linii), czy nie. Na początku, zanim cokolwiek
        # przeczytamy, nie jesteśmy wewnątrz bloku. W ten sposób znaczenie
        # czytanych linii zależy od kontekstu.
        #
        inside_block = False
        name = None

        # To może wydawać się nieco dziwne, ale w Pythonie pęta for świetnie
        # działa także i z plikami tekstowymi jako kolekcjami linii. Można
        # byłoby, zamiast czytać plik pętlą for, przeczytać całą jego zawartość
        # w podziale na linie wywołaniem lines = file.readlines(), a następnie
        # użyć pętli do czytania kolejnych linii z lines.
        #
        for line in file:

            # Usuwamy niewidoczne znaki, takie jak spacje, znaki nowej linii,
            # znaki tabulacji. Usuwane są tylko znaki z początku i z końca
            # linii, odstępy wewnątrz tekstu pozostaną bez zmian.
            #
            line = line.strip()

            if not line:
                # Linia jest linią pustą, więc nie ma bloku niepustych linii
                # i dlatego do zmiennej inside_block wkładamy False.
                # Oczywiście może to być kolejna pusta linia po pustej linii.
                # Wtedy powtórne wpisanie do zmiennej inside_block False
                # jest nieszkodliwe.
                #
                inside_block = False
            else:
                # Linia jest linią niepustą, a więc coś zawiera.
                #
                if not inside_block:
                    # Wiemy, że linia nie jest pusta. Wiemy, że inside_block
                    # jest False, więc jest to pierwsza linia niepusta
                    # nowego bloku. Dlatego zmieniamy wartość inside_block
                    # na True, a tekst tej linii przepisujemy do name (które
                    # do tej pory mogło być zupełnie nieokreślone).
                    #
                    inside_block = True
                    name = line
                else:
                    # Mamy więc niepustą i do tego kolejną (czyli co najmniej
                    # drugą, a być może trzecią itd.) linię bloku niepustych
                    # linii. Stąd mamy pewność, że zmienna name jest
                    # zdefiniowana i ma odpowiednią wartość.
                    #
                    # Dopasowujemy wzorzec. Jeżeli nam się to uda, to dobrze.
                    # Jeżeli nie to ignorujemy taką niepasującą linię.
                    #
                    matcher = pattern.match(line)
                    if matcher:
                        # Wyciągamy datę i czas, osobno początku i osobno
                        # końca, jako łańcuchy znaków. Łańcuchy są w formacie
                        # określanym przez ISO8601, ale data i godzina
                        # nie są rozdzielone literą T, lecz spacją, co jest
                        # dopuszczalne i prawidłowo interpretowane przez moduł
                        # datetime.
                        #
                        begin_str = matcher.group(1)
                        end_str = matcher.group(2)

                        # Konwertujemy daty na obiekty datetime
                        #
                        begin = datetime.fromisoformat(begin_str)
                        end = datetime.fromisoformat(end_str)

                        # Dodajemy pary dat do listy przechowywanej dla name.
                        #
                        booked[name].append((begin, end))

    # Dane przeczytane, zwracamy słownik z danymi.
    #
    return booked


def flatten(data):
    """
    Spłaszczanie danych rozumiane jako redukcja list zapisanych w słowniku
    do jednej listy zawierającej elementy wszystkich ich wszystkich.

    Args:
        data: słownik, którego kluczami są imiona i nazwiska
            pracowników (ewentualnie inne identyfikatory), a wartościami listy
            terminów zajętych. Każdy taki termin jest krotką (begin, end),
            gdzie begin to data i czas rozpoczęcia, a end to data i czas
            zakończenia.

    Returns:
        Listę terminów zajętych. Każdy taki termin jest krotką (begin, end),
        gdzie begin to data i czas rozpoczęcia, a end to data i czas
        zakończenia.
    """
    flatten_list = []  # pusta lista
    for intervals in data.values():
        flatten_list.extend(intervals)  # dopisujemy intervals do flatten_list
    return flatten_list


def round_down(datetime_object, resolution_timedelta):
    """
    Zaokrąglanie obiektów datetime w dół (w kierunku przeszłości).

    Args:
        datetime_object: data i czas jako obiekt datetime.datetime.
        resolution_timedelta: skok podziałki, jaka posłuży do zaokrąglania,
            jako obiekt datetime.timedelta, nie powinien przekraczać jednej
            godziny (nie jest to sprawdzane).

    Returns:
        zaokrąglony w dół obiekt klasy datetime.datetime
    """
    date = datetime_object.date()
    h = datetime_object.hour
    m = datetime_object.minute
    minutes = h * 60 + m
    step = int(resolution_timedelta.total_seconds() / 60)
    #
    # Proste zaokrąglanie minut.
    #
    minutes = (minutes // step) * step
    h = minutes // 60
    m = minutes - h * 60
    datetime_object = datetime.combine(date, time(h, m))
    return datetime_object


def round_up(datetime_object, resolution_timedelta):
    """
    Zaokrąglanie obiektów datetime w górę (w kierunku przyszłości).

    Args:
        datetime_object: data i czas jako obiekt datetime.datetime.
        resolution_timedelta: skok podziałki, jaka posłuży do zaokrąglania,
            jako obiekt datetime.timedelta, nie powinien przekraczać jednej
            godziny (nie jest to sprawdzane).

    Returns:
        zaokrąglony w górę obiekt klasy datetime.datetime
    """
    date = datetime_object.date()
    h = datetime_object.hour
    m = datetime_object.minute
    minutes = h * 60 + m
    step = int(resolution_timedelta.total_seconds() / 60)
    if minutes % step == 0:
        # Zaokrąglanie nie jest potrzebne, wynik już jest "okrągły".
        #
        return datetime_object
    if 24 * 60 - minutes <= step:
        # Proste zaokrąglanie minut.
        #
        minutes = (minutes // step + 1) * step
    else:
        # Trochę trudniej, musimy przy zaokrąglaniu zmienić datę.
        #
        date = date + timedelta(days=1)
        minutes = (minutes // step + 1) * step - 24 * 60
    h = minutes // 60
    m = minutes - h * 60
    datetime_object = datetime.combine(date, time(h, m))
    return datetime_object


def overlapped(interval1, interval2):
    """
    Funkcja sprawdzająca czy dwa przedziały czasowe się nakładają.
    Args:
        interval1: para zawierająca, jako obiekty datetime.datetime,
            początek i koniec interwału czasowego pierwszego zdarzenia.
        interval2: para zawierająca, jako obiekty datetime.datetime,
            początek i koniec interwału czasowego drugiego zdarzenia.

    Returns:
        True jeżeli zdarzenia się nakładają, False jeżeli dzieją się
        w różnych czasach.
    """
    begin1, end1 = interval1
    begin2, end2 = interval2
    return begin1 < end2 and end1 > begin2


def main():  # @todo: ta funkcja jest zbyt zbyt złożona, zrefaktoryzować.

    # Czytanie danych i ich pobieżna weryfikacja.
    #
    data = read_data(FILE_NAME)
    if not data:
        print("Brak danych, zaawansowane wyszukiwanie terminów niemożliwe.")
        return

    number_of_peoples = len(data)
    print(f"Planowanie spotkania {number_of_peoples} osób.")
    flatten_data = flatten(data)

    if not flatten_data:
        print("Nie ma żadnych ograniczeń na termin spotkania.")
        return

    # Rozsądna dokładność terminów spotkań, przecież nie chcemy ustalać
    # rozpoczęcia spotkania na takie godziny jak 13:49 czy 11:44,
    # bo są trudne do zapamiętania.
    #
    # UWAGA: resolution_timedelta powinno być mniejsze niż kilka godzin
    #        (a nawet jedna godzina), bo obecna wersja algorytmu zaokrąglania
    #        może dawać, jeżeli ten warunek nie będzie spełniony, złe wyniki.
    #
    resolution = timedelta(minutes=5)
    assert resolution <= timedelta(hours=1)

    # Szukamy najwcześniejszego i najpóźniejszego terminu w danych.
    #
    total_begin = min((begin for begin, end in flatten_data))
    total_end = max((end for begin, end in flatten_data))
    total_begin = round_down(total_begin, resolution)
    total_end = round_up(total_end, resolution)

    # Teraz rozpatrujemy dwie opcje zerowe: opcja A to spotkanie o terminie
    # zaplanowanym wcześniejszym — zanim będą odbywać się jakiekolwiek
    # zajęcia ujęte w planach; opcja B to spotkanie w czasie wyznaczonym
    # tak, aby było po wszystkich innych zarezerwowanych terminach.
    #
    # Opcja A wymaga rozpoczęcia spotkania odpowiednio wcześniej, tak aby
    # przez cały czas jego trwania nie nastąpiła kolizja terminów.
    #
    # Opcja A mogłaby dawać złą odpowiedź, podając godzinę rozpoczęcia
    # nieprzypadającą na godziny pracy, zbyt wczesną. Takie przypadki są
    # wykrywane i korygowane: czas rozpoczęcia jest wyznaczany jako możliwie
    # najpóźniejszy, ale dnia poprzedniego. Podobnie opcja B mogłaby dać
    # odpowiedź niemieszczącą się w godzinach pracy. W tym przypadku
    # korekcja polega na przeniesienie spotkania na możliwie najwcześniejszą
    # godzinę w dniu następnym.
    #
    before = total_begin - MEETING_DURATION
    after = total_end
    one_day = timedelta(days=1)
    if before.time() < WORKDAY_BEGIN:
        before = datetime.combine(before.date() - one_day, WORKDAY_END)
        before -= MEETING_DURATION
    if (after + MEETING_DURATION).time() > WORKDAY_END:
        after = datetime.combine(after.date() + one_day, WORKDAY_BEGIN)

    # Mamy już (częściowe) rozwiązanie problemu — sugerowane terminy
    # spotkań. Nie jest jednak sprawdzane, czy terminy te nie są
    # wyznaczone na dni ustawowo wolne od pracy, w tym soboty i niedziele.
    #
    print()
    print(f"Spotkanie może się odbyć albo wcześniej niż {before},")
    print(f"                           albo później niż {after}")
    print()
    print("Inne proponowane terminy:")
    print()

    # Iteracyjnie sprawdzamy, co dzieje się, gdy zgodzimy się na nieobecność
    # części potencjalnych uczestników. Oczywiście zaczynamy od zgody na zero
    # nieobecności, czyli ma być pełna obecność.
    #
    # @todo: Jak, mając dane jakie mamy szukać tylko tych terminów,
    #        które obejmują dni które jeszcze nie minęły, tj. w których
    #        będzie można jeszcze coś zrobić?
    #
    best = after  # najlepsze rozwiązanie to te z najbliższą datą spotkania
    for n_absentee in range(number_of_peoples):  # pętla po liczbie nieobecnych
        begin_meeting = total_begin
        end_meeting = begin_meeting + MEETING_DURATION

        # Sprawdzamy, czy możemy dalej szukać i, dodatkowo, czy damy radę
        # znaleźć lepsze rozwiązanie niż już najlepsze znalezione do tej pory.
        #
        while end_meeting <= total_end and begin_meeting < best:

            # Sprawdzamy, czy mieścimy się w godzinach pracy.
            #
            # @todo: A co z niedzielami i świętami ustawowymi?
            #
            # @todo: Być może szybciej byłoby przechodzić najpierw po kolejnych
            #        dniach, a dopiero potem po godzinach pracy.
            #
            if (begin_meeting.time() <= WORKDAY_END and
                    end_meeting.time() >= WORKDAY_BEGIN):
                meeting_interval = begin_meeting, end_meeting

                # Nieobecni tworzą zbiór. Jeżeli nieobecność Pauli
                # Nowakowskiej odnotujemy kilka razy na liście, to w ten
                # sposób będziemy mieli kilka razy tę samą Paulę zapisaną.
                # Jeżeli użyliśmy zbioru set() to nieważne ile razy
                # odnotujemy nieobecność Pauli, wynikiem będzie po prostu
                # to że jedna i ta sama Paula będzie w zbiorze absentee.
                #
                absentee = set()
                for name, booked_intervals in data.items():
                    for interval in booked_intervals:
                        if overlapped(interval, meeting_interval):
                            absentee.add(name)

                # Jeżeli liczba nieobecnych jest dopuszczalna w danej iteracji,
                # to wypisujemy znaleziony rezultat. Trochę kłopotliwe jest
                # dopasowywanie odpowiedzi tak, aby nie była ona rażąco
                # niezgodna z gramatyką języka polskiego.
                #
                # @todo: Jak rozdzielić wypisywanie i obliczenia "back-end"?
                # @todo: Jak przeprowadzić i18n i L10n ?
                #
                if len(absentee) <= n_absentee:
                    print(begin_meeting, end="  ")
                    if len(absentee) == 0:
                        print(f"wszyscy obecni")
                    elif len(absentee) == 1:
                        name = list(absentee)[0]
                        print(f" 1 nieobecny: {name}")
                    else:
                        names = ", ".join(sorted(list(absentee)))
                        print(f"{n_absentee:2} nieobecnych: {names}")
                    best = begin_meeting
                    break

            # Inkrementujemy wartości określające okno czasowe danej iteracji,
            # tym kończy się pętka while.
            #
            begin_meeting += resolution
            end_meeting += resolution


# Standardowy sposób rozpoznawania czy uruchomiamy jako program, czy może
# ładujemy jako dodatkową bibliotekę instrukcją import. Gdy jako program to
# zmienna name zawiera tekst "__main__", ale gdy jako bibliotekę to będzie
# w name nazwa pliku bez .py, czyli w naszym konkretnym przypadku "meeting".
# Dla dociekliwych: pliki __main__.py mają w Pythonie szczególne znaczenie,
# umieszcza się w nich kod startowy pakietów Pythona.
#
if __name__ == "__main__":
    # Wywołujemy funkcję main, choć w zasadzie moglibyśmy po prostu wstawić
    # tu instrukcje, jakie są w funkcji main, a ją samą skasować.
    #
    main()
