from basisfuncties import data_naar_pandas#functie
from basisfuncties import json_path#bestand
from basisfuncties import sorteer_data
global q1, q2, q3
#• • • • • • • • • • • • • • • • • • • • • • • •Centrummaten• • • • • • • • • • • • • • • • • • • • • • • • • • • • •#
def gemiddelde(df, key):
    """
    Functiebeschrijving:
        Het gemiddelde mag gebruikt worden op interval- en ratiovariabelen. De functie berekend het gemiddelde door alle
        waarden bij elkaar op te tellen en te delen door het totaal aantal gemeten waarden.

    Parameters:
        df Pandas Dataframe
        key: Kolomnaam waar het gemiddelde van dient berekend te worden

    Return:
        Gemiddelde
    """
    return sum(df[(key)]) / len(df[(key)])

def mediaan(df, key):
    """
    Functiebeschrijving:
        De mediaan is de middelste waarneming van een reeks. De functie zet de getallen op volgorde van klein naar groot.
        Indien de lijst een even aantal waarnemeningen betreft, zal het gemiddelde van de middelste twee getallen
        genomen worden.

    Parameters:
        df: Pandas Dataframe
        key: Kolomnaam waar het mediaan bepaald dient te worden

    Return:
        Mediaan
    """
    data_copy = sorteer_data(df.copy(), key, True)

    index_mediaan = len(data_copy) // 2

    if len(data_copy) % 2 == 0:
        mediaan = (data_copy[key].iloc[index_mediaan - 1] + data_copy[key].iloc[index_mediaan]) / 2
    else:
        mediaan = data_copy[key].iloc[index_mediaan]
    return float(mediaan)

def freq(df,key):
    """
    Functiebeschrijving:
        De functie berekent hoe vaak een bepaalde waarneming zich voordoet.

    Parameters:
        df: Pandas Dataframe.
        key: Kolomnaam waarvan de waarnemingen opgeslagen worden.

    Return:
        Dict met per waarneming het aantal voorkomens.
    """
    data = sorteer_data(df,(key),True)
    freqs = dict()

    for value in data[key]:
        if value in freqs:
            freqs[value] += 1
        else:
            freqs[value] = 1

    return freqs

def modi(df,key):
    """
    Functiebeschrijving:
        De functie bepaald welke waarneming het vaakst voorkomt.

    Parameters:
        df: Pandas Dataframe.
        key: Kolomnaam waarvan de waarnemingen opgeslagen worden.

    Return:
        Dict met modus, en indien er meerdere modi zijn, een dict met modi.
    """
    lijst = freq(df,key)
    modi = dict()
    max_freq = 0
    for key, value in lijst.items():
        if value > max_freq:
            max_freq = value

    for key, value in lijst.items():
        if value >= max_freq:
            modi[key] = value

    return modi

#• • • • • • • • • • • • • • • • • • • • • • • •Spreidingsmaten• • • • • • • • • • • • • • • • • • • • • • • • • • • #
def standaarddeviatie_variantiecoëfficiënt(df,key):
    """
    Functiebeschrijving:
        Deze functie bepaalt hoe ver de waarnemingen afliggen ten opzichte van het gemiddelde.
        • Van elke waarneming berekent de functie het verschil met het gemiddelde
        • Van elk verschil wordt het kwadraat genomen
        • Vervolgens wordt het gemiddeld berekend van alle kwadraten
        • Waarna de wortel van deze uiktomst word genomen.

        Tevens wordt de variantiecoëfficiënt bepaald. Hierdoor kun je makkelijker zeggen of de mate van spreiding
        groot of klein is.
        • standaardeviatie / gemiddelde

    Parameters:
        df: Pandas Dataframe.
        key: Kolomnaam waarvan de standaarddeviatie en variantiecoëfficiënt bepaald dient te worden.

    Return:
        • standaarddeviatie
        • variantiecoëfficiënt
    """
    gemiddelde_value = gemiddelde(df,key) #gemiddelde
    verschil_machtsverheffen_sum = ((df[key] - gemiddelde_value)**2).sum()#afstand tot het gemiddelde vervolgens kwadrateren en optellen
    variantie = verschil_machtsverheffen_sum / len(df[key])#totaal kwadraten gedeeld door lengte van de data
    standaarddeviatie = round(variantie ** 0.5,2)
    variantiecoëfficiënt = standaarddeviatie / gemiddelde_value

    return standaarddeviatie, variantiecoëfficiënt

