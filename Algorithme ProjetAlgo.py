# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:03:30 2020

@author: mupat
"""

f = open("EIVP_KM.csv","r")
ligne = f.readline()
f.close()

def colonne(n):
    f = open("EIVP_KM.csv","r")
    liste = []
    f.readline()
    while f.readline() != '':
        ligne = f.readline()
        #fonction qui les points virgules qu'on veut

        dazeradf



