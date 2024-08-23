import random

"""
ZombieHuset
===========

ZombieHuset är ett spännande och utmanande spel utvecklat som ett projekt vid Högskolan i Gävle. 
Spelet kombinerar tur och matematiska färdigheter i en kamp för överlevnad mot hungriga zombies.

*Spelets Mekanik*
I ZombieHuset ställs spelaren inför en serie matematiska problem som måste lösas korrekt för att välja rätt dörr och undvika att bli uppäten av en zombie.
Felaktiga svar leder till att spelaren blir fångad och spelet tar slut.

*Funktioner*
-Felhantering: Klass för att hantera felmeddelanden och felaktiga inmatningar.
-Spelarmeddelanden: Dynamiska meddelanden baserade på spelets händelser, såsom introduktion, dörrval, och vinster.
-Matematiska Frågor: Anpassningsbara frågor baserade på spelarens val av räknesätt och konstanta värden.
-Spelarintegration: Hantering av spelarens väg genom spelet, inklusive val av antal frågor, räknesätt och om spelet ska fortsätta.

*Spelupplevelse*
Spelet inleds med en introduktion som sätter stämningen och förklarar spelets regler. 
Spelaren väljer sedan antal frågor, ett räknesätt och en konstant som kommer att användas i de matematiska frågorna. 
Målet är att svara korrekt på frågorna och navigera genom dörrarna utan att bli uppäten av zombies.

Gör dig redo för ett spel där dina matematiska kunskaper sätts på prov och varje val kan vara skillnaden mellan liv och död. 
Spetsa hjärnan och hoppas att turen är på din sida när du tar dig an utmaningarna i ZombieHuset!

Lycka Till!

"""

