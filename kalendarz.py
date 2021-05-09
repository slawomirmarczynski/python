from ics import Calendar
import arrow

with open('plan.ics') as plik_w_formacie_ics:
    kalendarz = Calendar(plik_w_formacie_ics.read())

teraz = arrow.get()

for wpis in kalendarz.events:
    if wpis.begin <= teraz <= wpis.end:   
        print(wpis.name)
        print('=================')
    
    
    
    