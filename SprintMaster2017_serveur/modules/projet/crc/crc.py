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
        self.importResp()

        self.vue=Vue(self,self.modele)
        self.vue.root.mainloop()
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.modele.adBD,allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.modele.ad)
#         rep=self.serveurBD.loginauserveur(self.nomUser,self.nomOrg)
         
    def importCRC(self):
        requeteSELECT = "SELECT id, nomClasse, proprietaire FROM crc WHERE idProjet = " + str(self.modele.idProjet)
        rep = self.serveurBD.requeteSelect(requeteSELECT,"Projet.smid",self.modele.nomUser)
        listeCollab=[]
        if rep == "Vide" or rep == "Erreur":
            rep = [];
        else:
            for crc in rep:
                requeteCOLLAB = "SELECT idCRC2 FROM collaboration WHERE idCRC1 = " + str(crc[0])
                repcollab = self.serveurBD.requeteSelect(requeteCOLLAB,"Projet.smid",self.modele.nomUser)
                if repcollab != "Vide":
                    for col in repcollab:
                        listeCollab.append(col[0])
                else:
                    listeCollab = []
                self.modele.ajoutCRCexistant(crc[0],crc[1],crc[2],listeCollab)
    def importResp(self):
        requeteSELECT = "SELECT id, nom, idCrc, previsionHre, sprintVise, priorite, idProjet FROM responsabilite WHERE idProjet = " + str(self.modele.idProjet)
        rep = self.serveurBD.requeteSelect(requeteSELECT, "Projet.smid", self.modele.nomUser)
        if rep != "Vide":
            for resp in rep:
                self.modele.listeResp.append(Responsabilite(resp[2],resp[1],resp[3],resp[4],resp[5],resp[0]))
        
    def enregistrerCRC(self, nomClasse, proprietaire,collaborateurs):
        requeteINSERT = "INSERT INTO crc(nomClasse,proprietaire,idProjet) VALUES ('" + nomClasse + "',(SELECT id FROM Employe WHERE nom ='"+proprietaire+"')," + str(self.modele.idProjet) + ")"
        rep = self.serveurBD.nouveauCRC(requeteINSERT,"Projet.smid", self.modele.nomUser)
            
        if rep == "Erreur":
           return None
        else:
            for collab in collaborateurs:
                requeteINSERT = "INSERT INTO collaboration(idCRC1,idCRC2) VALUES (" + str(rep) + ",(SELECT id FROM crc WHERE nom='" + str(collab) + "'))"
                id = self.serveurBD.nouveauCRC(requeteINSERT,"Projet.smid",self.modele.nomUser)
            return rep
    
    def ajoutCollab(self, id, collab):
        for crc in self.modele.listeCRC:
            if crc.nom == collab:
                collab = crc.id
                requeteMODIF = "INSERT INTO Collaboration (idCRC1, idCRC2) VALUES ("+str(id)+","+str(crc.id)+")"
                rep = self.serveurBD.nouveauCRC(requeteMODIF,"Projet.smid", self.modele.nomUser)
                for crc2 in self.modele.listeCRC:
                    if crc2.id == id:
                        crc2.collaboration.append(crc.id)
                        return "Le collaborateur est ajouté."
        return "Le collaborateur n'existe pas."
    
    def ajoutResp(self,idCRC,nom, nomCas):
        if nomCas == "Pas un cas d'usage":
            pass
        else:
            for cas in self.modele.listeCas:
                if cas[0] == nomCas:
                    nomCas = cas[2]
        
            requeteUpdate = "UPDATE CasUsage SET traiterCRC=1 WHERE id=" + str(nomCas)
            rep = self.serveurBD.modificationCasUsage(self.modele.nomUser, "Projet.smid", requeteUpdate)
            self.vue.importerCasUsage()
        
        requeteRESP = "INSERT INTO Responsabilite (nom, idCrc, previsionHre, sprintVise, priorite, idProjet) VALUES ('" + str(nom) + "'," + str(idCRC) + ",0,1,'Urgent'," + str(self.modele.idProjet) + ")"
        rep = self.serveurBD.nouveauCRC(requeteRESP,"Projet.smid",self.modele.nomUser)
        self.modele.ajoutResp(nom, idCRC,rep)
        
    def importerCasUsage(self):
        requeteSELECT = "SELECT nom, traiterCRC, id FROM CasUsage WHERE idProjet =" + str(self.modele.idProjet)
        rep = self.serveurBD.requeteSelect(requeteSELECT, "Projet.smid", self.modele.nomUser)
        self.modele.listeCas = []
        for cas in rep:
            self.modele.listeCas.append(cas)
        return self.modele.listeCas
        
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
            pid = Popen(["C:\\Python34\\Python.exe", chaineappli, self.modele.nomUser, self.modele.nomOrg,self.modele.adBD,self.modele.ad,str(self.modele.idProjet)],shell=1 ).pid 
            self.vue.fermerfenetre()
        else:
            pass 
            
    
class CRC():
    def __init__(self, nom, proprietaire, collaborateurs, id=None):
        self.id = id
        self.nom = nom
        self.proprietaire = proprietaire
        self.collaboration = []
        
        for collab in collaborateurs:
            self.collaboration.append(collab)
            
class Responsabilite():
    def __init__(self, idCRC, nom, previsionHre, sprintVise, priorite, idProjet, id=None):
        self.idCRC= idCRC
        self.nom=nom
        self.previsionHre = previsionHre
        self.sprintVise = sprintVise
        self.priorite = priorite
        self.idProjet = idProjet
        self.id = id
        
class Modele():
    def __init__(self,parent,nomuser,nomorg,adbd,ad,idprojet):
        self.controleur = parent
        self.nomUser=nomuser
        self.nomOrg=nomorg
        self.adBD=adbd
        self.ad=ad
        self.idProjet=int(idprojet)
        self.listeCRC = []
        self.listeResp = []
        self.listeCas = []
        self.nouveauCRC = None
        
    def ajoutResp(self,nom,idCRC,id):
        self.listeResp.append(Responsabilite(idCRC, nom, 0,0,"",self.idProjet,int(id)))
        
    def ajoutCRC(self, nom,proprietaire,collaborateurs):
        for crc in self.listeCRC:
            if crc.nom == nom:
                return "Le nom de la classe est déjà utilisé."
        
        self.nouveauCRC = CRC(nom,proprietaire,collaborateurs)
        rep = self.controleur.enregistrerCRC(self.nouveauCRC.nom,self.nouveauCRC.proprietaire,self.nouveauCRC.collaboration)
        self.nouveauCRC.id=rep
        self.listeCRC.append(self.nouveauCRC)
        return self.nouveauCRC
        
    def ajoutCRCexistant(self, id, nom, proprietaire,collaborateurs):
        self.listeCRC.append(CRC(nom,proprietaire,collaborateurs,int(id)))
        
if __name__ == '__main__':
    c=Controleur()