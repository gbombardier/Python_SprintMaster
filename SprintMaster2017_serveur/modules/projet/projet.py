# -*- coding: utf-8 -*-

import os,os.path
import sys
import Pyro4
import socket
from subprocess import Popen 
import math
#from sm_projet_modele import *
from projet_vue import *
from projet_modele import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy
from _sqlite3 import sqlite_version

class Controleur():
    def __init__(self):
        print("IN CONTROLEUR")
        self.createurId=Id
        self.BD="Projet.smid"
        self.nomUser=sys.argv[1]
        self.nomOrg=sys.argv[2]
        self.adBD=sys.argv[3]
        self.ad=sys.argv[4]
        self.monip = sys.argv[5]
        #self.nomUser="Gab"
        #self.nomOrg="CVM"
        #self.adBD="http://10.57.47.22:9998"
        #self.ad="http://10.57.47.22:9999"
        self.serveur=None
        self.serveurBD=None
        self.loginBD()
        self.modele=Modele(self)
        self.vue=Vue(self,self.modele, self.nomOrg)
        self.vue.root.mainloop()
        
    def ajoutProjet(self,req):
        return self.serveurBD.ajout(self.BD,req,self.nomUser)
     
    def retournerListe(self, requete,BD):
        rep= self.serveur.retournerListe(requete, BD)
        
        if rep == "Vide" or rep == "Erreur":
            rep = []
        return rep
    
    def modificationProjet(self,req):
        self.serveurBD.modification(self.BD,req,self.nomUser)
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.adBD,allow_none=True) # se connecter au serveur
        #self.serveurBD.loginauserveur(self.nomUser,self.nomOrg);
        self.serveur=ServerProxy(self.ad)
        
        #ad="http://"+self.monip+":9999" # construire la chaine de connection
        #self.serveurMachine=ServerProxy(ad) # se connecter au serveur
       
    def requeteSelect(self, requete):
        rep=self.serveurBD.requeteSelect(requete,self.BD,self.nomUser)
        if rep == "Vide" or rep == "Erreur":
            rep = []
        return rep
    
    def requeteModules(self,mod):
        rep=self.serveur.requeteProjet(mod)
        if rep:
            print(rep[0])
            cwd=os.getcwd()
            lieuApp="/"+rep[0]
            lieu=cwd+lieuApp
            print(lieu)
            if not os.path.exists(lieu):
                os.mkdir(lieu) #plante s'il exist deja
            reso=rep[1]
            for i in rep[2]:
                if i[0]=="fichier":
                    nom=reso+i[1]
                    print("DODODOO",nom)
                    rep=self.serveur.requetefichier(nom)
                    fiche=open(lieu+"/"+i[1],"wb")
                    fiche.write(rep.data)
                    fiche.close()
            chaineappli="."+lieuApp+lieuApp+".py"
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.nomUser, self.nomOrg,self.adBD,self.ad,str(self.vue.idProjet)],shell=1).pid 
            self.vue.fermerfenetre()
        else:
            print("RIEN") 
            
    def chargerModules(self):
        rep=self.serveur.obtenirModules()   # on averti le serveur de nous inscrire
        print("reponse du serveur",rep)
        self.vue.chargerModules(rep[2]) 
        
if __name__ == '__main__':
    c=Controleur()