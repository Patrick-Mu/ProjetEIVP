##Projet Algo

import matplotlib.pyplot as plt

f = open("EIVP_KM.csv","r")
ligne = f.readline()
f.close()

# La fonction colonne permet d'extraire des données du tableau excel ligne par ligne. Elle renvoie la liste des valeurs correspondant à la colonne n (n allant de 1 pour noise à 5 pour co2) et à l'expérience choisie définie par le paramètre id qui varie de 1 à 6. Il y a donc au total 6 expériences différentes.

def colonne(n,id):
    f = open("EIVP_KM.csv","r")
    liste = []
    ligne = f.readline()
    while ligne != '':
        ligne = f.readline()
        if ligne == '':
            break                                                #on extrait les données ligne par ligne
        point = []
        for i in range(len(ligne)):
            if ligne[i] == ';':
                point += [i]
        valeur = ligne[point[n-1]+1:point[n]]                    #on sélectionne les valeurs correspondant à la colonne choisie
        if ligne[0] == str(id) :
            liste += [float(valeur)]
    f.close()                                                    #on ajoute ces valeurs dans une liste vide correspondant alors
    return liste                                                 #à une colonne du tableau Excel pour une expérience particulière


# La fonction sent-at permet d'extraire toutes les valeurs de la dernière colonne. Elle sélectionne ensuite dans ces valeurs celles qui nous intéressent pour obtenir l'heure précise à laquelle on a relevé la donnée. Pour cela, elle créé une liste de liste avec dans chaque sous liste le jour, et l'heure précise (heure, minutes, secondes) du relevé.


def sent_at_date(id):
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
#on a la liste de toutes les valeurs de la dernière colonne
    liste_temps = []
    for i in range(len(liste)):
        liste_temps += [[int(liste[i][8:10]),int(liste[i][11:13]),int(liste[i][14:16]),int(liste[i][17:19])]]
    return liste_temps
#on créé une liste de listes avec, dans chaque sous liste, le jour,l'heure, les minutes et les secondes du relevé

# La fonction conv_sec permet d'obtenir une liste de temps en secondes qui correspondra à l'abscisse des courbes tracées. Pour cela, on commence par créer une liste vide liste_secondes. On convertit ensuite chaque sous liste de liste_temps définie dans la fonction précédente en une seule valeur de temps en secondes. On ajoute alors ces valeurs à la liste vide. On définit une origine des temps correspondant à la première valeur de liste_secondes et on ajoute ensuite l'ensemble des valeurs auxquelles on a retiré l'origine dans une autre liste vide appelée liste_finale.


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

#Dans l'énoncé, il est écrit "Avec éventuellement la possibilité de spécifier un intervalle de temps dans la ligne de commande" La fonction affichage permet ainsi d'afficher les courbes avec en ordonnée les valeurs d'une colonne n du fichier Excel (noise, température,etc...) pour une expérience donnée id et en abscisse les temps correspondants. La fonction affichage permet également de spécifier un jour de début et un jour de fin grâce aux paramètres deb et fin.

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

#Problème de la fonction affichage : sa complexité en temps est beaucoup trop importante car nous manipulons dans la fonction des listes de listes. La fonction courbes ci-dessous est donc une version modifiée de la fonction affichage qui manipule des listes simples et non des listes de listes.


def courbes(n,id,deb,fin):
    min = 0
    max = 0
    jours = []
    for date in sent_at_date(id):
        jours += [date[0]]                       #on ajoute dans la liste vide jour l'ensemble des jours correspondant à
    for i in range(len(jours)):                  #l'expérience choisie
        if jours[i] == deb:
            min = i
            break
    for j in range(len(jours)-1,-1,-1):
        if jours[j] == fin:
            max = j
            break                                #on sélectionne ensuite les indices min et max correspondant au jour de début
    Y = colonne(n,id)[min:max+1]                 #et au jour de fin
    X = conv_sec(sent_at_date(id))[min:max+1]
    return X,Y

#La complexité en temps de cette fonction est raisonnable et permet d'obtenir les résultats rapidement.

#La fonction affichage2 permet enfin d'afficher les courbes.

def affichage2(n,id,deb,fin):
    X,Y = courbes(n,id,deb,fin)
    plt.plot(X,Y)
    plt.show()

#La fonction min permet de trouver le minimum et d'afficher sur la courbe la valeur du minimum et l'ensemble des abscisses pour lesquelles ce minimum est atteint.

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

#La fonction max permet de trouver le maximum et d'afficher sur la courbe la valeur du maximum et l'ensemble des abscisses pour lesquelles ce maximum est atteint.

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
    X,Y = courbes(n,id,deb,fin)
    moy = sum(Y)/len(Y)
    Y_moy = len(Y)*[moy]
    plt.plot(X,Y)
    plt.plot(X,Y_moy,'r')
    plt.show()

def variance(n,id,deb,fin):
    X,Y = courbes(n,id,deb,fin)
    moy = sum(Y)/len(Y)
    var = 0
    for i in range(len(Y)):
        var += (Y[i]-moy)**2
    var = var/len(Y)
    return var

def ecart_type(n,id,deb,fin):
    e_t = variance(n,id,deb,fin)**0.5
    X,Y = courbes(n,id,deb,fin)
    moy = sum(Y)/len(Y)
    Y_haut = len(Y)*[moy+e_t]
    Y_bas = len(Y)*[moy-e_t]
    Y_moy = len(Y)*[moy]
    plt.plot(X,Y)
    plt.plot(X,Y_haut,'g',X,Y_bas,'g',X,Y_moy,'r')
    plt.show()

def tri(Y): #faire un tri pour trouver la médiane


def mediane(n,id,deb,fin):
    X,Y = courbes(n,id,deb,fin)
    Y_tri = tri(Y)
    med = 0
    if len(Y)%2 == 1:
        med = Y[len(Y)//2]
    else:
        med = (Y[len(Y)//2-1]+Y[len(Y)//2])/2
    return med

def valeurs_stats(n,id,deb,fin): #est-ce qu'on veut aussi les valeurs chiffrés avec un print?
    min(n,id,deb,fin)
    max(n,id,deb,fin)
    moy_arith(n,id,deb,fin)
    ecart_type(n,id,deb,fin)
    mediane(n,id,deb,fin)
    print()

##Indice humidex

from math import *

def humidex(T,H):
    H = H/100 #car c'est un poucentage
    a = 17.27
    b = 237.7
    Trosee = b*(a*T/(b+T)+log(H))/(a-(a*T/(b+T)+log(H)))
    return T + 0.5555*(6.11*exp(5417.7530*(1/273.16-1/(273.15+Trosee)))-10)

def courbe_humidex(id,deb,fin): #On doit l'afficher?
    X,temp = courbes(2,id,deb,fin)
    X,humidity = courbes(3,id,deb,fin)
    hum = []
    for i in range(len(temp)):
        hum += [humidex(temp[i],humidity[i])]
    plt.plot(X,hum)
    plt.show()

#Gros problème: la fonction courbes ne fonctionne pas avec id=5 et lorsque fin = 22 ?!?
#Réponse: Il n'y a pas de relevé de valeurs le 22 pour l'expérience id=5
