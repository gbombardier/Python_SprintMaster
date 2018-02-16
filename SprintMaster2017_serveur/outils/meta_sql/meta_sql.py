# -*- coding: utf-8 -*-

import os,os.path
import sys
import socket
from subprocess import Popen 
from xmlrpc.client import ServerProxy
import math
#from sm_projet_modele import *
from meta_sql_vue import *
from helper import Helper as hlp
from IdMaker import Id


class Controleur():
    def __init__(self):
        print("IN CONTROLEUR")
        self.createurId=Id
        self.nomUser=sys.argv[1]
        self.nomOrg=sys.argv[2]
        self.adBD=sys.argv[3]
#         self.nomUser="Gab"
#         self.nomOrg="CVM"
#         self.adBD="http://10.57.47.22:9998"
        self.serveurBD = None
        self.loginBD()
        self.modele=Modele(self.nomUser, self.nomOrg)
        self.vue=Vue(self)
        self.vue.root.mainloop()


    def loginBD(self):
        self.serveurBD=ServerProxy(self.adBD) # se connecter au serveur
#         rep=self.serveurBD.loginauserveur(self.nomUser,self.nomOrg)


    def chargerBD(self):
        rep = self.serveurBD.lireBD(self.nomUser)
        # rep[x][y][z]
        # x = 0: nom du dossier de l'organisation 1 = liste des fichiers
        # y = liste des fichiers ou dossiers
        # z = [type de fichier/dossier, nom du fichier/dossier]
        self.dossierOrg = rep[0]
        self.listeBD=[]
        for i in rep[1]:
            if i[0] == "fichier":
                self.listeBD.append(i[1])
        return self.listeBD

    def nouvelleBD(self,nomBD):
        rep = self.serveurBD.nouvelleBD(self.nomUser, nomBD)
        if rep == 1:
            rep = "BD crée."
            self.vue.refresh()
        else:
            rep = "Nom déja pris."
        return rep

    def ouvrirBD(self, choix):
        self.bd = choix
        self.bdpath = self.dossierOrg + '/' + choix + '.smid'
        rep = self.serveurBD.listeTable(self.nomUser, self.bd, self.bdpath)
        return rep
    
    def supprimerBD(self,nomBD):
        rep = self.serveurBD.supprimerBD(self.nomUser,nomBD)
        return rep
    
    def nouvelleTable(self,nomTable,champTable):
        nomBD = self.modele.BDcourante
        rep = self.serveurBD.nouvelleTable(self.nomUser, nomBD, nomTable, champTable)
        return rep
    
    def supprimerTable(self):
        print(self.modele.BDcourante, self.modele.tablecourante)
        rep = self.serveurBD.supprimerTable(self.nomUser,self.modele.BDcourante,self.modele.tablecourante)
        
    def listeInsertions(self, choix):
        self.table = choix
        rep = self.serveurBD.listeInsertions(self.nomUser,self.bd,self.bdpath,self.table)
        return rep
        
class Modele():
    def __init__(self,nom,organisation):
        self.nom = nom
        self.organisation = organisation
        self.BDcourante = None
        self.tablecourante = None

if __name__ == '__main__':
    c=Controleur()