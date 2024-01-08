"""
    Hier gaan wij een lege functie maken met parameters, en de return. Daarbij gaan we ook uitleg
    schrijven over wat de functie doet, waar de parameters voor gebruikt worden,
    en wat de functie uiteindelijk returnt. Alleen dus Statistiekalgoritmen van
    de verplichte onderdelen van Ai.
"""
import json

with open('steam.json', 'r') as bestand:
    gegevens = json.load(bestand)

def freq(lst,key):
    """
        Functie beschrijving:
            De functie bepaalt hoe vaak de waarde van een element in de lijst voorkomt.

        Parameters:
            Lst: Lijst met dicts
            Key: Key waarop bepaalt wordt hoe vaak de waarde in de gegevens lijst voorkomt.

        Return:
            Dict met de frequentie per value.
    """
    freqs = dict()

    for item in lst:
        if item[key] in freqs:
            freqs[item[key]] += 1
        else:
            freqs[item[key]] = 1

    return freqs


def modi(lst,key):
    """
        Functie beschrijving:
            De functie bepaalt welke waarde het meest in de lijst voorkomt.

        parameters:
            Lst: Lijst met dicts
            Key: Key die doorgegeven dient te worden aan de functie die de frequentie bepaalt

        Return:
            Dict met de modus/modi
    """

    lijst = freq(lst,key)
    modi = dict()
    max_freq = 0
    for key, value in lijst.items():
        if value > max_freq:
            max_freq = value

    for key, value in lijst.items():
        if value >= max_freq:
            modi[key] = value

    return modi

print(modi(gegevens,'required_age'))


def kwantitatief_rapportcijfer_reviews(lst):
    """
        Functie beschrijving:
            De functie berekend de waardering obv het totaal aantal gegeven negatieve en positieve reviews.
            De waardering wordt uitgedrukt op een schaal van 10.

        Parameters:
            lst: Lijst van dictionaries.

        Return:
            Lijst bestaande uit zowel het rapportcijfer als het aantal gegeven ratings per game.
    """

    cijfers = []

    for item in lst:
        positieve_reviews = item['positive_ratings']
        negatieve_reviews = item['negative_ratings']
        totaal = positieve_reviews + negatieve_reviews
        rapportcijfer = (positieve_reviews / (totaal)) * 10  # bijv: 75 / ( 75 + 25) * 10 = 7.5
        game_info = {
            'Naam': item['name'],
            'Rapportcijfer': round(rapportcijfer, 1),
            'Totaal_ratings': totaal
        }
        cijfers.append(game_info)


    return cijfers

# print(kwantitatief_rapportcijfer_reviews(gegevens))
"""
    functie beschrijving:
        De functie gaat de frequentie berekenen van de genres, om te zien
        hoevaak elke genre het meest voorkomen in games

    parameters:
        genres: de genres die worden opgehaald.

    return:
        De frequentie van elke genre
"""
def kwatitatief_frequentie_genres(genres):
    # return genre_frequentie


    """
        functie beschrijving:


        parameters:


        return:
    """
def kwantitatief_frequentie_prijs():
    # return gemiddelde_review