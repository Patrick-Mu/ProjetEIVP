## Projet d'algorithmie // Daphné Below / Patrick Mu


import matplotlib.pyplot as plt

from math import *

## Affichage des courbes montrant l'évolution d'une variable en fonction du temps


# La fonction nom_colonnes permet d'attribuer à chaque variable un numéro.

def nom_colonnes(var):
    if var=="noise":
        return 1
    if var=="temp":
        return 2
    if var=="humidity":
        return 3
    if var=="lum" :
        return 4
    if var=="co2" :
        return 5
    else :
        print("mauvaise orthographe")


# La fonction colonne permet d'extraire des données du tableau excel ligne par ligne. Elle renvoie la liste des valeurs correspondant à une variable et à l'expérience choisie définie par le paramètre id qui varie de 1 à 6. Il y a donc au total 6 expériences différentes.

def colonne(var,id):                                             # var doit être la variable écrite entre guillemets
    n=nom_colonnes(var)                                          # Avec la fonction nom_colonnes, on attribue à chaque variable un
    f = open("excelbonneversion.csv","r")                        # numéro
    liste = []
    ligne = f.readline()
    while ligne != '':                                           # On extrait les données ligne par ligne
        ligne = f.readline()
        if ligne == '':
            break
        point = []
        for i in range(len(ligne)):
            if ligne[i] == ';':
                point += [i]
        valeur = ligne[point[n]+1:point[n+1]]                    # On sélectionne la valeur correspondant à la colonne choisie
        if ligne[point[0]+1:point[1]]  == str(id) :
            liste += [float(valeur)]                             # On ajoute ces valeurs dans une liste vide correspondant alors
    f.close()                                                    # à une colonne du tableau Excel pour une expérience particulière
    return liste


# La fonction sent_at_date permet d'extraire toutes les valeurs de la dernière colonne. Elle sélectionne ensuite dans ces valeurs celles qui nous intéressent pour obtenir l'heure précise à laquelle on a relevé la donnée. Pour cela, elle créé une liste de liste avec dans chaque sous liste le jour, et l'heure précise (heure, minutes, secondes) du relevé. On ne conserve pas l'année et le mois car chaque expérience se déroule la même année et le même mois.

def sent_at_date(id):
    f = open("excelbonneversion.csv","r")
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
        valeur = ligne[point[6]+1:]
        if ligne[point[0]+1:point[1]]  == str(id) :
            liste += [valeur]
    f.close()
# On a la liste de toutes les valeurs de la dernière colonne
    liste_temps = []
    for i in range(len(liste)):
        liste_temps += [[int(liste[i][8:10]),int(liste[i][11:13]),int(liste[i][14:16]),int(liste[i][17:19])]]
    return liste_temps
# On a crée une liste de listes avec, dans chaque sous liste, le jour, l'heure, la minute et la seconde du relevé


# La fonction conv_sec permet d'obtenir une liste de temps en secondes qui correspondra à l'abscisse des courbes tracées. Pour cela, on commence par créer une liste vide liste_secondes. On convertit ensuite chaque sous-liste de liste_temps définie dans la fonction précédente en une seule valeur de temps en secondes. On ajoute alors ces valeurs à la liste vide. On définit une origine des temps correspondant à la première valeur de liste_secondes et on ajoute ensuite l'ensemble des valeurs auxquelles on a retiré l'origine dans une autre liste vide appelée liste_finale.

def conv_sec(liste_temps):
    liste_secondes = []
    for i in range(len(liste_temps)):
        liste_secondes += [liste_temps[i][0]*24*3600 + liste_temps[i][1]*3600 + liste_temps[i][2]*60 + liste_temps[i][3]]
    liste_finale = []
    origine = liste_secondes[0]
    for i in range(len(liste_secondes)):
        liste_finale += [liste_secondes[i]-origine]
    return liste_finale


# Dans l'énoncé, il est écrit "Avec éventuellement la possibilité de spécifier un intervalle de temps dans la ligne de commande" La fonction affichage permet ainsi d'afficher les courbes avec en ordonnée les valeurs d'une colonne variable du fichier Excel (noise, température,etc...) pour une expérience donnée id et en abscisse les temps correspondants. La fonction affichage permet également de spécifier un jour de début et un jour de fin grâce aux paramètres deb et fin. Etant donné que chaque expérience se déroule dans le même mois, il ne suffit de préciser que le jour pour la date de début et la date de fin.

def affichage(var,id,deb,fin):
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
    Y = colonne(var,id)[min:max+1]
    X = conv_sec(sent_at_date(id))[min:max+1]
    plt.plot(X,Y)
    plt.show()


