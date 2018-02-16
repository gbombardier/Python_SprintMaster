# -*- coding: utf-8 -*-

import os,os.path
import sys
import Pyro4
import socket
from subprocess import Popen 
import math

from planif_vue import *
from planif_modele import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy
from _sqlite3 import sqlite_version

class Controleur():
    def __init__(self):
        print("IN CONTROLEUR")
        self.nomUser=sys.argv[1]
        self.nomOrg=sys.argv[2]
        self.adBD = sys.argv[3]
        self.ad = sys.argv[4]
        self.idProjet=sys.argv[5]
        self.nomBD = "Projet.smid"
        self.loginBD()
        self.createurId=Id
        self.modele=Modele(self)
        self.vue=Vue(self, sys.argv[1], sys.argv[2],self.idProjet )
        self.vue.root.mainloop()
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.adBD,allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.ad,allow_none=True)  
       
    def retournerListe(self, requete,BD):
        return self.serveurBD.requeteSelect(requete, BD, self.nomUser)
    
    def ajoutRespo(self, idCrc, nom, prio, sprint, temps):
        self.modele.ajoutRespo(idCrc, nom, prio, sprint, temps)   
    
    def requeteSQL(self, requete, BD, usager):
        self.serveurBD.modificationCasUsage(usager, BD, requete)
         
if __name__ == '__main__':
    c=Controleur()