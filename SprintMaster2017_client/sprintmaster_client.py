# -*- coding: utf-8 -*-

import os,os.path
import sys
from xmlrpc.client import ServerProxy
import socket
from subprocess import Popen 
import math
from sprintmaster_modele import *
from sprintmaster_vue import *
from helper import Helper as hlp
from IdMaker import Id
import sqlite3
class Controleur():
    def __init__(self):
        self.monip=self.trouverIP()
        self.connecterClient()
        self.createurId=Id
        self.modele=None
        self.serveur=None
        self.ipBD=None
        self.adBD=None
        #self.serveurMachine=None
        self.vue=Vue(self,self.monip)
        self.vue.root.mainloop()
       
    #Enlever les commentaires lors de la création des BD
    def connecterClient(self):
        ad="http://"+self.monip+":9999" # construire la chaine de connection
        self.serveurMachine=ServerProxy(ad) # se connecter au serveur
        
        if(os.path.isfile("../SprintMaster2017_serveur/organisations.smid")):
            if(os.path.isfile("../SprintMaster2017_serveur/usagers.smid")):
                pass
            else:
               self.creerBDUsagers() 
        else:
            self.creerBDOrg()
            if(os.path.isfile("../SprintMaster2017_serveur/usagers.smid")):
                pass
            else:
                self.creerBDUsagers()
            
    def creerBDOrg(self):
        self.serveurMachine.nouvelleBD("organisations.smid")
        self.serveurMachine.requeteSQL("CREATE TABLE if not exists organisations (nom text,telephone text, adresse text, responsable text, statut text)", "organisations.smid")
        
    def creerBDUsagers(self):
        self.serveurMachine.nouvelleBD("usagers.smid")
        self.serveurMachine.requeteSQL("CREATE TABLE if not exists clients (organisation text, identifiant text, nom text, telephone text, adresse text, courriel text, role text, statut text)", "usagers.smid")  
        
    def retournerListe(self, requete, nomBD):
        rep = self.serveurMachine.retournerListe(requete, nomBD)
        return rep
        
    def trouverIP(self): # fonction pour trouver le IP en 'pignant' gmail
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # on cree un socket
        s.connect(("gmail.com",80))    # on envoie le ping
        monip=s.getsockname()[0] # on analyse la reponse qui contient l'IP en position 0 
        s.close() # ferme le socket
        return monip
    
    def loginclient(self,ipserveur,nom, org):
        if ipserveur and nom and org:
            self.ad="http://"+ipserveur+":9999" # construire la chaine de connection
            self.serveur=ServerProxy(self.ad) # se connecter au serveur
            self.monnom=nom
            self.monOrg=org
            rep=self.serveur.loginauserveur(self.monnom, self.monOrg)    # on averti le serveur de nous inscrire
            self.vue.chargercentral(rep[2],rep[3])
    
    def loginBD(self,ipbd, nom, org):
        if ipbd:
            self.ipBD=ipbd
            self.adBD="http://"+ipbd+":9998" # construire la chaine de connection
            self.serveurBD=ServerProxy(self.adBD) # se connecter au serveur
            self.monnom=nom
            self.monOrg=org
            rep=self.serveurBD.loginauserveur(self.monnom,self.monOrg)
            if org != "":
                self.serveurBD.nouvelleBD(self.monnom,"Projet")
            
    def requeteSQL(self, requete, nomBD):
        self.serveurMachine.requeteSQL(requete, nomBD)

            
    def requeteoutils(self,mod):      
        rep=self.serveur.requeteoutils(mod)
        if rep:
            cwd=os.getcwd()
            lieuApp="/"+rep[0]
            lieu=cwd+lieuApp
            if not os.path.exists(lieu):
                os.mkdir(lieu) #plante s'il exist deja
            reso=rep[1]
            for i in rep[2]:
                if i[0]=="fichier":
                    nom=reso+i[1]
                    rep=self.serveur.requetefichier(nom)
                    fiche=open(lieu+"/"+i[1],"wb")
                    fiche.write(rep.data)
                    fiche.close()
            chaineappli="."+lieuApp+lieuApp+".py"
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.monnom, self.monOrg, self.adBD,self.ad, self.monip],shell=1).pid 
        else:
            pass
            
    def requetemodule(self,mod):
        rep=self.serveur.requetemodule(mod)
        if rep:
            cwd=os.getcwd()
            lieuApp="/"+rep[0]
            lieu=cwd+lieuApp
            if not os.path.exists(lieu):
                os.mkdir(lieu) #plante s'il exist deja
            reso=rep[1]
            for i in rep[2]:
                if i[0]=="fichier":
                    nom=reso+i[1]
                    rep=self.serveur.requetefichier(nom)
                    fiche=open(lieu+"/"+i[1],"wb")
                    fiche.write(rep.data)
                    fiche.close()
            chaineappli="."+lieuApp+lieuApp+".py"
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.monnom, self.monOrg,self.adBD,self.ad, self.monip],shell=1 ).pid
        else:
            pass
            
        
    def connecteservice(self,rep):  # initalisation locale de la simulation, creation du modele, generation des assets et suppression du layout de lobby
        if rep[1][0][0]=="connecte":
            self.modele=Modele(self,rep[1][0][1],rep[1][0][2]) # on cree le modele
            self.vue.afficherinitpartie(self.modele)

            
    def fermefenetre(self):
        if self.serveur:
            self.serveur.jequitte(self.monnom)
        self.vue.root.destroy()
        
        
if __name__=="__main__":
    c=Controleur()
    c.connecterClient()