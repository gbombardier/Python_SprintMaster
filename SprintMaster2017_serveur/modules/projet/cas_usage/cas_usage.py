# -*- coding: utf-8 -*- #SQLLITE Viewer

import os,os.path
import sys
import Pyro4
import socket
from subprocess import Popen 
import math
#from sm_projet_modele import *
from cas_usage_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy
from _sqlite3 import sqlite_version
from tkinter import messagebox

class Controleur():
    def __init__(self):
        self.createurId=Id
        self.modele=None
        self.serveur=None
        self.serveurBD=None
        self.nomUser=sys.argv[1]
        self.nomOrg=sys.argv[2]
        self.adBD=sys.argv[3]
        self.ad=sys.argv[4]
        self.idProjet=int(sys.argv[5])
        self.nomBD="Projet.smid"
        self.loginBD()
        self.vue=Vue(self)
        self.IDTitre=0
        self.OrdreTitre=0
        self.IDinteraction=0
        self.OrdreInteraction=0
        self.titreCourant=""
        self.leCas=""
        self.vue.root.mainloop()
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.adBD,allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.ad,allow_none=True)
        
    def descriptionAfficher(self, selectioncourante):
        self.chaine='SELECT description FROM CasUserMachine WHERE description="'+str(selectioncourante)+'"'
        return self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
    
    def afficherLesCas(self):
        self.chaine="SELECT nom FROM CasUsage WHERE idProjet='"+str(self.idProjet)+"' ORDER BY ordre"
        return self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
    
    def afficherTitre(self):
        self.titrecas = self.vue.listecas.get(self.vue.listecas.curselection())
        self.chaine="SELECT nom FROM CasUsage WHERE nom="+str(self.titrecas)+'"'
        return self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
    
    def afficherInteractionMachine(self,titreCas):
        self.titrecas = self.vue.listecas.get(self.vue.listecas.curselection())
        self.chaine='SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.titrecas)+'") AND typeCas="ordinateur" ORDER BY ordre'
        return self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        
    def afficherInteractionUser(self, titreCas):
        self.titrecas= self.vue.listecas.get(self.vue.listecas.curselection())
        self.chaine='SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.titrecas)+'") AND typeCas="usager" ORDER BY ordre'
        return self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)

    def ajouterTitreBD(self):
        tabTitre= self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        for n in tabTitre:
            self.OrdreTitre+=1
        self.OrdreInteraction=0
        self.titrecourant = self.vue.titreInsertion.get()
        self.chaine = 'INSERT INTO CasUsage(idProjet,nom,ordre,TraiterMaquette,traiterCRC) VALUES ((SELECT id FROM Projet WHERE id='+str(self.idProjet)+'),"'+str(self.titrecourant)+'",'+str(self.OrdreTitre)+',0,0)'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)

    def ajouterCasOrdiBD(self, lecas):
        self.lecas= self.vue.casInsertion.get()
        self.chaine= 'SELECT id FROM CasUsage WHERE nom="'+str(self.titrecourant)+'"'
        self.idCas= self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        self.OrdreInteraction+=1
        self.chaine= "INSERT INTO CasUserMachine(idCas,typeCas,ordre,description) VALUES ('"+str(self.idCas[0][0])+"', 'ordinateur','"+str(self.OrdreInteraction)+"','"+str(lecas)+"');"        
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        
    def ajouterCasOrdiMENU(self):
        self.nbinteraction=1
        self.interaction=self.vue.entreeMachine.get()
        self.cas=self.vue.entreeTitre.get()
        self.chaine='SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'");'
        rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        for i in rep:
            self.nbinteraction+=1
        self.chaine= 'SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'"'
        rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        self.chaine="INSERT INTO CasUserMachine(idCas, typeCas,ordre,description) VALUES('"+str(rep[0][0])+"', 'ordinateur',"+str(self.nbinteraction)+",'"+str(self.interaction)+"');"
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        
    def ajouterCasUsagerMENU(self):
        self.nbinteraction=1
        self.interaction=self.vue.entreeUser.get()
        self.cas=self.vue.entreeTitre.get()
        self.chaine='SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'");'
        rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        for i in rep:
            self.nbinteraction+=1
        self.chaine= 'SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'"'
        rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        self.chaine="INSERT INTO CasUserMachine(idCas, typeCas,ordre,description) VALUES('"+str(rep[0][0])+"', 'usager',"+str(self.nbinteraction)+",'"+str(self.interaction)+"');"
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        
        
    def ajouterCasUsagerBD(self, lecas):
        self.OrdreInteraction+=1
        self.chaine= 'SELECT id FROM CasUsage WHERE nom="'+str(self.titrecourant)+'"'
        self.idCas= self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        self.chaine= 'INSERT INTO CasUserMachine(idCas,typeCas,ordre,description) VALUES ('+str(self.idCas[0][0])+', "usager",'+str(self.OrdreInteraction)+', "'+str(lecas)+'");'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
       
    def modifierDescription(self, vieuxTitre, nouveauTitre, cas):
        self.chaine= 'UPDATE CasUserMachine SET description="'+str(nouveauTitre)+'" WHERE description="'+str(vieuxTitre)+'" AND idCas=(SELECT id FROM CasUsage WHERE nom="'+str(cas)+'");'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        
    def modifierOrdre(self ,vieuxOrdre, nouveauOrdre, cas):
        self.nbInteractions=0;
        self.chaine = 'SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(cas)+'");'
        rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        for i in rep:
            self.nbInteractions+=1
        if nouveauOrdre>self.nbInteractions:
            messagebox.showinfo("Erreur", "Cette position est invalide")
        else: 
            self.chaine = 'SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(cas)+'") AND ordre>='+str(nouveauOrdre)+';'
            rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
            self.chaine= 'UPDATE CasUserMachine SET ordre="'+str(nouveauOrdre)+'" WHERE ordre="'+str(vieuxOrdre)+'" AND idCas=(SELECT id FROM CasUsage WHERE nom="'+str(cas)+'");'
            self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
            #inserer boucle FOR afin de calculer le nombre d'elements dans rep (paske "i in range(rep)" marche pas)
            for i in rep:
                self.description=i[0]
                self.ordre=i[1]
                self.ordreAjoute=i[1]+1
                if self.ordre<=vieuxOrdre:
                    self.chaine='UPDATE CasUserMachine SET ordre='+str(self.ordreAjoute)+' WHERE description="'+str(self.description)+'" AND idCas=(SELECT id FROM CasUsage WHERE nom="'+str(cas)+'") AND ordre='+str(self.ordre)+';'
                    self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
                
    def afficherOrdre(self, description, cas):
        self.chaine= 'SELECT ordre FROM CasUserMachine WHERE description="'+str(description)+'" AND idCas=(SELECT id FROM CasUsage WHERE nom="'+str(cas)+'");'
        return self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        

    def modifierTitre(self, vieuxTitre, nouveauTitre):
        self.chaine = 'UPDATE CasUsage SET nom="'+str(nouveauTitre)+'" WHERE nom="'+str(vieuxTitre)+'"'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)

    def deleteTitreBD(self):
        self.nom =self.vue.listecas.get(self.vue.listecas.curselection())       
        self.chaine = 'DELETE from CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.nom)+'")'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        self.chaine = 'DELETE from CasUsage WHERE nom="'+str(self.nom)+'"'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        
    def deleteCasUserMachine(self):
        self.cas=self.vue.entreeTitre.get()
        self.ordre=self.vue.entreeOrdre.get()
        self.chaine = 'SELECT description, ordre FROM CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'") AND ordre>='+str(self.ordre)+';'
        rep=self.serveurBD.selectCasUsage(self.nomUser,self.nomBD,self.chaine)
        for i in rep:
            self.description=i[0]
            self.ordre=i[1]
            self.nouveauOrdre=i[1]-1
            self.chaine='UPDATE CasUserMachine SET ordre='+str(self.nouveauOrdre)+' WHERE description="'+str(self.description)+'" AND idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'")AND ordre='+str(self.ordre)+';'
            self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)
        self.nom=self.vue.entreeDescription.get()
        self.chaine = 'DELETE from CasUserMachine WHERE idCas=(SELECT id FROM CasUsage WHERE nom="'+str(self.cas)+'") AND description="'+str(self.nom)+'"'
        self.serveurBD.modificationCasUsage(self.nomUser, self.nomBD, self.chaine)

    def requeteModules(self,mod):
        rep=self.serveur.requeteProjet(mod)
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
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.nomUser, self.nomOrg,self.adBD,self.ad,str(self.idProjet)],shell=1 ).pid 
            self.vue.fermerfenetre()
        else:
            pass
    
       
class CasUsage():
    def __init__(self, nom, id, idprojet, ordre,maquette):
        self.nom=nom
        self.id=id
        self.idprojet=idprojet
        self.ordre=ordreself.maquette=maquette
        
class CasUserMachine():
    def __init__(self, id, idCas, typeCas, ordre, description):
        self.id=id
        self.idCas=idCas
        self.ordre=ordre
        self.description=description
        


if __name__ == '__main__':
    c=Controleur()