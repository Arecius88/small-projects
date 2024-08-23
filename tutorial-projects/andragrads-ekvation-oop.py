import math

class Andragradsekvation:
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __str__(self):
        return f"x\u00b2 + {self.p} x + {self.q} = 0"

    def lösningar(self):
        self.lösningslista = []
        self.diskriminanten = (self.p/2)**2-self.q

        if self.diskriminanten > 0:
            # Första uträkningen av x**2
            x1 = -(self.p/2)-math.sqrt(self.diskriminanten)
            
            # Väljer round som en extra rad för att jag tycker det blir mer läsbart.
            x1 = round(x1,2)
                        
            # Andra uträkningen av X**2
            x2 = -(self.p/2)+math.sqrt(self.diskriminanten)
            x2 = round(x2,2)
            self.lösningslista.extend([x1, x2])

            return self.lösningslista
        
        elif self.diskriminanten == 0:
            x1 = -(self.p/2)-math.sqrt(self.diskriminanten)            
            x1 = round(x1,2)
            self.lösningslista.append(x1)
            
            return self.lösningslista

        else:
            return self.lösningslista


def main():    
    # Fråga användaren om p och q i en andragradekvation x*x + px + q = 0
    str = input('Ange heltalen p och q i en andragradsekvation (x\u00b2 + px + q = 0): ')
    lista = str.split()

    # Hämta ut p och q från listan och omvandla datatypen från sträng till heltal
    p = int(lista[0])
    q = int(lista[1])

    ekvation = Andragradsekvation(p, q)  # Skapa objektet
    print(ekvation)

    # Anropa metoden lösningar på objektet, som returnerar en lista
    lösningar = ekvation.lösningar()

    # Skriv ut lösningen på ekvationen
    if len(lösningar) == 0:
        print('Ekvationen har inga reella lösningar')
    elif len(lösningar) == 1:
        print(f'Ekvationen har en lösning: {lösningar[0]}')
    else:
        print(f'Ekvationen har två lösningar: {lösningar[0]} och {lösningar[1]}')


main()  # Anropa huvudprogrammet, som ligger i funktionen main

