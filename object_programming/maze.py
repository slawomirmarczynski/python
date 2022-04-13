#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#region
"""
Program demonstrujący użycie technik programowania obiektowego. Jako przykład
służy labirynt: trzeba utworzyć labirynt, pokazać go itd.

Labirynt jest złożony z komnat i ścian. Każda ściana rozdziela dokładnie dwie
komnaty. Wszystkie komnaty tworzą kolekcję (użycie zbioru, tj. set, ma zalety,
ale lista ma operację shuffle, która pozwoli losowo wybierać ściany do usuwania.
Algorytm tworzy labirynt ze wszystkimi możliwymi ścianami. Następnie usuwane są
te ściany, które uniemożliwiają przejście pomiędzy komnatami. Czyli jeżeli mimo
istnienia ściany da się przejść pomiędzy komnatą A i komnatą B , to ściana
pozostaje nienaruszona. W przeciwnym razie jest ona usuwana.

UWAGA: program ma więcej komentarzy niż jest to niezbędne. Komentarze są
także tam gdzie wyjaśniają rzeczy oczywiste dla przeciętnego programisty
używającego języka Java. Są dwie szkoły: jedna zakłada że komentarzy należy
używać bardzo oszczędnie (patrz R.C. Martin "Czysty kod"); druga zaleca
komentowanie wszystkiego i wszędzie (D. van Tassel "Praktyka programowania").
Z pewnością napisanie (i poprawianie w miarę zmian w kodzie) komentarza jest
pracochłonne. Z drugiej strony dobre komentarze potrafią zaoszczędzić mnóstwo
czasu w przyszłości, gdy np. ktoś będzie modyfikował nasz program.
Zalecałbym, w samodzielnie pisanych programach, pisanie przynajmniej jednej
linijki komentarza co 3 linie programu. Zwracam też uwagę na znaczniki TODO,
czyli zwyczajowy sposób określania rzeczy które warto byłoby zrobić.


The MIT License

Copyright 2019 Sławomir Marczyński.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
#endregion


import turtle
from random import shuffle


class Maze:

    def __init__(self, width, height):
        """
        Tworzenie labiryntu. 
        
        Najpierw gromadzimy wszystkie komnaty i wszystkie ściany. Potem usuwamy
        te ściany które chcą być usunięte.

        Parametry:
            width (int):  szerokość labiryntu
            height (int): wysokość labiryntu
        Zwraca:
            labirynt jako obiekt
        """
        self.WIDTH = width
        self.HEIGHT = height
        self._chambers = list()
        self._walls = set()

        # Taka mała ciekawostka: klasa Maze definiowana zanim będziemy mieli
        # w pełni zdefiniowaną klasę Chamber, ale możemy używać klasy Chamber
        # już teraz.

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self._chambers.append(Chamber(x, y))
        for chamber1 in self._chambers:
            for chamber2 in self._chambers:
                if chamber1.near(chamber2) and id(chamber1) > id(chamber2):
                    self._walls.add(Wall(chamber1, chamber2))

        # Zagwarantowanie losowości - set może, teoretycznie, porządkować
        # elementy zgodnie z hash'em - nie gwarantuje określonego porządku
        # elementów - ale nie gwarantuje też przypadkowej kolejności - czyli
        # samo użycie zbioru zamiast listy nie zapewnia że komnaty będą
        # przypadkowo wybierane ze zbioru.
        #
        shuffled_walls = list(self._walls)
        shuffle(shuffled_walls)
        
        for wall in shuffled_walls:
            if wall.should_be_removed():
                self._walls.remove(wall)
        
    def draw(self, view):
        """
        Narysowanie całego labiryntu.

        Parametry:
            view (View): obiekt podklasy klasy View
        """

        def draw_maze():
            for wall in self._walls:
                wall.draw(view)

        def draw_border():
            view.draw_line(0, 0, self.WIDTH, 0)
            view.draw_line(0, 0, 0, self.HEIGHT)
            view.draw_line(self.WIDTH, 0, self.WIDTH, self.HEIGHT)
            view.draw_line(0, self.HEIGHT, self.WIDTH, self.HEIGHT)

        if view:
            draw_maze()
            draw_border()


class Chamber:
    """
    Klasa, której obiekty reprezentują pojedynczą komnatę w labiryncie. 
    
    Każda komnata w labiryncie ma zbiór komnat z nią połączonych.
    """

    def __init__(self, x, y):
        """
        Komnaty maja jakieś położenie, określone przez współrzędne (x,y).
        """        
        self.X = x
        self.Y = y
        self._connected = {self}
        
    def near(self, chamber):
        """
        Sprawdzanie czy dana komnata (self) sąsiaduje z inną komnatą (chamber).

        Parametry:
            chamber (Chamber): komnata którą sprawdzamy czy jest sąsiednią.
        """
        distance = abs(self.X - chamber.X) + abs(self.Y - chamber.Y)
        return distance == 1

    def merge_chamber(self, another):
        """
        Łączenie przez dwóch komnat a i b.  Jeżeli połączenia nie ma,
        to aktualizowana są listy komnat połączonych z komnatą a i b.

        Parametry:
            another (Chamber): komnata, z którą połączenie jest sprawdzane.
        Zwraca:
            True jeżeli ściana powinna być usunięta ze zbioru/listy
            istniejących ścian, False jeżeli nie jest to konieczne.
        """

        should_wall_be_removed = another not in self._connected
        if should_wall_be_removed:
            self._connected |= another._connected
            for ch in self._connected:
                ch._connected = self._connected
        return should_wall_be_removed


class Wall:
    """
    Klasa której obiekty reprezentują ściany.
    """

    def __init__(self, a, b):
        """
        Ściana jest tworzona jako coś pomiędzy dwoma komnatami.

        Parametry:
            a (Chamber): jedna z komnat.
            b (Chamber): druga z komnat.
        """
        self.A = a
        self.B = b

    def should_be_removed(self):
        """
        Wywołanie tej metody nie oznacza bezwarunkowego usunięcia ściany,
        a tylko przygotowanie do usunięcia ściany.

        Zwraca:
            False jeżeli nic nie trzeba robić.
        """
        return self.A.merge_chamber(self.B)

    def draw(self, view):
        """
        Rysowanie ściany polega na tym, że to nie my (ew. jakiś inny obiekt)
        rysujemy ścianę, ale że ściana sama się rysuje. Wszystkie operacje
        robimy za pomocą fasady, tj. View jest także klasą dostarczającą
        "standardowego zestawu narzędzi do rysowania", co skutecznie izoluje nas
        od konkretnej biblioteki graficznej itd.

        Parametry:
            view (View): obiekt View, dostarczający toolkitu do rysowania
        """
        if self.A.Y == self.B.Y:
            if self.A.X < self.B.X:
                view.draw_line(self.B.X, self.B.Y, self.B.X, self.B.Y + 1)
            else:
                view.draw_line(self.A.X, self.A.Y, self.A.X, self.A.Y + 1)
        elif self.A.X == self.B.X:
            if self.A.Y < self.B.Y:
                view.draw_line(self.B.X, self.B.Y, self.B.X + 1, self.B.Y)
            else:
                view.draw_line(self.A.X, self.A.Y, self.A.X + 1, self.A.Y)


class View: # abstract
    """
    Abstrakcja odmalowywania się labiryntu: zapamiętuje labirynt (który trzeba
    będzie kiedyś odmalowywać); deklaruje jakich narzędzi do "malowania" może
    używać labirynt. UWAGA: chociaż nazywa się View, to niezupełnie jest to ten
    view o jaki chodzi we wzorcu model-view-controller (MVC).
    """

    def __init__(self, maze):
        self._maze = maze

    def draw(self):
        """
        Jeżeli maze jest to ma się narysować na tym, czyli self, obiekcie.
        """
        if self._maze:
            self._maze.draw(self)

    def draw_line(self, x1, y1, x2, y2): # abstract
        """
        Metoda kreślenia "linii" na rysunku w istocie rzeczy nie musi rysować
        linii (ściślej odcinka linii), bo możliwe są różne sposoby prezentacji -
        może to być linia, może to być np. gotowa bitmapa z fragmentem ściany,
        albo wizualizacja 3D. UWAGA: współrzędne nie są w pikselach,
        ale wyrażone w "komnatach". Metoda jest abstrakcyjna, bo jeszcze
        nie określone jest jak konkretnie rysować, to będzie dopiero w klasach
        pochodnych.

        Parametry:
            x1: współrzędna.
            y1: współrzędna.
            x2: współrzędna.
            y2: współrzędna.
        """
        raise NotImplementedError('Abstract')


class ViewTurtle(View):
    """
    Subklasa konkretna klasy abstrakcyjnej View implementująca toolkit potrzebny
    innym klasom do rysowania jako wywołania "grafiki żółwia".

    Nie jest to szczególnie wyrafinowana grafika, ale jest proste, nie wymaga
    innych niż standardowo dostępne bibliotek i co najważniejsze działa.
    """
    def __init__(self, maze):
        super().__init__(maze)
        
    def draw(self):        
        turtle.setworldcoordinates(
                0, turtle.window_height(), turtle.window_width(), 0)
        turtle.speed()
        turtle.tracer(0, 0)
        turtle.hideturtle()
        super().draw()
        turtle.update()
        turtle.done()

    def draw_line(self, x1, y1, x2, y2):
        X_UNIT = turtle.window_width() / (self._maze.WIDTH + 1)
        Y_UNIT = turtle.window_height() / (self._maze.HEIGHT + 1)
        X_MARGIN = (turtle.window_width() - self._maze.WIDTH * X_UNIT) / 2
        Y_MARGIN = (turtle.window_height() - self._maze.HEIGHT * Y_UNIT) / 2
        turtle.up()
        d = 3
        turtle.goto(X_MARGIN + x1 * X_UNIT, Y_MARGIN + y1 * Y_UNIT - d)
        turtle.fillcolor('red')
        turtle.begin_fill()
        turtle.circle(d)  
        turtle.end_fill()
        turtle.goto(X_MARGIN + x1 * X_UNIT, Y_MARGIN + y1 * Y_UNIT)
        turtle.down()
        turtle.goto(X_MARGIN + x2 * X_UNIT, Y_MARGIN + y2 * Y_UNIT)
        turtle.up()
        turtle.goto(X_MARGIN + x2 * X_UNIT, Y_MARGIN + y2 * Y_UNIT - d)
        turtle.down()
        turtle.fillcolor('red')
        turtle.begin_fill()
        turtle.circle(d)  
        turtle.end_fill()


if __name__ == "__main__":
    WIDTH = 25
    HEIGHT = 15
    maze = Maze(WIDTH, HEIGHT)
    view = ViewTurtle(maze)
    view.draw()
