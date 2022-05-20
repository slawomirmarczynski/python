# Rozmaite przykłady

## Błądzenie przypadkowe

Błądzenie przypadkowe (random walking) jest uproszczonym modelem dyfuzji gazów i podobnych zjawisk: cząstka jest przesuwana w każdym kroku w losowo wybranym
kierunku, dla uproszczenia (w modelu dwuwymiarowym) przesunięcia są tylko wzdłuż osi x lub osi y i zawsze mają jednostkową długość.

Program demonstruje użycie pętli for, instrukcji warunkowej if, generowania liczb losowych oraz możliwości grafiki żółwia (moduł turtle, animacje)
i grafiki tworzonej za pomocą biblioteki matplotlib (grafika o jakości publikacyjnej).

1. *random_walk_1.py* - wariant programu wykorzystujący listy jako tablice.
1. *random_walk_2.py* - wariant programu wykorzystujący wektory numpy jako tablice.

## Regresja liniowa

Obliczanie współczynników regresji liniowej, szacowanie niepewności współczynników (także dla małej próby), rysowanie wykresu i automatyczne zapisywanie rysunku.
Program ilustruje użycie bibliotek numpy, scipy i matplotlib do zaawansowanych obliczeń.

1. *linear_regression.py* - program jako taki.
1. *linear_regression_data.txt* - przykładowe dane dla programu.
1. *linear_regression_fig.png* - wykres narysowany przez program.

## Porównywanie plików tekstowych.

Chcemy porównać dwa pliki tekstowe, plik1.txt i plik2.txt, tak aby dodatkowe odstępy (spacje, zmiany wiersza, znaki tabulacji) nie były brane pod uwagę.
Programy ilustrują: czytanie plików tekstowych i techniki pracy z nimi; pracę z łańcuchami znaków jako tablicami znaków; użycie pętli while i instrukcji
warunkowych; zastosowanie wyrażeń regularnych.

1. *compare_two_files_1.py* - wariant programu niezbyt *pytoniczny* - zbyt skomplikowany, choć zbudowany z prostych instrukcji.
1. *compare_two_files_2.py* - ulepszona wersja, nadal niezbyt elegancka, ale dzięki funkcjom ma mniej powtarzającego się kodu (zasada DRY).
1. *compare_two_files_3.py* - *pythoniczny* wariant - dzięki użyciu standardowej obsługi wyrażeń regularnych.
1. *compare_two_files_4.py* - jest to ten sam wariant co *compare_two_files_3.py*, ale z usuniętymi komentarzami dydaktycznymi.
1. *compare_two_files_plik1.txt* - tekst przykładowy (szablon licencji MIT-expat).
1. *compare_two_files_plik2.txt* - tekst przykładowy (szablon licencji MIT-expat inaczej sformatowany).

## Raportowanie zmian plików w folderze

1. *cerber.py* - program z algorytmami o koszcie czasowym O(N\*\*2)

## Rozwiązywanie równań ruchu pocisku w powietrzu

Ruch pocisku w ośrodku stawiającym opór proporcjonalny do drugiej potęgi prędkości.

1. *air_drag.py* - program wykorzystujący metodę Eulera ze stałym krokiem.
1. *air_drag_scipy.py* - program wykorzystujący metodę Runge-Kutty 4 rzędu i metodę Runge-Kutty
    5 rzędu (RK45).
1. *air_drag_fig.png* - wykres narysowany przez program.

## Rozwiązywanie równania Laplace'a

1. *heat_2d.py* - program demonstrujący możliwości bibliotek NumPy, SciPy i MatPlotLib.
1. *heat_2d_fig.png* - wykres narysowany przez program.
