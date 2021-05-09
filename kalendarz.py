from ics import Calendar
import arrow

with open('plan.ics') as plik_w_formacie_ics:
    kalendarz = Calendar(plik_w_formacie_ics.read())

teraz = arrow.get()

for wpis in kalendarz.events:
    if wpis.begin <= teraz <= wpis.end:   
        print(wpis.name)
        print('=================')

print()
print('**************')
    
# początek dnia 15 czerwca 2021, godzina 10:15    
początek = arrow.get(2021, 6, 15, 10, 15)

# koniec dnia 25 czerwca 2021, godzina 16:00
koniec = arrow.get(2021, 6, 25, 16, 00)

for wpis in kalendarz.events:
    if ((początek <= wpis.begin and koniec >= wpis.begin)
            or (koniec >= wpis.end and początek <= wpis.end)
            or (początek >= wpis.begin) and (koniec <= wpis.end)):
        print(wpis.name)
        print('**************')
    
    
    