class MeddelandeOchFelHantering:
    """Klassens syfte är att samla och skicka ut alla meddelanden som behövs i spelet.  
    """

    def error_messages(self, error_num: int, antal_dörrar: int = 0) -> str:
        """Returnerar ett meddelande baserat på error_num. 

        Args:
            error_num (int): Numret som bestämmer vilket meddelande som ska returneras.
            antal_dörrar (int): Nummer som används i key:value nr 7

        Returns:
            Optional[str]: Meddelandet som motsvarar error_num, eller None om det inte finns något meddelande för det numret.
        """
        error_messages = {
            1: "Error 1: Antal frågor måste vara mellan 12 och 39",
            2: "Error 2: Ange heltal mellan 0 och 12",
            3: "Error 3: Ange en heltalssiffra",
            4: "Error 4: Välj rätt räknesätt",
            5: "Error 5: Ange heltal mellan 2 och 12",
            6: "Error 6: Ange heltal mellan 2 och 5",
            7: f"Error 7: Välj ett tal mellan 1 och {antal_dörrar}",
            8: "Error 8: Ange j eller n.",
        }
        return error_messages.get(error_num)

    def game_messages(self,
                      game_message_str: str,
                      vald_dörr: int = 0,
                      spelare_lyckats_räknare: int = 0,
                      fråge_räknare: int = 0,
                      zombie_bakom_dörr: int = 0,
                      dörrar_kvar_att_öppna: int = 0) -> str:
        """
        Returnerar ett specifikt meddelande baserat på inmatad sträng.

        Denna metod används för att generera och returnera olika meddelanden som används i spelet.
        Meddelandena är relaterade till olika händelser i spelet, såsom felaktiga svar, vinst,
        introduktionstext, val av dörr, och mer. Meddelandena kan innehålla dynamiska värden,
        såsom antalet dörrar som är kvar att öppna, antalet frågor som spelaren har klarat, och
        vilken dörr zombien befinner sig bakom.

        Args:
            game_message_str (str): Strängen som bestämmer vilket meddelande som ska returneras.
            vald_dörr (int, optional): Numret på den dörr som spelaren valde. Defaults to 0.
            spelare_lyckats_räknare (int, optional): Antalet dörrar som spelaren har klarat. Defaults to 0.
            fråge_räknare (int, optional): Antalet frågor som spelaren har kvar att svara på. Defaults to 0.
            zombie_bakom_dörr (int, optional): Numret på den dörr där zombien befinner sig. Defaults to 0.
            dörrar_kvar_att_öppna (int, optional): Antalet dörrar som är kvar att öppna. Defaults to 0.

        Returns:
            str: Det begärda meddelandet, formaterat med eventuella dynamiska värden.
        """

        game_messages = {
            "fel svar": "Game over. Du svarade fel. Zombie åt upp dig",
            "uppäten av zombie": f"Game over. Zombie var bakom dörr nummer {zombie_bakom_dörr}. Zombie åt upp dig",
            "vinst": "Gratulerar, du vann.",
            "intro": (
                "Välkommen till ZombieHuset".center(60, "=")
                + "\n\n"
                + "Ett spel som kräver tur och skicklighet.\n"
                + "Du kommer lösa matematiska problem och välja vilken av dörrarna du kommer ta dig igenom.\n"
                + "Du kommer få välja antal frågor, ett räknesätt och en känd siffra i det matematiska problemet.\n"
                + "Målet är att fly från ZombieHuset.\n"
                + "Dags att spetsa hjärnan och hoppas turen är på din sida.\n\n"
                + "Du hör Zombies hungrar efter hjärna och krafsar på dörrarna runt dig.\n\n"
                + "Lycka till!".center(60, "=")
                + "\n"
            ),
            "dörrval": f"Du valde dörr: {vald_dörr}",
            "progress räknare": f"Du klarat {spelare_lyckats_räknare} dörrar och har {fråge_räknare} frågor kvar.",
            "zombie bakom dörr": f"Zombien befann sig bakom dörr nummer {zombie_bakom_dörr}\n",
            "urval av dörrar": f"Välj en dörr mellan 1 och {dörrar_kvar_att_öppna}: ",
            "fortsätt spela": "Vill du forstätta spela (j/n): ",
            "tack meddelande": "Tack för att du ville spela ZombieHouse. Spelet avslutas",
            "total restart": "Spelet börjar om\n ",
            "mjuk restart": "Lycka till denna gång. Räkna som om livet hänger på det ",

        }
        return game_messages.get(game_message_str)

    def matematiska_frågor(self, operand: str, unknown_num: int = 0, known_num: int = 0) -> str:
        """Metod för att skicka den matematiska frågan till spelaren

        Returns:
            str: den matematiska frågan som spelaren ska svara på
        """
        return f"vad är {unknown_num} {operand} {known_num}? "

    def användar_val(self, prompt: str) -> str:
        """Returnerar ett meddelande baserat på prompt.

        Args:
            prompt (str): str som bestämmer vilket meddelande som ska returneras.

        Returns:
            Optional[str]: Meddelandet som motsvarar prompt, eller None om det inte finns något meddelande för det numret.
        """

        path_messages = {
            "antal frågor": "Välj antal frågor (12 - 39): ",
            "räknesätt": "Välj räknesätt(*, %, // eller s för slump): ",
            "tabell": "Välj mutliplikationstabell (2-12): ",
            "divisor": "Välj divisor (2-5): ",
        }

        return path_messages.get(prompt)

    def string_to_integer(self, value: str) -> int:
        """
        Denna metod försöker konvertera en sträng till ett heltal. Om konverteringen lyckas,
        returneras det konverterade heltalet. Om strängen inte kan konverteras till ett heltal
        (t.ex. om strängen innehåller icke-numeriska tecken), skrivs ett felmeddelande ut
        och metoden returnerar inget värde.

        Args:
            value (str): Strängen som ska konverteras till ett heltal.

        Returns:
            int: Det konverterade heltalet om konverteringen lyckas.
            None: Inget värde returneras om konverteringen misslyckas.
        """
        if value is not None:
            try:
                value_int = int(value)
                return value_int
            except ValueError:
                print(self.error_messages(3))

