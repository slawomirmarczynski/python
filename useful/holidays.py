#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Obliczanie czy dany dzień jest ustawowo wolny od pracy.

Obecna wersja wspiera wyłącznie aktualne (rok 2022, tj. lista świąt taka jaka
obowiązuje od 2011 roku) polskie przepisy i nie będzie dawała poprawnych
wyników dla dat historycznych. Można ją łatwo rozszerzyć (OCD/SOLID) poprzez
dostarczenie odpowiednich danych inicjalizatorowi obiektu klasy Holidays.
"""


import datetime


# Poniedziałek jest pierwszym dniem tygodnia, niedziela jest siódmym.

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7


# Format: zbiór zawierający krotki (dzień, miesiąc) albo łańcuchy znaków dla
# świąt ruchomych. Gdy łańcuch znakóW to g+1 oznacza plus jeden dzień po dacie
# Wielkanocy, j+1 też plus jeden dzień po Wielkanocy ale według prawosławia.
#
# Co do zasady dni wolne od pracy są określone ustawowo dla wszystkich oraz
# odrębnymi ustawami dla wyznawców niektórych religii. I tak np. prawosławni
# mają prawo do dni wolnych według kalendarza juliańskiego.
#
# Poniżej (od 2011 roku) dni wolne od pracy w Polsce z innej przyczyny niż
# tylko ta że są szczególnym dniem tygodnia.

HOLIDAYS_PL = {
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
}


# Dni ustawowo wolne w Polsce od pracy dla baptystów.

HOLIDAYS_PL_BAPTIST_CHURCH = HOLIDAYS_PL | {
    'g-2',  # Wielki Piątek
    'g+40',  # Wielki Czwartek
}


# Dni ustawowo wolne w Polsce od pracy dla ewangelików.

HOLIDAYS_PL_EVANGELICAL_CHURCH = HOLIDAYS_PL | {
    'g-2',  # Wielki Piątek
    'g+40',  # Wielki Czwartek
}


# Dni ustawowo wolne w Polsce od pracy dla luteran.

HOLIDAYS_PL_LUTHERAN_CHURCH = HOLIDAYS_PL | {
    'g-2',  # Wielki Piątek
    'g+40',  # Wielki Czwartek
    (31, 10),  # Święto Reformacji
}


# Dni ustawowo wolne w Polsce od pracy dla mariawitów.

HOLIDAYS_PL_MARIAVITE_CHURCH = HOLIDAYS_PL | {
    (2, 8),  # Dzieło Wielkiego Miłosierdzia
    (23, 8),  # Święto Krwi i Ofiary
}


# Dni ustawowo wolne w Polsce od pracy dla prawosławnych.

HOLIDAYS_PL_ORTHODOX_CHURCH = HOLIDAYS_PL | {
    (7, 1),  # Boże Narodzenie
    (8, 1),  # Boże Narodzenie
    (19, 1),  # Chrzest Pański
    (7, 4),  # Zwiastowanie Najświętszej Marii Panny
    (19, 8),  # Przemienienie Pańskie
    (28, 8),  # Zaśnięcie Najświętszej Marii Panny
    'j+0',  # Wielkanoc (niedziela wielkanocna)
    'j+1',  # Wielkanoc (poniedziałek wielkanocny)
}


# Dni ustawowo wolne w Polsce od pracy dla zielonoświątkowców.

HOLIDAYS_PL_PENTECOSTAL_CHURCH = HOLIDAYS_PL | {
    'g-2',  # Wielki Piątek
    'g+40',  # Wielki Czwartek
    'g+50',  # Zielone Świątki (drugi dzień)
}


# Dni ustawowo wolne w Polsce od pracy dla przynajmniej dla jednej z grup
# ludności.

HOLIDAYS_PL_TOTAL = (
    HOLIDAYS_PL | HOLIDAYS_PL_BAPTIST_CHURCH | HOLIDAYS_PL_EVANGELICAL_CHURCH |
    HOLIDAYS_PL_LUTHERAN_CHURCH | HOLIDAYS_PL_MARIAVITE_CHURCH |
    HOLIDAYS_PL_ORTHODOX_CHURCH | HOLIDAYS_PL_PENTECOSTAL_CHURCH)


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

    # Algorytm podany przez T. H. O'Beirne, "How ten divisions lead
    # to Easter, New Scientist, 30 marca 1961,
    # https://books.google.com/books?id=zfzhCoOHurwC&pg=PA828 (2 maja 2022)

    # pylint: disable=invalid-name

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
    p = (h + l - 7 * m + 33 * n + 19) % 32
    return datetime.date(year, n, p)


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

    # pylint: disable=invalid-name

    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = (d + e + 114) % 31 + 1
    return datetime.date(year, month, day) + datetime.timedelta(13)


class Holidays:
    """
    Obiekty klasy Holidays potrafią sprawdzić czy dany dzień jest wolny
    od pracy.
    """

    def __init__(self, holidays_set, weekend=(SATURDAY, SUNDAY)):
        """
        Inicjalizuje obiekt Holidays.

        Obiekty klasy Holidays dostarczają funkcji is_free() skonfigurowanej
        tak aby uwzględniały święta dla określonego państwa i dla określonej
        grupy (np. wyznawców danej religii). W Polsce, niezależnie od tego że
        są dni wolne od pracy dla wszystkich, są także dodatkowe dni ustawowo
        wolne od pracy dla wyznawców określonych religii. Niezależnie od tego
        ustawowo wolne od pracy są niedziele oraz jeszcze jeden dzień (zwykle
        sobota, określa to pracodawca) w tygodniu. Np. jeżeli dniami wolnym
        mają być niedziele i poniedziałki, a pracownik jest luteraniem::

            free_days = Holidays(HOLIDAYS_PL_LUTHERANS, (SUNDAY, MONDAY))
            today_is_working_day = not free_days.is_free(datetime.now())

        Uwaga - mariawici mają ustawowo zagwarantowane, przez Polskę, szabasy
        które nie są tym samym co soboty (bo trwają od zmierzchu do zmierzchu).

        Uwaga - niektóre grupy zawodowe (np. górnicy i Barbórka) mogą mieć
        dodatkowe "branżowe" dni wolne od pracy. Obecna wersja nie uwzględnia
        tego rodzaju niuansów. Jest to względnie łatwe to ograrnięcia, np.

            BARBÓRKA = {(4, 12)}  # Barbórka jest 4 grudnia
            free_days = Holidays(HOLIDAYS_PL | BARBÓRKA)

        Parametry:
            holidays_set: kolekcja (zbiór, ale może też być krotka lub lista)
                w której wyszczególnione są święta. Kolekcja powinna zawierać
                albo krotki (dzień, miesiąc) albo łańcuchy znaków dla świąt
                ruchomych. Przykładowo gdy łańcuch znakóW to 'g+1' wtedy data
                jest kolejnym (plus jeden) dniem po dacie Wielkanocy. Podobnie
                'j+1' to też jeden dzień po Wielkanocy ale według prawosławia.
            weekend: dni tygodnia wolne od pracy, domyślnie sobota i niedziela,
                ale w razie konieczności można wybrać je dowolnie - zgodnie
                z polskim prawem niedziela powinna być zawsze wolna od pracy,
                ale program tego nie sprawdza i nie wymusza.
        """
        self._weekend = weekend
        self._holidays = set(holidays_set)
        self._memorized_years = set()
        self._dates = set()

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
        if given_date.isoweekday() in self._weekend:
            return True
        return False

    def is_holiday(self, given_date=datetime.date.today()):
        """
        Sprawdza czy dany dzień jest szczególnym świętem.

        Sprawdza czy, przy założeniach określonych przy tworzeniu obiektu
        klasy Holidays, dany dzień jest świętem wolnym od pracy niezależnie
        od ogólnych zasad dotyczących dni tygodnia. I tak, jeżeli ogólnie
        niedziele są dniami wolnymi, to sam fakt że dany dzień jest niedzielą
        nie spowoduje że is_holiday() zwróci True. Ale jeżeli to Wielkanoc,
        która zawsze jest w niedzielę, to zwróci True.

        Parametry:
            given_date: dzień (obiekt datetime.date) jaki ma być sprawdzony.

        Zwraca:
            True jeżeli dany dzień jest dniem wolnym od pracy bo jest dniem
            określonym jako szczególny dzień świąteczny (patrz wyżej),
            False jeżeli w danym dniu święta nie ma. Niedziele i soboty same
            w sobie nie wymuszają wyniku True.
        """
        # Sprawdzanie czy to jest jedno ze świąt traktowane jako dzień
        # wolny od pracy. Ponieważ obliczenia są nieco skomplikowane staramy
        # się buforować wyniki.

        year = given_date.year
        if year not in self._memorized_years:
            eastern_gregorian = compute_eastern_date(year)
            eastern_orthodox = compute_eastern_date_orthodox(year)
            for holiday in self._holidays:
                if isinstance(holiday, tuple):
                    day, month = holiday
                    self._dates.add(datetime.date(year, month, day))
                elif isinstance(holiday, str):
                    code = holiday[0]
                    offset = datetime.timedelta(int(holiday[1:]))
                    if code == 'g':
                        self._dates.add(eastern_gregorian + offset)
                    elif code == 'j':
                        self._dates.add(eastern_orthodox + offset)
                    else:
                        raise ValueError
                else:
                    raise ValueError
            self._memorized_years.add(year)

        # W tym miejscu będąc mamy już do zbioru dni wolnych od pracy dodane
        # dni wolne w interesującym nas roku. Bo albo już wcześniej mieliśmy,
        # albo właśnie przed chwilą obliczyliśmy.

        return given_date in self._dates


    def is_free(self, given_date):
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
        # przypadków, czyli zdarzać się będzie dość często. Następnie
        # sprawdzanie czy to jest jedno ze świąt traktowane jako dzień wolny
        # od pracy.

        return self.is_weekend(given_date) or self.is_holiday(given_date)


if __name__ == '__main__':

    holidays = Holidays(HOLIDAYS_PL_TOTAL)

    start_year = datetime.date.today().year
    date = datetime.date(start_year, 1, 1)
    delta = datetime.timedelta(1)
    while date.year == start_year:
        if holidays.is_holiday(date):
            print(date)
        date += delta
