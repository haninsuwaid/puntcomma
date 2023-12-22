"""
    Hier gaan wij een lege functie maken met parameters, en de return. Daarbij gaan we ook uitleg
    schrijven over wat de functie doet, waar de parameters voor gebruikt worden,
    en wat de functie uiteindelijk returnt. Alleen dus Statistiekalgoritmen van
    de verplichte onderdelen van Ai.
"""



def kwantitatief_rapportcijfer_reviews(positive_reviews, negative_reviews):
    """
        functie beschrijving:
            De functie berekend het rapportcijfer per game obv de positieve en negatieve reviews

        parameters:
           positive_reviews: Het aantal positieve beoordelingen.
           negative_reviews: Het aantal negatieve beoordelingen.

        return:
            Het rapportcijfer van de reviews per game.
    """
    rapportcijfer = (positive_reviews / (positive_reviews + negative_reviews)) * 10 #bijv: 75 / ( 75 + 25) * 10 = 7.5
    #Kan eventueel ook op een schaal van 5, ipv rapportcijfer aantal sterren.

    return round(rapportcijfer, 1)

print(kwantitatief_gemiddelde_reviews(data_list['positive_ratings'],data_list['negative_ratings']))#data dient nog in variabel gezet te worden
#functies voor mediaan van alle positieve, negatieve en rapportcijfer kunnen. Tevens kan obv hiervan nog de modus of modi vastgesteld worden



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


