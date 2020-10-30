##Projet Algo

import matplotlib.pyplot as plt

f = open("EIVP_KM.csv","r")
ligne = f.readline()
f.close()

def colonne(n,id): #n correspond au numéro de la colonne allant de 1 pour noise à 5 pour co2
    f = open("EIVP_KM.csv","r")
    liste = []
    ligne = f.readline()
    while ligne != '':
        ligne = f.readline()
        if ligne == '':
            break
        point = []
        for i in range(len(ligne)):
            if ligne[i] == ';':
                point += [i]
        valeur = ligne[point[n-1]+1:point[n]]
        if ligne[0] == str(id) :
            liste += [float(valeur)]
    f.close()
    return liste



def sent_at(id): #On veut le temps en secondes
    f = open("EIVP_KM.csv","r")
    liste = []
    ligne = f.readline()
    while ligne != '':
        ligne = f.readline()
        if ligne == '':
            break
        point = []
        for i in range(len(ligne)):
            if ligne[i] == ';':
                point += [i]
        valeur = ligne[point[5]+1:]
        if ligne[0] == str(id):
            liste += [valeur]
    f.close()
    #on a la liste de toutes les valeurs de sent_at
    liste_temps = []
    for i in range(len(liste)):
        liste_temps += [[int(liste[i][8:10]),int(liste[i][11:13]),int(liste[i][14:16]),int(liste[i][17:19])]]
    liste_secondes = []
    for i in range(len(liste_temps)):
        liste_secondes += [liste_temps[i][0]*24*3600 + liste_temps[i][1]*3600 + liste_temps[i][2]*60 + liste_temps[i][3]]
    liste_finale = []
    origine = liste_secondes[0]
    for i in range(len(liste_secondes)):
        liste_finale += [liste_secondes[i]-origine]
    return liste_finale


def affichage(n,id):
    Y = colonne(n,id)
    X = sent_at(id)
    plt.plot(X,Y)
    plt.show()

##Modification pour choisir des intervalles de temps

#Dans l'énoncé, il est écrit "Avec éventuellement la possibilité de spécifier un intervalle de temps dans la ligne de commande"

def affichage(n,id,ini,fin):
#temps INItial et temps FINal qui sont des jours (car les expériences se font à chaque fois dans le même mois)
#Le problème c'est qu'il faudrait avoir les temps en date et non en secondes dans sent_at car ini et fin sont des dates.
#Revoir l'algo sent_at?