# Problème de la fonction affichage : sa complexité en temps est beaucoup trop importante (plusieurs minutes) car nous manipulons dans la fonction des listes de listes. La fonction courbes ci-dessous est donc une version modifiée de la fonction affichage qui manipule des listes simples et non des listes de listes.

def courbes(var,id,deb,fin):
    min = -1
    max = -1
    jours = []
    for date in sent_at_date(id):
        jours += [date[0]]                                                 # On ajoute dans la liste vide jour l'ensemble des jours
    for i in range(len(jours)):                                            # correspondant à l'expérience choisie
        if jours[i] == deb:
            min = i
            break
    for j in range(len(jours)-1,-1,-1):
        if jours[j] == fin:
            max = j                                                        # On sélectionne ensuite les indices min et max
            break                                                          # correspondant au jour de début et au jour de fin
    if max==-1:
        print("il n'y a pas eu de relevé pour le jour"+str(fin))           # Il peut exister des jours où il n'y a pas eu de relevé
    if min==-1:                                                            # et cela peut créer des erreurs, d'où ces lignes
        print("il n'y a pas eu de relevé pour le jour"+str(deb))
    Y = colonne(var,id)[min:max+1]
    X = conv_sec(sent_at_date(id))[min:max+1]
    return X,Y

# La complexité en temps de cette fonction est raisonnable et permet d'obtenir les résultats rapidement.


# La fonction affichage2 permet enfin d'afficher les courbes.

def affichage2(var,id,deb,fin):
    X,Y = courbes(var,id,deb,fin)
    plt.plot(X,Y)
    plt.scatter(X,Y,10,'red')
    plt.xlabel("temps en secondes")
    plt.ylabel(var)
    plt.show()

## Affichage des valeurs statistiques sur la courbe


# La fonction min permet de trouver le minimum et d'afficher sur la courbe la valeur du minimum et l'ensemble des abscisses pour lesquelles ce minimum est atteint.

def min(var,id,deb,fin):
    X,Y = courbes(var,id,deb,fin)
    min =  Y[0]
    for val in Y:
        if val < min:
            min = val
    X_min = []
    Y_min = []
    for i in range(len(Y)):
        if Y[i] == min:
            X_min += [X[i]]
            Y_min += [Y[i]]
    plt.plot(X,Y)
    plt.xlabel("temps en secondes")
    plt.ylabel(var)
    plt.scatter(X_min,Y_min,s = 10,c ='red')
    plt.show()


# La fonction max permet de trouver le maximum et d'afficher sur la courbe la valeur du maximum et l'ensemble des abscisses pour lesquelles ce maximum est atteint.

def max(var,id,deb,fin):
    X,Y = courbes(var,id,deb,fin)
    max =  Y[0]
    for val in Y:
        if val > max:
            max = val
    X_max = []
    Y_max = []
    for i in range(len(Y)):
        if Y[i] == max:
            X_max += [X[i]]
            Y_max += [Y[i]]
    plt.plot(X,Y)
    plt.xlabel("temps en secondes")
    plt.ylabel(var)
    plt.scatter(X_max,Y_max,s = 10,c= 'red')
    plt.show()


# La fonction moy_arith permet de calculer la moyenne arithmétique d'une variable pendant une expérience et de superposer cette valeur sur la courbe représentant l'évolution de cette variable dans le temps.

def moy_arith(var,id,deb,fin):
    X,Y = courbes(var,id,deb,fin)
    moy = sum(Y)/len(Y)
    Y_moy = len(Y)*[moy]
    print(moy)
    plt.plot(X,Y)
    plt.plot(X,Y_moy,'r')
    plt.xlabel("temps en secondes")
    plt.ylabel(var)
    plt.show()


# La fonction variance permet de calculer et de retourner la variance d'une variable pendant une expérience. C'est une variable qu'on ne peut pas afficher.

def variance(var,id,deb,fin):
    X,Y = courbes(var,id,deb,fin)
    moy = sum(Y)/len(Y)
    vari = 0
    for i in range(len(Y)):
        vari += (Y[i]-moy)**2
    vari = vari/len(Y)
    return vari


# La fonction ecart_type permet de calculer l'écart-type d'une variable pendant une expérience. C'est une variable qu'on ne peut pas afficher.

def ecart_type(var,id,deb,fin):
    return variance(var,id,deb,fin)**0.5


# La fonction tri est la fonction faisant un tri à bulles d'une liste Y.

