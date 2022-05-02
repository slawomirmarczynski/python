#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Obliczanie czy dany dzień jest ustawowo wolny od pracy.

Obecna wersja wspiera wyłącznie aktualne (rok 2022) polskie przepisy
i nie będzie dawała poprawnych wyników dla dat historycznych.
"""

# pylint: disable=invalid-name

import datetime


class Holidays:
    """
    Obiekty klasy Holidays potrafią sprawdzić czy dany dzień jest wolny
    od pracy.
    """

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @staticmethod
    def compute_eastern_date(year):
        """
        Oblicza datę Wielkanocy dla danego roku.

        Oblicza datę Wielkanocy dla danego roku używając zwykłego kalendarza,
        tj. kalendarza gregoriańskiego, czyli powszechnie obecnie przyjętego.

        Parametry:
            year: rok jako liczba całkowita, np. 2021

        Zwraca:
            obiekt date będący datą Wielkanocy
        """
        # Dlaczego metoda statyczna, a nie funkcja lokalna metody is_free() ?
        # Obliczanie daty Wielkanocy może być przydatne niekoniecznie tylko
        # wewnątrz is_free(). Gdyby zaś zadeklarować compute_eastern_date()
        # poza klasą (czyli po prostu jako zwykłą funkcję modułu) to byłaby
        # ona zbyt słabo powiązana z klasą Holidays.
        #
        # Algorytm podany przez T. H. O'Beirne, "How ten divisions lead
        # to Easter, New Scientist, 30 marca 1961,
        # https://books.google.com/books?id=zfzhCoOHurwC&pg=PA828 (2 maja 2022)

        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        g = (8 * b + 13) // 25
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (2 * e + 2 * i - h - k + 32) % 7
        m = (a + 11 * h + 19 * l) // 433
        n = (h + l - 7 * m + 90) // 25
        p = (h + l - 7 * m + 33 * n + 19) % 32  # TODO: sprawdzić!
        return datetime.date(year, n, p)

    @staticmethod
    def compute_eastern_date_orthodox(year):
        """
        Oblicza datę Wielkanocy dla danego roku według kalendarza juliańskiego.

        Oblicza datę Wielkanocy tak jak to jest przyjęte w prawosławiu,
        tj. na podstawie kalendarza juliańskiego. Zwracany obiekt date
        jest jednak po prostu datą kalendarza gregoriańskiego, tyle że aby
        ją wyznaczyć użyty był kalendarz juliański. Uwaga: algorytm jest
        poprawny dla dat od 1900 do 2099.

        Parametry:
            year: rok jako liczba całkowita, np. 2021

        Zwraca:
            obiekt date będący datą Wielkanocy obliczoną tak jak wymaga tego
            prawosławie (według kalendarza juliańskiego), ale zapisaną jako
            dzień kalendarza gregoriańskiego (dlatego +13 dni dodane do wyniku)
        """
        # Dlaczego metoda statyczna a nie funkcja lokalna metody is_free() ?
        # Obliczanie daty Wielkanocy może być przydatne niekoniecznie tylko
        # wewnątrz is_free(). Gdyby zadeklarować compute_eastern_date_julian()
        # poza klasą (czyli po prostu jako zwykłą funkcję modułu) to byłaby
        # ona zbyt słabo powiązana z klasą Holidays.
        #
        a = year % 4
        b = year % 7
        c = year % 19
        d = (19 * c + 15) % 30
        e = (2 * a + 4 * b - d + 34) % 7
        month = (d + e + 114) // 31
        day = (d + e + 114) % 31 + 1
        return datetime.date(year, month, day) + datetime.timedelta(13)

    def __init__(self, locale='pl_PL', extra=None, weekend=(SATURDAY, SUNDAY)):
        """
        Inicjalizuje obiekt Holidays.

        Obiekty klasy Holidays dostarczają funkcji is_free() skonfigurowanej
        tak aby uwzględniały święta dla określonego państwa i dla określonej
        grupy (np. wyznawców danej religii). W Polsce, niezależnie od tego że
        są dni wolne od pracy dla wszystkich, są także dodatkowe dni ustawowo
        wolne od pracy dla wyznawców określonych religii. Niezależnie od tego
        ustawowo wolne od pracy są niedziele oraz jeszcze jeden dzień (zwykle
        sobota, określa to pracodawca) w tygodniu. Wyjątkiem są w tym przypadku
        mariawici - stosowna ustawa gwarantuje im wolne wszystkie szabasy - co
        dodatkowo jest zawikłane przez definicję szabasu przyjętą w odnośnej
        ustawie. Aby to ogarnąć można po prostu użyć parametru weekend z inną
        niż domyślną wartością, np. jeżeli dniami wolnym od pracy mają być
        niedziele i poniedziałki, a pracownik jest luteraniem to::

            free_days = Holidays(extra='luteranie', weekend=(SUNDAY, MONDAY))
            today_is_working_day = not free_days.is_free(datetime.now())

        Uwaga - mariawici mają ustawowo zagwarantowane, przez Polskę, szabasy
        - obecnie Holidays nie przyjmuje parametru extra dla nich,
        ale można użyć domyślnego Holidays() - czyli wolne soboty i niedziele.
        Nie jest to w 100% zgodne z definicją szabasu jaka jest w ustawie
        (od zachodu Słońca w piątek) - jednakże Holidays sprawdza jedynie dni,
        nie operuje na godzinach i nie sprawdza kiedy zachodzi Słońce w danym
        miejscu na Ziemi.

        Uwaga - niektóre grupy zawodowe (np. górnicy i Barbórka) mogą mieć
        dodatkowe "branżowe" dni wolne od pracy. Obecna wersja nie uwzględnia
        tego rodzaju niuansów.

        Parametry:
            locale: parametr zarezerwowany na użytek przyszłych wersji,
                określa jakiego państwa przepisy są podstawą do obliczeń,
                domyślnie 'pl_PL', obecnie obsługiwane jest tylko 'pl_PL',
                w przyszłości np. 'fr' itp. ewentualnie 'pl_2031' itp.
            extra: dodatkowe dni wolne od pracy przewidziane dla określonych
                grup ludności (np. wyznawców religii) - jeden z łańcuchów
                'baptyści', 'ewangelicy', 'luteranie', 'prawosławni',
                'zielonoświątkowcy' - domyślnie None (czyli bez dodatkowych
                dni wolnych).
            weekend: dni tygodnia wolne od pracy, domyślnie sobota i niedziela,
                ale w razie konieczności można wybrać je dowolnie - zgodnie
                z prawem niedziela powinna być zawsze wolna od pracy, ale
                program tego nie sprawdza i nie wymusza.
        """

        assert locale == 'pl_PL'

        self.weekend = weekend
        self.memorized_years = set()
        self.memorized_dates = set()

        self.holidays = [
            (6, 1),  # Święto Trzech Króli
            (1, 1),  # Nowy Rok
            (1, 5),  # Międzynarodowy Dzień Solidarności Ludzi Pracy
            (3, 5),  # Święto Konstytucji 3 Maja
            (15, 8),  # Wniebowzięcie Najświętszej Marii Panny
            (1, 11),  # Wszystkich Świętych
            (11, 11),  # Narodowe Święto Niepodległości
            (25, 12),  # Boże Narodzenie (pierwszy dzień)
            (26, 12),  # Boże Narodzenie (drugi dzień)
            'g+0',  # Wielkanoc (niedziela wielkanocna)
            'g+1',  # 'Wielkanoc (poniedziałek wielkanocny)
            'g+49',  # Zielone Świątki
            'g+60',  # Boże Ciało,
        ]

        if not extra:
            pass
        elif extra == 'baptyści' or 'baptyści' in extra:  # TODO ---> sprawdzić czy są dobrze wpisane
            self.holidays += [
                'g-2',  # Wielki Piątek
                'g+40',  # Wielki Czwartek
            ]
        elif extra == 'ewangelicy':
            self.holidays += [
                'g+40',  # Wielki Czwartek
            ]
        elif extra == 'luteranie':
            self.holidays += [
                (31, 10),  # Święto Reformacji
            ]
        elif extra == 'prawosławni':
            self.holidays += [
                (7, 1),  # Boże Narodzenie
                (8, 1),  # Boże Narodzenie
                (19, 1),  # Chrzest Pański
                (7, 4),  # Zwiastowanie Najświętszej Marii Panny
                (19, 8),  # Przemienienie Pańskie
                (28, 8),  # Zaśnięcie Najświętszej Marii Panny
                (2, 8),  # Dzieło Wielkiego Miłosierdzia
                (23, 8),  # Święto Krwi
                'j+0',  # Wielkanoc (niedziela wielkanocna)
                'j+1',  # Wielkanoc (poniedziałek wielkanocny)
            ]
        elif extra == 'zielonoświątkowcy':
            self.holidays += [
                'g-2',  # Wielki Piątek
                'g+40',  # Wielki Czwartek
                'g+50',  # Zielone Świątki (drugi dzień)
            ]

        self.dates = set()

    def is_weekend(self, given_date=datetime.date.today()):
        """
        Sprawdza czy dzień jest wolny od pracy dlatego że jest określonym
        dniem tygodnia.

        Parametry:
            given_date: dzień (obiekt datetime.date) jaki ma być sprawdzony.

        Zwraca:
            True jeżeli dany dzień tygodnia jest dniem wolnym od pracy
            (niedziele, wolne soboty itp.), False w przeciwnym razie;
            wartość False nie oznacza że dany dzień może być świętem będącym
            dniem wolnym od pracy (przykładowo 1 stycznia przypadający
            we wtorek jest świętem, ale nie dlatego że to wtorek tylko dlatego
            że to Nowy Rok).
        """
        if given_date.isoweekday() in self.weekend:
            return True
        return False

    def is_free(self, given_date=datetime.date.today()):
        """
        Sprawdza czy, przy założeniach określonych przy tworzeniu obiektu
        klasy Holidays, dany dzień jest co do zasady wolny od pracy.

        Parametry:
            given_date: dzień (obiekt datetime.date) jaki ma być sprawdzony.

        Zwraca:
            True jeżeli dany dzień jest dniem wolnym od pracy (święta,
            niedziele, wolne soboty itp.), False jeżeli jest dniem roboczym.
        """

        # Najpierw jest sprawdzane czy dzień nie jest dniem wolnym jako że
        # jest określonym dniem tygodnia. To statystycznie może obsłużyć 2/7
        # przypadków, czyli zdarzać się będzie dość często.

        if self.is_weekend(given_date):
            return True

        # Teraz sprawdzanie czy to jest jedno ze świąt traktowane jako dzień
        # wolny od pracy. Ponieważ obliczenia są nieco skomplikowane staramy
        # się buforować wyniki.

        year = given_date.year
        if year not in self.memorized_years:
            eastern_gregorian = self.compute_eastern_date(year)
            eastern_orthodox = self.compute_eastern_date_orthodox(year)
            for h in self.holidays:
                if isinstance(h, tuple):
                    day, month = h
                    self.dates.add(datetime.date(year, month, day))
                elif isinstance(h, str):
                    code, offset = h[0], datetime.timedelta(int(h[1:]))
                    if code == 'g':
                        self.dates.add(eastern_gregorian + offset)
                    elif code == 'j':
                        self.dates.add(eastern_orthodox + offset)
                    else:
                        raise ValueError
                else:
                    raise ValueError
            self.memorized_years.add(year)

        # W tym miejscu będąc mamy już do zbioru dni wolnych od pracy dodane
        # dni wolne w interesującym nas roku. Bo albo już wcześniej mieliśmy,
        # albo właśnie przed chwilą obliczyliśmy.

        return given_date in self.dates
