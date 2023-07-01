# Proste wyzwania programistyczne

Przykładowe, niezbyt obszerne w realizacji, problemy. Niektóre mogłyby mieć
jakąś praktyczną przydatność, niektóre są bardziej abstrakcyjne, wszystkie służą
ilustracji jak wykorzystać podstawowe instrukcje Pythona i standardowe moduły
bibliotek do osiągnięcia założonego celu.

1. *brute_force.py* - program niezbyt elegancki, nie wykorzystujący jakiegoś
   ładnego algorytmu, ale po prostu skuteczny - sprawdzający milion różnych
   możliwości jedna po drugiej i wybierający te przypadki które spełniają 
   założone reguły. Zwykle takie podejście jest najgorszą metodą rozwiązywania
   problemu, jednak jeżeli jest efektywne może być zupełnie wystarczające.
   Innym, niż w zadaniu, przykładem jest łamanie czterocyfrowego kodu pin przez
   wypróbowanie wszystkich kombinacji cyfr po kolei - jeżeli każda tak próba
   trwa milisekundę to kod zostanie złamany w czasie krótszym niż 10 sekund.

1. *flatten.py* - niekiedy złożone dane jakie otrzymujemy zawierają dość proste
   informacje które należy z nich wyodrębnić - przykładowy program to właśnie
   robi, zbierając jednocześnie statystykę (ilość wystąpień) i generując oparty
   na tej statystyce raport.

1. *greedy.py* - przykład połączonego działania sortowania i algorytmu
   zachłannego - dość prosty, bo postawiony jest prosty warunek "zabrać jak
   najwięcej". Gdyby jednak przypisać każdej przesyłce z zadania nie tylko
   masę ale też i zysk z jej doręczenia, a to po to aby maksymalizować nie ilość
   lecz zysk... to mielibyśmy "klasyczny problem plecakowy" który jest trudny
   do rozwiązania (w sensie np-zupełności).

1. *monotonic.py* - przykład jak wyszukiwać coś możliwie najbardziej
   optymalnego - trochę naiwny, bo algorytm można znacznie ulepszyć - ale
   pokazujący że niekiedy lepsze jest proste rozwiązanie już działające niż
   świetny algorytm ale nie zaimplementowany.

1. *square.py* - to dość trudny przykład, na szczęście dzięki bibliotece
   *itertools* i funkcji *isclose()* z biblioteki *math* możliwy do rozwiązania.
   Trudności są dwojakie: porównywanie liczb rzeczywistych jest trudne, albowiem
   obliczenia nie są zupełnie dokładne i używa się zaokrągleń (to rozwiązuje
   użycie funkcji *isclose()* zamiast zwykłego operatora porównania); jeżeli
   założymy że wierzchołki nie są podane w odpowiedniej kolejności to musimy
   sprawdzić wszystkie możliwości zmiany ich kolejności (to rozwiązuje
   użycie permutacji, choć w ten sposób część obliczeń jest powtarzana
   wielokrotnie).

1. *white_list.py* - bardzo prosty przykład na sprawdzanie *każdego z każdym.*
   Przyjemną niespodzianką może być w jaki sposób działa operator *in.*
