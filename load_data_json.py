import json


def laad_json_bestand(bestandsnaam):
    with open((bestandsnaam), 'r') as bestand:
        gegevens = json.load(bestand)
        return gegevens#list van dicts

def laad_eerste_game(list):
    lijst = list
    for key, value in lijst[0].items():
        print(f'Key: {key} Value: {value}')
    #return lijst[0]
    #bron: https://github.com/OXKuiper/PROG-demos/blob/master/PROG7.py

# def sorteer(list):
#     for key, value in list.items():
#         if key['positive_ratings'] >......
#bron: https://canvas.hu.nl/courses/39942/pages/prog7-control-structures-and-dictionaries-uitwerkingen?module_item_id=943900
#bron: https://discuss.python.org/t/sort-a-list-in-ascending-order-using-loop/31170/2

data_list = laad_json_bestand('steam.json')
(laad_eerste_game(data_list))