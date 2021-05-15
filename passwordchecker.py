def przeczytaj_hasło():
    hasło = input('podaj hasło: ')
    hasło = hasło.strip();
    return hasło

def oceń_hasło(hasło):
    punkty = 0
    if (len(hasło) > 4):
        punkty += 5
    if (len(hasło) > 8):
        punkty += 5
#    if (są małe litery):
#        punkty += 1
#    if (są duże litery):
#        punkty += 1
#    if (są znaki specjalne):
#        punkty += 1
#    if (słowa nie ma w słowniku):
#        punkty += 5
#
# itd.             
    return punkty

def wypisz_ocenę(ocena):
    if 0 <= ocena < 4:
        print('zbyt słabe hasło')
    elif 4 <= ocena < 8:
        print('słabe hasło')
    elif ocena == 10:
        print('dobre hasło')


hasło = przeczytaj_hasło()
ocena = oceń_hasło(hasło)
wypisz_ocenę(ocena)
