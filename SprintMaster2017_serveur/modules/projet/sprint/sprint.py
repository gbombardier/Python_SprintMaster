# -*- coding: utf-8 -*-

import os,os.path
import sys
import Pyro4
import socket
from subprocess import Popen 
import math
#from sm_projet_modele import *
from sprint_modele import *
from sprint_vue import *
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
        self.idProjet=sys.argv[5]
        #self.nomUser="Gab"
        #self.nomOrg="CVM"
        #self.adBD="http://10.57.47.17:9998"
        #self.ad="http://10.57.47.17:9999"
        #self.idProjet="1"
        self.serveur=None
        self.serveurBD=None
        self.loginBD()
        #self.test()
        self.modele=Modele(self)
        self.vue=Vue(self,self.modele)
        self.vue.root.mainloop()
               
    def retournerListe(self, requete,BD):
        rep= self.serveur.retournerListe(requete, BD)
        
        if rep == "Vide" or rep == "Erreur":
            rep = []
        return rep
    
    def trouverIndexSous(self,current,idTache):
        return self.modele.trouverIndexSous(current,idTache)
       
    def trouverIndex(self,current):
        return self.modele.trouverIndex(current)
        
    def loadData(self,requete):
        rep=self.serveurBD.requeteSelect(requete,self.BD,self.nomUser)
        if rep == "Vide" or rep == "Erreur":
            rep = []
        return rep
    
    def modifSousTache(self,idTache,idSousTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        self.modele.modifSousTache(idTache,idSousTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
    
    def ajoutSousTache(self,idTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        return self.modele.ajoutSousTache(idTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
    
    def modification(self,requete):
        return self.serveurBD.modification(self.BD,requete,self.nomUser)
    
    def test(self):
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "salut" + "','" + "24" + "','"+ "2"+ "','" + "1" + "','" + "Bas"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+"bonjour" + "','" + "24" + "','" +"2"+ "','" + "3" + "','" + "Urgent"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "salut1" + "','" + "24" + "','"+ "2"+ "','" + "1" + "','" + "Bas"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+"bonjour1" + "','" + "24" + "','" +"2"+ "','" + "3" + "','" + "Urgent"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "salut2" + "','" + "24" + "','"+ "2"+ "','" + "1" + "','" + "Bas"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+"bonjour3" + "','" + "24" + "','" +"2"+ "','" + "3" + "','" + "Urgent"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "salut4" + "','" + "24" + "','"+ "2"+ "','" + "1" + "','" + "Moyen"+ "','" + self.idProjet + "')")
        self.ajout("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+"bonjour4" + "','" + "24" + "','" +"2"+ "','" + "3" + "','" + "Urgent"+ "','" + self.idProjet + "')")
        
      
    def ajout(self,requete):
        return self.serveurBD.ajout(self.BD,requete,self.nomUser)
       
    def loginBD(self):
        self.serveurBD=ServerProxy(self.adBD,allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.ad,allow_none=True)
        #rep=self.serveurBD.loginauserveur(self.nomUser,self.nomOrg)
       
    def requeteSelect(self, requete):
        rep=self.serveurBD.requeteSelect(requete,self.BD,self.nomUser)
        return rep
    
    def requeteModules(self,mod):
        rep=self.serveur.requetemodule(mod)
        if rep:
            print(rep[0])
            cwd=os.getcwd()
            lieuApp="/"+rep[0]
            lieu=cwd+lieuApp
            print(lieu)
            if not os.path.exists(lieu):
                os.mkdir(lieu) #plante s'il exist deja
            reso=rep[1]
            print(rep[1])
            for i in rep[2]:
                if i[0]=="fichier":
                    nom=reso+i[1]
                    rep=self.serveur.requetefichier(nom)
                    fiche=open(lieu+"/"+i[1],"wb")
                    fiche.write(rep.data)
                    fiche.close()
            chaineappli="."+lieuApp+lieuApp+".py"
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.monnom, self.monOrg,self.adBD,self.ad,self.vue.idProjet],shell=1 ).pid 
        else:
            print("RIEN") 
            
    def chargerModules(self):
        rep=self.serveur.obtenirModules()   # on averti le serveur de nous inscrire
        print("reponse du serveur",rep)
        self.vue.chargerModules(rep[2]) 
       
if __name__ == '__main__':
    c=Controleur()