def range(df,key):
    """
    Functiebeschrijving:
    De functie bepaald de minimale en maximale waarde in een reeks waarnemingen.


    Parameters:
        df: Pandas Dataframe
        key: Kolomnaam waarvan de range bepaald dient te worden.

    Return:
        Afstand tussen de minimale en maximale waarde.
    """

    min_value = df[key].min()
    max_value = df[key].max()

    return max_value - min_value

def kwartielen(df,key):
    """
    Functiebeschrijving:
    Deze functie berekend de kwartielen van de opgegeven data.
    • q1(grenswaarde waaronder 25% van de kleinste waarnemingen liggen)
    • q2(valt samen met de mediaan)
    • q3(grenswaarde waarboven 25% van de grootste waarnemingen liggen)25% van de kleinste waarnemingen liggen)


    Parameters:
        df: Pandas Dataframe
        key: Kolomnaam waarvan de interkwartielen bepaald dienen te worden.

    Return:
        • q1
        • q2
        • q3
    """
    q = df[key].quantile([0.25,0.50,0.75])#https://datagy.io/pandas-iqr/

    return q[0.25],q[0.50],q[0.75]

def interkwartielafstand(q3,q1):
    """
    Functiebeschrijving:
    De functie berekend de afstand tussen q3 en q1, ook de interkwartielaftsand genoemd.

    Parameters:
        Kwartielen q3 en q1

    Return:
        Interkwartielaftsand(q3-q1)
    """
    return q3-q1

#• • • • • • • • • • • • • • • • • • • • • • • •Toepassing• • • • • • • • • • • • • • • • • • • • • • • • • • • • • • #
df = data_naar_pandas(json_path)
def onderzoek_data(df,key=None):
    """
    Functiebeschrijving:
    De functie brengt alle centrum- en spreidinsmaten samen, en geeft vervolgens een overzicht van de resultaten.

    Parameters:
        Pandas dataframe waarop het onderzoek uitgevoerd dient te worden

    Return:
        De functie heeft geen explicitie return-waarde. De resultaten worden geprint.
    """
    if key == None:
        key = input(f'Voer de key in van de data die je wilt onderzoeken: ')
    else:
        key == key

    q1, q2, q3 = kwartielen(df, key)

    kolomnaam = f'Onderzoek wordt gedaan op kolom: {key}'
    gemiddelde_kolom = f'Gemiddelde van de data is: {gemiddelde(df, key)}'
    mediaan_kolom = f'Mediaan van de data is: {mediaan(df, key)}'
    frequenties_kolom = f'Lijst met frequenties: {freq(df, key)}'
    modi_kolom = f'Modi/modus van de data is: {modi(df, key)}'
    standaarddeviatie_kolom = f'Standaarddeviatie van de data is: {standaarddeviatie_variantiecoëfficiënt(df, key)}'
    range_kolom = f'Range van de data is: {range(df, key)}'
    kwartielen_kolom = f'Kwartielen van de data zijn: Q1={q1}, Q2={q2}, Q3={q3}'
    interkwartielafstand_kolom = f'Interkwartielafstand van de data is: {interkwartielafstand(q3, q1)}'

    return kolomnaam,gemiddelde_kolom,mediaan_kolom,frequenties_kolom,modi_kolom,standaarddeviatie_kolom,range_kolom,kwartielen_kolom,interkwartielafstand_kolom

onderzoek_data(df)

