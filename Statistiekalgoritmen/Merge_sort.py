import json
import os

def mergesort_split(lst,value):
    """
    Functiebeschrijving:
        De functie sorteert een lijst met behulp van het mergesort-algoritme, dat de "divide en qonquer" methode gebruikt.
        Het algoritme splits de lijst op in kleinere delen tot elk deel slechts een element bevat en voegt vervolgens recursief de gesorteerde delen samen.

    Parameters:
        Lst: Lijst die gesorteerd dient te worden.
        Value: Meegegeven waarde waar op gesorteerd dient te worden.

    Return:
        Gesorteerde lijst.
    """

    #Split de lijst op in twee
    if len(lst) > 1:
        mid = int(len(lst) / 2 + 0.5)#kan ook met floor, maar deze manier komt overeen met de visualisatie van:https://www.hackerearth.com/practice/algorithms/sorting/merge-sort/visualize/
        print(f'Lijst: {lst}')
        links = lst[:mid]
        print(f'Links: {links}')
        rechts = lst[mid:]
        print(f'Rechts: {rechts} ')

        #Split de lijst rechts/links op dmv recursie tot deze uit een enkele index bestaat.
        mergesort_split(links,value)
        mergesort_split(rechts,value)
        print(f'\n')


        i = 0#Zowel teller als index van links
        j = 0#Zowel teller als index van rechts
        k = 0#k = lijst die weer wordt samengevoegd

        #Bepaal of of de waarde groter is en pas de lijst
        print(f'{i,j,k}')
        while i < len(links) and j < len(rechts):
            print(f'Eerste loop.')
            print(f'lijst links: {links}')
            print(f'lijst rechts: {rechts}')
            print(f'Is {links[i]} <= {rechts[j]}')
            if links[i][f'{value}'] <= rechts[j][f'{value}']:
                print(f'Lst: {lst}')
                print(f'Lst[k] {lst[k]} = links[l] {links[i]}')
                lst[k] = links[i]
                print(f'Lst: {lst}')
                print(f'\n')

                i += 1#verhoog teller om te bepalen of we door de lijst heen zijn
            else:
                print(f'Lst: {lst}')
                print(f'Lst[k] {lst[k]} = rechts[r] {rechts[j]}')
                lst[k] = rechts[j]
                print(f'Lst: {lst}')
                print(f'\n')

                j += 1#Verhoog teller en indexwaarde
            k += 1#Verhoog indexwaarde van de lijst

        #zet overgebleven op zijn plaats
        while i < len(links):
            if lst[k] != links[i]:#! om een extra stap te voorkomen #dit ga je vergeten haal even weg om te zien wat het precies deed :p
                print(f'While i: {i} < lengte links: {len(links)}')
                print(f'Tweede loop')
                print(f'Lst: {lst}')
                print(f'Index: {k}')
                print(f'Lst[k] {lst[k]} = links[l] {links[i]}')
                lst[k] = links[i]
                print(f'Lst: {lst}')
                print(f'\n')
            i += 1
            k += 1

        while j < len(rechts):
            if lst[k] != rechts[j]:
                print(f'While j: {j} < lengte links: {len(links)}')
                print(f'Derde loop')
                print(f'Lijst: {lst}')
                lst[k] = rechts[j]
                print(lst)
            j += 1
            k += 1


        return lst

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'puntcomma', 'json', 'steam2.json')#gekopieerd
with open(file, 'r') as bestand:
    gegevens = json.load(bestand)
print(mergesort_split(gegevens.copy(), 'negative_ratings'))
#print(mergesort_split((gegevens[:4]).copy(),'negative_ratings'))


# Beschreven stappen
# Lst = [5,4,3,2,1]
#
# Links = [5,4,3]
# Rechts = [2,1]
#
# Splitten links:
# [5,4,3]
# [5,4] links
# [3] rechts
# [5] links
# [4] rechts
#
# Splitten rechts:
# [2] links
# [1] rechts
# ---------------------------------
# L = 0
# R = 0
# K = 0
#
# Links: [5]
# Rechts: [4]
#
# While l < len(links) and r < len(rechts):
#
# Links[l] <= rechts[r] (5<4)
# Lst[k] = rechts[r]
#  [4,5]
# R += 1
# K += 1
#
# -----------------------------------------------------
# L = 0
# R = 1
# K = 1
#
# While l < len(links):
# Lst[k] = links [L]
#  [4,5]
#
# L += 1
# K += 1
#
# L = 1
# R = 1
# K = 2
#
# -----------------------------
# L = 0
# R = 0
# K = 0
#
# Links: [4,5]
# Rechts: [3]
# Lst : [5,4,3]
#
# While l < len(links) and r < len(rechts):
#
# Links[l] <= rechts[r] (4<3)
#
# Lst[k] = rechts[r]
#  [3,4,3]
#
# R += 1
# K += 1
#
# -----------------------------------------
# L = 0
# R = 1
# K = 1
#
# While l < len(links)
#
# Lst[k] = links[L]
# [3,4]
#
# L += 1
# K += 1
#
# ---------------
#
# L = 1
# R = 1
# K = 2
#
# While l < len(links)
#
# Lst[k] = links[L]
# [3,4,5]
#
# L += 1
# K += 1
#
# L = 2
# R = 1
# K = 3
#
# ------------------------------------------------
#
# L = 0
# R = 0
# K = 0
#
# Links: [2]
# Rechts: [1]
#
# While l < len(links) and r < len(rechts):
#
# Links[l] <= rechts[r] (2<1)
# Lst[k] = rechts[r]
#  [1]
# R += 1
# K += 1
#
# -----------------------------------------------------------
# L = 0
# R = 1
# K = 1
#
# While l < len(links):
#
# Lst[k] = links[l]
# [1,2]
#
# L += 1
# K += 1
#
# L = 1
# R = 1
# K = 1
# -------------------------------------------------------------
#
# L = 0
# R = 0
# K = 0
#
# Links: [3,4,5]
# Rechts: [1,2]
#
# While l < len(links) and r < len(rechts):
#
# Links[l] <= rechts[r] (3<1)
# Lst[k] = rechts[r]
#  [1]
# R += 1
# K += 1
#
# L = 0
# R = 1
# K = 1
#
# While l < len(links and r < len(rechts:
# Links[l] <= rechts[r] (3<2)
# Lst[k] = rechts[r]
# [1,2]
#
# R += 1
# K += 1
#
# L = 0
# R = 2
# K = 2
#
# While l < len(links) and r < len(rechts):
# stop
#
# --------------------------------------
#
# L = 0
# R = 2
# K = 2
#
# While l < len(links):
# Lst[k] = links[l]
# [1,2,3]
#
# L += 1
# K + = 1
# ---------------------------
# L = 1
# R = 2
# K = 3
#
# While l < len(links):
# Lst[k] = links[l]
# [1,2,3,4]
#
# L += 1
# K + = 1
# ------------------------------
# L = 2
# R = 2
# K = 4
#
# While l < len(links):
# Lst[k] = links[l]
# [1,2,3,4,5]
#
# L += 1
# K + = 1
# ------------------------------
# L = 3
# R = 2
# K = 5


