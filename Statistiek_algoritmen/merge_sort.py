import json
import os
import time

def mergesort_split(lst, value):
    """
    Functiebeschrijving:
        De functie sorteert een lijst met behulp van het mergesort-algoritme, dat gebruikt maakt van de "divide en qonquer" methode.
        Het algoritme splits de lijst op in kleinere delen tot elk deel slechts een element bevat en voegt vervolgens recursief de gesorteerde delen samen.

        Onderstaande stappen beschrijven summier welke stappen het algoritme maakt:
        • De lijst wordt in tweeën gesplitst totdat er niets meer te splitsen valt.
        • Vervolgens worden de afzonderlijke delen recursief met elkaar vergeleken.
        • Voor elke lijst wordt een teller bijgehouden.
        • Bij elke vergelijking wordt de voorwaarde gesteld dat de teller kleiner is dan de lengte van de lijst.
        • Bij elke wisseling wordt er een teller bijgehouden, zodat duidelijk is op welke plaats het item neergezet dient te worden.

        • Als voorbeeld:
        • 5 en 4 worden met elkaar vergeleken.
        • Als 5 < 4, wat onwaar is, gaat de code door naar het 'else' statement waar 4 op zijn plek wordt gezet en de teller voor deze lijst toeneemt.
        • Het overgebleven item 5 wordt op zijn plek gezet, waarvan de teller ook toeneemt.
        • Na de volgende iteratie zal deze teller 1 zijn, en wordt er niet meer aan de voorwaarde voldaan dat de teller kleiner is dat de lengte van de lijst.
        • De lus verbreekt, waarna het volgende onderdeel recursief wordt opgelost.

    Parameters:
        Lst: Lijst die gesorteerd dient te worden.
        Value: Waarde waar op gesorteerd dient te worden.

    Return:
        • Gesorteerde lijst.
        • Verstreken tijd.

    """
    start_time = time.time()#voor het bijhouden van de tijd
    if len(lst) > 1:
        #deel lijst op in twee delen
        mid = int(len(lst) // 2)
        links = lst[:mid]
        rechts = lst[mid:]

        #deel op tot de lengte van de lijst uit een enkele index bestaat
        mergesort_split(links, value)
        mergesort_split(rechts, value)

        i = 0#teller links
        j = 0#teller rechts
        k = 0#teller positie lijst

        #vergelijk wanneer teller kleiner is dan lengte lijst
        while i < len(links) and j < len(rechts):
            if links[i][f'{value}'] < rechts[j][f'{value}']:
                lst[k] = links[i]
                i += 1
            else:
                lst[k] = rechts[j]
                j += 1
            k += 1

        #Zet overgebleven index op zijn plaats
        while i < len(links):
            lst[k] = links[i]
            i += 1
            k += 1
        while j < len(rechts):
            lst[k] = rechts[j]
            j += 1
            k += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    return lst,elapsed_time


#• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • • #
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'puntcomma', 'json', 'new_steam.json')
with open(file, 'r') as bestand:
    gegevens = json.load(bestand)
print(mergesort_split(gegevens.copy(), 'negative_ratings'))

