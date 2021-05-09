
haslo = input('podaj hasło do sprawdzenia')

ocena = 0


def sa_małe_litery(łańcuch_znaków):
    for znak in łańcuch_znaków:
        if znak.islower():
            return True
    return False


if są_małe_litery(hasło):
    ocena += 1
    
if są_duże_litery(hasło):
    ocena += 1
    
if są_cyfry(hasło):
    ocena += 1
    
if są_znaki_specjalne(hasło):
    ocena += 1
    
if len(hasło) > 8:
    ocena += 1

if len(hasło) > 16:
    ocena += 1
    
if hasło not in słownik:
    ocena += 1
    
print('ocena hasła =', ocena)