class PlayerFlow(MeddelandeOchFelHantering):
    """Class för att hantera spelarens väg genom spelet. Innehåller alla val som en spelare kan göra.
    Ärver från MeddelandeOchFelHantering för att göra det lättare senare. 
    """

    def kalkylering(self, lista_av_nummer: list[int], tabell_or_divisor: int, operand: str) -> tuple[int, int, int, str]:
        """ Metod för att ta fram det mattematiska talet

        Args:
            lista_av_nummer (list[int]): urvalet av nummer som metoden kan använda
            tabell_or_divisor (int): av användaren angiven tabell eller divisor. 
            operand (str): räknesättet

        Returns:
            tuple[int, int, int, str]: består av tabellen, randomiserad siffra, korrekta svaret och operanden
        """

        random_tal = random.choice(lista_av_nummer) 

        if operand == "*":
            korrekt_svar = random_tal * tabell_or_divisor 

        elif operand == "//":
            korrekt_svar = random_tal // tabell_or_divisor 
        else: 
            korrekt_svar =  random_tal % tabell_or_divisor 

        return tabell_or_divisor, random_tal, korrekt_svar, operand

    def forsätta_spel(self, promt: str) -> bool:
        """
        Hanterar användarens input för att avgöra om spelet ska fortsätta eller inte.

        Argument:
        - promt (str): Användarens input som ska hanteras.

        Returnerar:
        - bool: True om användaren vill fortsätta spelet, annars False.

        Beskrivning:
        Denna funktion tar emot en sträng (promt) som representerar användarens input.
        Den omvandlar inputen till gemener för att säkerställa att jämförelsen är skiftlägesokänslig.
        Sedan kontrollerar den om inputen är antingen "j" eller "n", vilket representerar
        om användaren vill fortsätta spelet eller inte. Om inputen inte är "j" eller "n",
        uppmanas användaren att ange inputen  igen tills en giltig input erhålls.
        Om användaren väljer "n", skrivs ett tackmeddelande ut och funktionen returnerar False,
        vilket indikerar att spelet inte ska fortsätta. Om användaren väljer "j", returneras True,
        vilket indikerar att spelet ska fortsätta.
        """
        promt = promt.lower()
        möjliga_svar = ("j", "n")
        while promt not in möjliga_svar:
            promt = input(
                f"{self.error_messages(8)}\n{self.game_messages('fortsätt spela')} ")
        if promt == "n":
            print(self.game_messages("tack meddelande"))
            return False
        print(self.game_messages("mjuk restart"))
        return True

    def välja_antalet_frågor(self, spelarens_val: str) -> tuple[int, list]:
        """
        Argument:
            spelarens_val (str): Användarens input för antalet frågor.

        Returnerar:
            tuple: En tuple innehållande antalet frågor valda av användaren och en lista
                av tal som representerar sekvensen av tal som ska användas i spelet.

        Beskrivning:
            Denna funktion tar en sträng (spelarens_val) som representerar användarens input
            för antalet frågor. Den konverterar inputen till ett heltal och kontrollerar om
            talet ligger inom det giltiga intervallet (12 till  39). Om talet är giltigt, genererar
            den en lista av tal (nummer_lista) baserat på det valda antalet frågor och returnerar
            både antalet frågor och listan över tal. Om talet inte är giltigt, skriver den ut ett
            felmeddelande och uppmanar användaren att ange antalet frågor  igen. Denna process
            upprepas tills ett giltigt tal är inmatat.
        """
        while True:
            antal_frågor = self.string_to_integer(spelarens_val)
            if antal_frågor and 12 <= antal_frågor <= 39:
                self.nummer_lista = self._nummer_till_räknesätt(antal_frågor)
                return antal_frågor, self.nummer_lista
            else:
                print(self.error_messages(1))
                spelarens_val = self.string_to_integer(
                    input(self.användar_val("antal frågor")))

    def välja_räknesätt(self, räknesätt: str) -> str:
        """
        Argument:
            räknesätt (str): Användarens valda räknesätt.

        Returnerar:
            str: Det valda räknesättet.

        Beskrivning:
            Denna metod tar en sträng (räknesätt) som representerar det räknesätt
            som användaren vill använda i spelet. Den kontrollerar om det valda
            räknesättet finns i listan över tillåtna räknesätt (tillåtna_räknesätt).
            Om räknesättet är tillåtet, returneras det. Om det inte är tillåtet, skrivs ett
            felmeddelande ut och användaren uppmanas att ange ett räknesätt  igen.
            Denna process upprepas tills ett tillåtet räknesätt är valt.
        """
        while True:
            tillåtna_räknesätt = ["*", "%", "//", "s"]
            if räknesätt in tillåtna_räknesätt:
                return räknesätt
            else:
                print(self.error_messages(4))
                räknesätt = input(self.användar_val("räknesätt"))

    def _nummer_till_räknesätt(self, antal_frågor: int) -> list:
        """
        Argument:
            antal_frågor (int): Antalet frågor valda av användaren.

        Returnerar:
            list: En lista av tal baserat på det valda antalet frågor.

        Beskrivning:
            Denna privata metod används för att generera en lista av tal
            (nummer_lista) baserat på det valda antalet frågor för spelet.
            Beroende på antalet frågor, skapas en lista av tal som ska användas
            i spelet. Listan returneras sedan.
        """
        if antal_frågor <= 13:
            num_list = [i for i in range(13)]

        elif 13 <= antal_frågor <= 26:
            num_list = [i for i in range(13) for _ in range(2)]

        elif 27 <= antal_frågor <= 39:
            num_list = [i for i in range(13) for _ in range(3)]

        return num_list

    def välja_matematisk_konstant(self, räknesätt: str) -> int:
        """Spelaren väljer en matematisk konstant. Det är denna som komemr vara den fasta siffran i de matematiska frågorna. 
            Kontrollerar även att spelaren ager konstanten inom korrekt intervall. 
        Arguments:
            räknesätt(str): Spelarens valda räknesätt.

        Returns:
            int: den valda konstanten. 
        """
        while True:            
            if räknesätt == "*":
                self.multiplikationstabell_int = self.string_to_integer(
                    input(self.användar_val("tabell")))         

                if self.multiplikationstabell_int is not None and 2 <= self.multiplikationstabell_int <= 12:
                    return self.multiplikationstabell_int
                else:
                    print(self.error_messages(5))

            elif räknesätt in ["//", "%"]:
                dividend_int = self.string_to_integer(
                    input(self.användar_val("divisor")))

                if dividend_int is not None and 2 <= dividend_int <= 5:
                    return dividend_int
                else:
                    print(self.error_messages(6))
            else:
                break

    def _ta_fram_matematisk_fråga(self, lista_av_nummer: list[int],räknesätt: str = None, matematisk_konstant: int = None) -> tuple[bool, int]:
        """En anonym metod för att generera alla variabler som behövs för att ge spelaren den matematiska frågan. 


        Returns:
            str : returnerar sträng från metoden kalkylering.  
        """

        tillåtna_räknesätt = ["*", "%", "//"]

        # Första statement rullar när slump är valt. andra statement är en felhantering om användaren anger en bokstav vid den matematiska frågan. 
        if räknesätt not in tillåtna_räknesätt or matematisk_konstant == None:
            slump_räknesätt = random.choice(tillåtna_räknesätt)

            if slump_räknesätt == tillåtna_räknesätt[0]:
                slump_matematisk_konstant = random.randint(2,12)

            else:
                slump_matematisk_konstant = random.randint(2,5)

            return self.kalkylering(lista_av_nummer = lista_av_nummer, tabell_or_divisor = slump_matematisk_konstant, operand = slump_räknesätt)

        return self.kalkylering(lista_av_nummer = lista_av_nummer, tabell_or_divisor = matematisk_konstant, operand = räknesätt)


    def svara_på_matematisk_fråga(self, lista_av_nummer: list[int], räknesätt: str, matematisk_konstant: int | None = None)->tuple[bool,int]:
        """
        Hanterar splarens svar på de matiematiska frågorna i spelet. 

        Metoden presenterar för spelaren en matematisk fråga baserat på den valda räknesättet och listan med nummer. 
        Därefter kontorlleras om spelarens svar mot det korrekta svaret. Om svaret är korrekt returneras True och den slumpade 
        siffran i matematikfrågan. Om svaret är fel returneras false och den slumpade siffran i matematikfrågan. 

        Arguments:
            räknesätt (str): Det valde räknesättet
            lista_av_nummer (list[int]): listan med nummer som kommer slumpas till den matematiska frågan. 
            matematisk_konstant (int| None): den av spelaren valda siffran till den matiematisk frågan. None om slumpat räknesätt är valt.

        Returns:
            bool: True om spelaren svarat korrekt på frågan. Annars False. 
            int: nummret från lista_av_nummer som användes i den matematiska frågan. 
                    Detta används för att kontrollera vilka randomiserade tal som använts
        """
        while True:
            tabell_or_divisor, random_tal, korrekt_svar, räknesätt = self._ta_fram_matematisk_fråga(lista_av_nummer, räknesätt, matematisk_konstant)

            spelarens_svar_matte_fråga = self.string_to_integer(input(self.matematiska_frågor(
                operand=räknesätt, known_num=tabell_or_divisor, unknown_num=random_tal)))

            if spelarens_svar_matte_fråga == korrekt_svar:
                return True, random_tal
            elif spelarens_svar_matte_fråga == None:
                continue

            else:
                print(self.game_messages("fel svar"))
                return


    def välja_en_dörr(self, spelarens_val_av_dörr: int, antal_frågor: int) -> tuple[bool, int]:
        """
        Hanterar spelarens val av en dörr i spelet.

        Args:
            spelarens_val_av_dörr (int): Spelarens val av dörr.
            antal_frågor (int): Antalet frågor i spelet.

        Returns:
            bool or int: False om spelaren förlorar, annars numret på dörren.

        Beskrivning:
            Denna metod hanterar spelarens val av en dörr i spelet. Spelaren
            väljer en dörr, och om denna dörr innehåller en zombie, förlorar spelaren
            och False returneras. Annars returneras numret på dörren som valts av zombien.
        """

        zombies_val_av_dörr = self._zombie_gömmer_sig_bakom_dörr(antal_frågor)
        while True:
            if spelarens_val_av_dörr is not None and 1 <= spelarens_val_av_dörr <= antal_frågor:
                if spelarens_val_av_dörr == zombies_val_av_dörr and antal_frågor > 1:
                    print(self.game_messages("uppäten av zombie",
                                             zombie_bakom_dörr=zombies_val_av_dörr))
                    return False
                else:
                    return zombies_val_av_dörr
            else:
                print(self.error_messages(7, antal_dörrar=antal_frågor))
                spelarens_val_av_dörr = self.string_to_integer(input(self.game_messages(
                    game_message_str="urval av dörrar", dörrar_kvar_att_öppna=antal_frågor)))

    def _zombie_gömmer_sig_bakom_dörr(self, totalt_antal_dörrar: int) -> int:
        """
        Genererar ett random nummer för zombiens dörrval.

        Args:
            totalt_antal_dörrar (int): Antalet dörrar i spelet.

        Returns:
            int: Zombiens valda dörr.

        Beskrivning:
            Denna privata metod används för att generera ett slumpmässigt nummer
            som representerar zombiens val av dörr i spelet. Det returnerade numret
            är zombiens valda dörr.
        """
        dörr_lista = []
        for dörr in range(totalt_antal_dörrar):
            dörr_lista.append(dörr + 1)
        zombie_dörr = random.choice(dörr_lista)
        return zombie_dörr


    def handle_game_over(self, initial_antal_frågor: int, nummer_lista: list[int], antal_korrekta_svar: int):
        """Metoden hanterar slutfasen i spelet. När en spelare svarat fel eller om zombie har ätit up en. 

        Args:
            initial_antal_fr (int): variabeln används för att hantera reset-förfarandet
            nummer_lista (list[int]): listan med ursprungliga nummren
            antal_korrekta_svar (int): antalet korrekta svar som spelaren angivit. 

        Returns:
            _type_: _description_
        """
        fortsätta_spela = self.forsätta_spel(input(self.game_messages("fortsätt spela")))
        if fortsätta_spela:
            antal_frågor = initial_antal_frågor
            nummer_lista = self._nummer_till_räknesätt(antal_frågor) 
            antal_korrekta_svar = 0  
            gameloop = True
            return antal_frågor, nummer_lista, antal_korrekta_svar,gameloop
        else: 
            antal_frågor = 0 
            nummer_lista = None
            antal_korrekta_svar = 0
            gameloop = False

            return antal_frågor, nummer_lista, antal_korrekta_svar,gameloop


