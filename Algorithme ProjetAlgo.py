##Projet Algo

import matplotlib.pyplot as plt

f = open("EIVP_KM.csv","r")
ligne = f.readline()
f.close()

def colonne(n,id):
#n correspond au numéro de la colonne allant de 1 pour noise à 5 pour co2
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



def sent_at_date(id): #On veut le temps en secondes
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
    return liste_temps

def conv_sec(liste_temps):
    liste_secondes = []
    for i in range(len(liste_temps)):
        liste_secondes += [liste_temps[i][0]*24*3600 + liste_temps[i][1]*3600 + liste_temps[i][2]*60 + liste_temps[i][3]]
    liste_finale = []
    origine = liste_secondes[0]
    for i in range(len(liste_secondes)):
        liste_finale += [liste_secondes[i]-origine]
    return liste_finale


##Modification pour choisir des intervalles de temps

#Dans l'énoncé, il est écrit "Avec éventuellement la possibilité de spécifier un intervalle de temps dans la ligne de commande"

def affichage(n,id,deb,fin):
    min = 0
    max = 0
    for i in range(len(sent_at_date(id))):
        if sent_at_date(id)[i][0] == deb:
            min = i
            break
    for j in range(len(sent_at_date(id))-1,-1,-1):
        if sent_at_date(id)[j][0] == fin:
            max = j
            break
    Y = colonne(n,id)[min:max+1]
    X = conv_sec(sent_at_date(id))[min:max+1]
    plt.plot(X,Y)
    plt.show()


#temps INItial et temps FINal qui sont des jours (car les expériences se font à chaque fois dans le même mois)
#Le problème c'est qu'il faudrait avoir les temps en date et non en secondes dans sent_at car ini et fin sont des dates.
#Revoir l'algo sent_at?


def courbes(n,id,deb,fin):
    min = 0
    max = 0
    jours = []
    for date in sent_at_date(id):
        jours += [date[0]]
    for i in range(len(jours)):
        if jours[i] == deb:
            min = i
            break
    for j in range(len(jours)-1,-1,-1):
        if jours[j] == fin:
            max = j
            break
    Y = colonne(n,id)[min:max+1]
    X = conv_sec(sent_at_date(id))[min:max+1]
    return X,Y

def affichage2(n,id,deb,fin):
    X,Y = courbes(n,id,deb,fin)
    plt.plot(X,Y)
    plt.show()



def min(n,id,deb,fin):
    X,Y = courbes(n,id,deb,fin)
    min =  Y[0]
    for val in Y:
        if val < min:
            min = val
    liste_min = []
    X_min = []
    Y_min = []
    for i in range(len(Y)):
        if Y[i] == min:
            liste_min += [i]
            X_min += [X[i]]
            Y_min += [Y[i]]
    plt.plot(X,Y)
    plt.scatter(X_min,Y_min,s = 10,c ='red')
    plt.show()


def max(n,id,deb,fin):
    X,Y = courbes(n,id,deb,fin)
    max =  Y[0]
    for val in Y:
        if val > max:
            max = val
    liste_max = []
    X_max = []
    Y_max = []
    for i in range(len(Y)):
        if Y[i] == max:
            liste_max += [i]
            X_max += [X[i]]
            Y_max += [Y[i]]
    plt.plot(X,Y)
    plt.scatter(X_max,Y_max,s = 10,c= 'red')
    plt.show()

def moy_arith(n,id,deb,fin):