def tri(Y):
    n = len(Y)
    for i in range(n):
        for j in range(0, n-i-1):
            if Y[j] > Y[j+1] :
                Y[j], Y[j+1] = Y[j+1], Y[j]


# La fonction mediane utilise la fonction tri pour pouvoir déterminer la médiane d'une variable pendant une expérience et de superposer cette valeur sur la courbe représentant l'évolution de cette variable dans le temps.

def mediane(var,id,deb,fin):
    X,Y = courbes(var,id,deb,fin)
    plt.plot(X,Y)
    Y_tri = tri(Y)
    med = 0
    if len(Y)%2 == 1:
        med = Y[len(Y)//2]
    else:
        med = (Y[len(Y)//2-1]+Y[len(Y)//2])/2
    Y_med=len(Y)*[med]
    plt.plot(X,Y_med,'y')
    plt.xlabel("temps en secondes")
    plt.ylabel(var)
    plt.show()


## Calcul de l'indice humidex


# La fonction humidex calcule et retourne l'indice humidex correspondant à une température T et humidité relative en pourcentage H.

def humidex(T,H):
    H = H/100                                                                   #car c'est un poucentage
    a = 17.27
    b = 237.7
    Trosee = b*(a*T/(b+T)+log(H))/(a-(a*T/(b+T)+log(H)))
    return T + 0.5555*(6.11*exp(5417.7530*(1/273.16-1/(273.15+Trosee)))-10)


# La fonction courbe_humidex affiche l'évolution de l'indice humidex d'une expérience en fonction du temps grâce à la fonction humidex.

def courbe_humidex(id,deb,fin):
    X,temp = courbes("temp",id,deb,fin)
    X,humidity = courbes("humidity",id,deb,fin)
    hum = []
    for i in range(len(temp)):
        hum += [humidex(temp[i],humidity[i])]
    plt.plot(X,hum)
    plt.xlabel("temps en secondes")
    plt.ylabel("indice humidex")
    plt.show()


## Calcul l’indice de corrélation entre un couple de variables


# La fonction correlation calcule et affiche la valeur de l'indice de corrélation de deux variables pendant une expérience. De plus, la fonction affiche l'évolution de ces deux variables en fonction du temps sur le même graphe.

def correlation(var1,var2,id,deb,fin):
    X,Y1=courbes(var1,id,deb,fin)
    X,Y2=courbes(var2,id,deb,fin)
    e_t1 = variance(var1,id,deb,fin)**0.5
    e_t2 = variance(var2,id,deb,fin)**0.5
    cov=0
    Y1_moy=sum(Y1)/len(Y1)
    Y2_moy=sum(Y2)/len(Y2)
    for i in range(len(X)):
        cov+=(Y1[i]-Y1_moy)*(Y2[i]-Y2_moy)
    cov=cov/len(X)
    cor=cov/(e_t1*e_t2)
    print(cor)
    fig, ax1 = plt.subplots()                                                   # La fonction permet de créer deux axes des ordonnées
    ax1.plot(X,Y1, 'b')                                                         # pour les deux variables
    ax1.set_xlabel('temps (s)')
    ax1.set_ylabel(var1, color='b')
    ax2 = ax1.twinx()
    ax2.plot(X, Y2, 'r')
    ax2.set_ylabel(var2, color='r')
    plt.title("indice de corrélation : "+str(cor))
    plt.show()


## Relevé des anomalies


# La fonction anomalies permet d'afficher les valeurs anormales de la courbe d'une expérience donnée. On considère qu'une valeur est une anomalie dès lors que la différence entre cette valeur et celles qui la suit et qui la précède est supérieure à une valeur seuil. La valeur seuil choisie correspond à l'écart-type de la variable en question.


def anomalies(var,id,deb,fin):
    seuil = ecart_type(var,id,deb,fin)
    X,Y = courbes(var,id,deb,fin)
    X_anomalie = []
    Y_anomalie = []
    for i in range(1,len(Y)-1):
        diff1 = abs(Y[i]-Y[i-1])
        diff2 = abs(Y[i]-Y[i+1])
        if diff1 > seuil and diff2 > seuil and (Y[i]-Y[i-1])*(Y[i]-Y[i+1])>0:   # Une valeur est une anomalie uniquement si elle
            Y_anomalie += [Y[i]]                                                # présente un pic sur la courbe, d'où la dernière
            X_anomalie += [X[i]]                                                # condition
    plt.plot(X,Y)
    plt.scatter(X,Y,10,'red')
    plt.xlabel("temps en secondes")
    plt.ylabel(var)
    plt.scatter(X_anomalie,Y_anomalie,s = 50,c= 'orange')
    plt.show()