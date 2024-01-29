from basisfuncties import data_naar_pandas#functie
from basisfuncties import json_path#bestand
from basisfuncties import sorteer_data

#---------------------------------------------centrummaten-----------------------------------------------------------#
def gemiddelde(data,key):
    return sum(data[(key)]) / len(data[(key)])

def mediaan(data,key):
    data_copy = sorteer_data(data.copy(),key,True)

    index_mediaan = len(data_copy) // 2

    if len(data_copy) % 2 == 0:
        mediaan = (data_copy[key].iloc[index_mediaan - 1] + data_copy[key].iloc[index_mediaan]) / 2
    else:
        mediaan = data_copy[key].iloc[index_mediaan]
    return float(mediaan)

def freq(data,key):
    data = sorteer_data(data,(key),True)
    freqs = dict()

    for value in data[key]:
        if value in freqs:
            freqs[value] += 1
        else:
            freqs[value] = 1

    return freqs

def modi(data,key):
    lijst = freq(data,key)
    modi = dict()
    max_freq = 0
    for key, value in lijst.items():
        if value > max_freq:
            max_freq = value

    for key, value in lijst.items():
        if value >= max_freq:
            modi[key] = value

    return modi

#---------------------------------------------spreidingsmaten--------------------------------------------------------#

def standaarddeviatie_variantiecoëfficiënt(data,key):

    gemiddelde_value = gemiddelde(data,key) #gemiddelde
    verschil_machtsverheffen_sum = ((data[key] - gemiddelde_value)**2).sum()#afstand tot het gemiddelde vervolgens kwadrateren en optellen
    variantie = verschil_machtsverheffen_sum / len(data[key])#totaal kwadraten gedeeld door lengte van de data
    standaarddeviatie = round(variantie ** 0.5,2)
    variantiecoëfficiënt = standaarddeviatie / gemiddelde_value

    return standaarddeviatie, variantiecoëfficiënt

def range(data,key):
    min_value = data[key].min()
    max_value = data[key].max()

    return max_value - min_value

def kwartielen(data,key):
    q = data[key].quantile([0.25,0.50,0.75])#https://datagy.io/pandas-iqr/

    return q[0.25],q[0.50],q[0.75]

def interkwartielafstand(q3,q1):
    return q3-q1

#-------------------------------------------------------------------------------------------------------------------#
def onderzoek_data(data):
    key = input(f'Voer de key in van de data die je wilt onderzoeken: ')
    print(f'\nGemiddelde van de data is: {gemiddelde(data, key)}')
    print(f'Mediaan van de data is: {mediaan(data, key)}')
    print(f'Lijst met frequenties: {freq(data, key)}')
    print(f'Modi/modus van de data is: {modi(data, key)}')
    print(f'Standaarddeviatie van de data is: {standaarddeviatie_variantiecoëfficiënt(data, key)}')
    print(f'Range van de data is: {range(data, key)}')
    q1,q2,q3= kwartielen(data, key)
    print(f'Kwartielen van de data zijn: Q1={q1}, Q2={q2}, Q3={q3}')
    print(f'Interkwartielafstand van de data is: {interkwartielafstand(q3, q1)}')

df = data_naar_pandas(json_path)
#onderzoek_data(df)
