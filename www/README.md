# HTML5, CSS3, ...

__World Wide Web__ i rozwiązania w nim stosowane są obecnie (rok 2023)
bardzo często stosowane zarówno do oczywistych rzeczy (witryny internetowe,
aplikacje webowe), jaki i nawet w oderwaniu od Internetu. Oczywiście można
to wykorzystać w "zwykłym" programowaniu. Tu są tylko bardzo proste przykłady
pokazujące najprostsze rzeczy.

1. **start.html** - uproszczony szablon pliku HTML5 jaki można wykorzystać
   do stworzenia strony internetowej (lub po prostu dokumentu w formacie HTML5
   dla przeglądarki internetowej takiej jak Edge, Chrome, Firefox itd.)
   Uwaga: choć miał to być minimalistyczny plik HTML5, to znalazły się w nim
   takie rzeczy jak DOCTYPE (można pominąć, ale niektóre przeglądarki przełączą
   się wtedy w niestandardowy tryb pracy), atrybut lang="PL" (konieczny jeżeli
   chcemy być uprzejmi wobec systemów automatycznego tłumaczenia i TTS),
   jawny podział na nagłówek (head) i na treść (body), a także przykład
   komentarza. Oczywiście to trochę za mało i dlatego warto zobaczyć inne
   przykłady, jak choćby *html5_css3.html* itd.
1. **html5_css3.html** i **html5_css3.css** - przykład jak kod HTML5
   współpracuje z arkuszem stylów CSS3. Dodatkowo używany jest plik image.jpg
   zawierający ilustrację która ma być umieszczona na stronie WWW.
1. **html5_canvas.html** - przykład użycia kanwy HTML5 na której rysunek jest
   tworzony skryptem napisanym w języku Javascript. W tym przykładzie są użyte
   elementy <meta> uzupełniające dokument HTML o informacje przydatne dla
   automatycznego katalogowania stron internetowych.

Uwaga: aby obniżyć ilość przesyłanych bajtów zwykle dokumenty HTML i CSS są
sformatowane w wersji "produkcyjnej" bez użycia wcięć, bez systematycznego
podziału na linie. Nie należy jednak sugerować się że twórcy stron internetowych
tak właśnie, byle jak i niestarannie, piszą. Po prostu bardzo łatwo jest
automatycznie skompresować tekst napisany w HTML i zwykle robi się to przed
publikacją go na serwerze WWW. Niekiedy kod HTML jest generowany automatycznie
(systemy CMS) i wtedy dbanie o czytelność kodu jest zbędne. 
Natomiast przykłady tu przedstawione są napisane tak, aby łatwo było je
zrozumieć.