def main():
    gameloop = True
    while gameloop:
        # Skapa instance för programmet.
        spelare = PlayerFlow()

        # Intromeddelande
        print(spelare.game_messages("intro"))

        # Spelaren väljer antalet frågor och tilldelar variabeler värden
        antal_frågor, nummer_lista = spelare.välja_antalet_frågor(
            input(spelare.användar_val("antal frågor")))
        initial_antal_frågor = antal_frågor
        antal_korrekta_svar = 0

        # Spelaren väljer räknesättet
        spelare_valt_räknesätt = spelare.välja_räknesätt(
            input(spelare.användar_val("räknesätt")).lower())

        # Kontrollerar om räknesättet är slump eller inte.
        if spelare_valt_räknesätt != "s":
            spelare_valt_matematisk_konstant = spelare.välja_matematisk_konstant(
                spelare_valt_räknesätt)

        # Huvudprogramloopen
        while antal_frågor > 0:

            if spelare_valt_räknesätt != "s":
                # Matematisk fråga

                spelare_svarar_matematisk_fråga = spelare.svara_på_matematisk_fråga(
                    räknesätt = spelare_valt_räknesätt,
                    lista_av_nummer = nummer_lista,
                    matematisk_konstant = spelare_valt_matematisk_konstant)

            # Om slump är valt
            else:
                spelare_svarar_matematisk_fråga = spelare.svara_på_matematisk_fråga(lista_av_nummer=nummer_lista, räknesätt=spelare_valt_räknesätt)

            if spelare_svarar_matematisk_fråga:
                # Spelarens val av dörr
                spelare_vald_dörr = spelare.string_to_integer(input(spelare.game_messages(
                    game_message_str="urval av dörrar", dörrar_kvar_att_öppna=antal_frågor)))

                # Kontrollerar om spelaren överlevde eller inte
                överlevande_spelare = spelare.välja_en_dörr(
                    spelarens_val_av_dörr=spelare_vald_dörr, antal_frågor=antal_frågor)

                # Om överlever börja om while-loopen. Ta bort den valda den randomiserade siffran från listan av nummer.
                if överlevande_spelare:
                    antal_korrekta_svar += 1
                    antal_frågor -= 1
                    nummer_lista.remove(spelare_svarar_matematisk_fråga[1])
                    print(spelare.game_messages(
                        "dörrval", vald_dörr=spelare_vald_dörr))
                    print(spelare.game_messages(
                        "progress räknare", spelare_lyckats_räknare=antal_korrekta_svar, fråge_räknare=antal_frågor))
                    print(spelare.game_messages("zombie bakom dörr",
                                                zombie_bakom_dörr=överlevande_spelare))

                    # Hanterar sista frågan i spelet. Exkuderar val av dörr.
                    if antal_frågor == 1:
                        if spelare_valt_räknesätt != "s".lower():
                            spelare_svarar_matematisk_fråga = spelare.svara_på_matematisk_fråga(
                                räknesätt=spelare_valt_räknesätt,
                                lista_av_nummer=nummer_lista,
                                matematisk_konstant=spelare_valt_matematisk_konstant)
                        else:
                            spelare_svarar_matematisk_fråga = spelare.svara_på_matematisk_fråga(lista_av_nummer=nummer_lista, räknesätt=spelare_valt_räknesätt)

                        # Vinst - logik
                        if spelare_svarar_matematisk_fråga:
                            print(spelare.game_messages("vinst"))
                            fortsätta_spela = spelare.forsätta_spel(
                                input(spelare.game_messages("fortsätt spela")))

                            if fortsätta_spela:
                                print(spelare.game_messages("total restart"))
                                antal_frågor = 0

                            else:
                                gameloop = False
                                antal_frågor = 0

                # END GAME - förlorade mot en zombie
                elif överlevande_spelare == False:
                    antal_frågor, nummer_lista, antal_korrekta_svar, gameloop = spelare.handle_game_over(initial_antal_frågor, nummer_lista, antal_korrekta_svar)

            # END GAME - Svarade fel på matematisk fråga
            else:
                antal_frågor, nummer_lista, antal_korrekta_svar, gameloop= spelare.handle_game_over(initial_antal_frågor, nummer_lista, antal_korrekta_svar)



if __name__ == "__main__":
    main()
