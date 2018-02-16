# -*- coding: utf-8 -*-

import os,os.path
import sys
import socket
from subprocess import Popen 
from xmlrpc.client import ServerProxy
import math
#from sm_projet_modele import *
from crc_vue import *

from IdMaker import Id


class Controleur():
    def __init__(self):
        print("IN CONTROLEUR de CRC")
        self.createurId=Id
        self.modele = Modele(self,sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
#         self.nomUser="Gab"
#         self.nomOrg="CVM"
#         self.adBD="http://10.57.47.22:9998"
#         self.ad="http://10.57.47.22:9999"
#         self.idProjet="1"
#         self.modele = Modele(self, self.nomUser,self.nomOrg,self.adBD,self.ad,self.idProjet)
        self.serveurBD = None
        self.serveur = None
        self.loginBD()
        self.importCRC()

        self.vue=Vue(self,self.modele)
        self.vue.root.mainloop()
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.modele.adBD,allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.modele.ad)
#         rep=self.serveurBD.loginauserveur(self.nomUser,self.nomOrg)
         
    def importCRC(self):
        requeteSELECT = "SELECT id, nomClasse, proprietaire FROM crc WHERE idProjet = " + str(self.modele.idProjet);
        print(requeteSELECT)
        rep = self.serveurBD.requeteSelect(requeteSELECT,"Projet.smid",self.modele.nomUser)
        listeCollab=[]
        print(rep)
        if rep == "Vide" or rep == "Erreur":
            rep = [];
        else:
            for crc in rep:
                requeteCOLLAB = "SELECT idCRC2 FROM collaboration WHERE idCRC1 = " + str(crc[0])
                repcollab = self.serveurBD.requeteSelect(requeteCOLLAB,"Projet.smid",self.modele.nomUser)
                if repcollab != "Vide":
                    for col in repcollab:
                        listeCollab.append(col)
                    print(col)
                else:
                    listeCollab = []
                self.modele.ajoutCRCexistant(crc[0],crc[1],crc[2],listeCollab)
        
    def enregistrerCRC(self, nomClasse, proprietaire,collaborateurs):
        requeteINSERT = "INSERT INTO crc(nomClasse,proprietaire,idProjet) VALUES ('" + nomClasse + "',(SELECT id FROM Employe WHERE nom ='"+proprietaire+"')," + str(self.idProjet) + ")"
        rep = self.serveurBD.nouveauCRC(requeteINSERT,"Projet.smid", self.nomUser)
        
            
        if rep == "Erreur":
           return None
        else:
            for collab in collaborateurs:
                requeteINSERT = "INSERT INTO collaboration(idCRC1,idCRC2) VALUES (" + str(rep) + ",(SELECT id FROM crc WHERE nom='" + str(collab) + "'))"
                id = self.serveurBD.nouveauCRC(requeteINSERT,"Projet.smid",self.nomUser)
            return rep
    
    def ajoutCollab(self, id, collab):
        for crc in self.modele.listeCRC:
            if crc.nom == collab:
                collab = crc.id
                requeteMODIF = "INSERT INTO Collaboration (idCRC1, idCRC2) VALUES ("+str(id)+","+str(crc.id)+")"
                rep = self.serveurBD.nouveauCRC(requeteMODIF,"Projet.smid", self.nomUser)
                if rep:
                    for crc in self.modele.listeCRC:
                        if crc.id == id:
                            crc.collaboration.append(crc.id)
                            return "Le collaborateur est ajouté."
        return "Le collaborateur n'existe pas."
     
    def requeteModules(self,mod):
        rep=self.serveur.requeteProjet(mod)
        if rep:
            print(rep[0])
            cwd=os.getcwd()
            lieuApp="/../"+rep[0]
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
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.modele.nomUser, self.modele.nomOrg,self.modele.adBD,self.modele.ad,self.modele.idProjet],shell=1 ).pid 
        else:
            print("RIEN") 
            
    def chargerModules(self):
        rep=self.serveur.obtenirModules()   # on averti le serveur de nous inscrire
        print("reponse du serveur",rep)
        self.vue.chargerModules(rep[2]) 
        
class CRC():
    def __init__(self, nom, proprietaire, collaborateurs, id=None):
        self.id = id
        self.nom = nom
        self.proprietaire = proprietaire
        self.collaboration = []
        
        for collab in collaborateurs:
            self.collaboration.append(collab)
        
class Modele():
    def __init__(self,parent,nomuser,nomorg,adbd,ad,idprojet):
        self.controleur = parent
        self.nomUser=nomuser
        self.nomOrg=nomorg
        self.adBD=adbd
        self.ad=ad
        self.idProjet=int(idprojet)
        self.listeCRC = []
        self.nouveauCRC = None
        
    
    def ajoutCRC(self, nom,proprietaire,collaborateurs):
        for crc in self.listeCRC:
            if crc.nom == nom:
                return "Le nom de la classe est déjà utilisé."
        
        self.nouveauCRC = CRC(nom,proprietaire,collaborateurs)
        rep = self.controleur.enregistrerCRC(self.nouveauCRC.nom,self.nouveauCRC.proprietaire,self.nouveauCRC.collaboration)
        self.nouveauCRC.id=rep
        self.listeCRC.append(self.nouveauCRC)
        return "CRC créé."
        
    def ajoutCRCexistant(self, id, nom, proprietaire,collaborateurs):
        self.listeCRC.append(CRC(nom,proprietaire,collaborateurs,int(id)))
        
if __name__ == '__main__':
    c=Controleur()