# -*- coding: utf-8 -*-

import os,os.path
import sys
import socket
from subprocess import Popen 
import math
from maquette_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy

class Controleur():
    def __init__(self):
        print("IN CONTROLEUR")
        self.createurId=Id
        self.projet=int(sys.argv[5])
        self.ad=sys.argv[4]
        self.nomUser = sys.argv[1]
        self.nomOrg = sys.argv[2]
        self.adBD = sys.argv[3]

        self.BD="Projet.smid"
        self.loginBD()
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.modele.chargerIdEtTitre()
        self.vue.root.mainloop()
        
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.adBD, allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.ad, allow_none=True)

    
    def creerNouvelleMaquette(self, titre):
        self.modele.creerNouvelleMaquette(titre)  
    
    def enregistrerBD(self):
        self.modele.enregistrerBD()
        
    def ouvrirMaquetteExistante(self, titre):
        self.modele.ouvrirMaquetteExistante(titre)
        
    def supprimerMaquette(self, titre):
        self.modele.supprimerMaquette(titre)

class Modele():
    def __init__(self, parent):
        self.parent=parent
        self.maquettes=[]
        self.maquetteActive=None
        self.IdEtTitre=[]
        self.formesImportees=[]
        
    def creerNouvelleMaquette(self, titre):
        m=Maquette(self.parent.projet, titre)
        self.maquettes.append(m)
        self.maquetteActive=m
        self.parent.vue.cadreDessin.pack()
    
    def enregistrerBD(self):
        if self.maquetteActive.idMaquette!=None:
            requete="DELETE FROM MaquetteAction WHERE idMaquette="+str(self.maquetteActive.idMaquette)
            self.parent.serveurBD.supprimerFormes(self.parent.BD, self.parent.nomUser, requete)
            for uneForme in self.maquetteActive.formes:
                vartest=str(self.maquetteActive.idMaquette) + "," + str(uneForme.idFigure) + "," + str(uneForme.x0) + "," + str(uneForme.y0) + "," + str(uneForme.x1) + "," + str(uneForme.y1) + ",'" + uneForme.texte + "'"                            
                requete="INSERT INTO MaquetteAction (idMaquette,type,x1,y1,x2,y2,texte) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.ajoutForme(self.parent.BD, self.parent.nomUser, requete)
            
        else:
            requete="INSERT INTO Maquette (Nom,idProjet) VALUES ('" + self.maquetteActive.titre + "'," + str(self.parent.projet) + ")"
            print(requete)
            self.maquetteActive.idMaquette=self.parent.serveurBD.ajoutMaquette(self.parent.BD, self.parent.nomUser, requete)
            for uneForme in self.maquetteActive.formes:
                vartest=str(self.maquetteActive.idMaquette) + "," + str(uneForme.idFigure) + "," + str(uneForme.x0) + "," + str(uneForme.y0) + "," + str(uneForme.x1) + "," + str(uneForme.y1) + ",'" + uneForme.texte + "'"
                requete="INSERT INTO MaquetteAction (idMaquette,type,x1,y1,x2,y2,texte) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.ajoutForme(self.parent.BD, self.parent.nomUser, requete)
        
    
    def chargerIdEtTitre(self):
        requete="SELECT id,Nom FROM Maquette WHERE idProjet="+str(self.parent.projet)
        self.IdEtTitre=self.parent.serveurBD.requeteIdEtTitreMaquette(self.parent.BD, self.parent.nomUser, requete)
        if self.IdEtTitre!="Vide" and self.IdEtTitre!="Erreur":
            for i in self.IdEtTitre:
                self.parent.vue.listbox.insert(END,i[1])
    
    
    def ouvrirMaquetteExistante(self, titre):
        self.creerNouvelleMaquette(titre)
        for i in self.IdEtTitre:
            if i[1]==self.maquetteActive.titre:
                self.maquetteActive.idMaquette=i[0]
        
        requete="SELECT type,x1,y1,x2,y2,texte FROM MaquetteAction WHERE idMaquette="+str(self.maquetteActive.idMaquette)
        self.formesImportees=self.parent.serveurBD.requeteFormesMaquette(self.parent.BD, self.parent.nomUser, requete)
        self.parent.vue.redessinerFormesImportees()
        
    def supprimerMaquette(self, titre):
        titreASupprimer=titre
        idASupprimer=None
        
        for i in self.IdEtTitre:
            if i[1]==titreASupprimer:
                idASupprimer=i[0]
                self.IdEtTitre.remove(i);
        
        if self.maquetteActive:
            if self.maquetteActive.idMaquette==idASupprimer:
                self.maquetteActive.idMaquette=None
        
        requete="DELETE FROM MaquetteAction WHERE idMaquette="+str(idASupprimer)
        self.parent.serveurBD.supprimerFormes(self.parent.BD, self.parent.nomUser, requete)
        
        requete="DELETE FROM Maquette WHERE id="+str(idASupprimer)
        self.parent.serveurBD.supprimerMaquette(self.parent.BD, self.parent.nomUser, requete)
        
        """
        self.creerNouvelleMaquette(titre)
        for i in self.IdEtTitre:
            if i[1]==self.maquetteActive.titre:
                self.maquetteActive.idMaquette=i[0]
                self.IdEtTitre.remove(i);
        
        requete="DELETE FROM MaquetteAction WHERE idMaquette="+str(self.maquetteActive.idMaquette)
        self.parent.serveurBD.supprimerFormes(self.parent.BD, self.parent.nomUser, requete)
        
        requete="DELETE FROM Maquette WHERE id="+str(self.maquetteActive.idMaquette)
        self.parent.serveurBD.supprimerMaquette(self.parent.BD, self.parent.nomUser, requete)
        
        self.maquettes.remove(self.maquetteActive)
        self.maquetteActive=None
        """
            
       
    
    
class Maquette():
    def __init__(self, idProjet, titre):
        self.idProjet=idProjet
        self.titre=titre
        self.idMaquette=None
        self.formes=[]
        
        
    def creerForme(self, idFigure, figure, x0, y0, x1, y1, tagUnique, texte):
        formeAAjouter = Forme(idFigure, figure, x0, y0, x1, y1, tagUnique, texte)
        self.formes.append(formeAAjouter)
        print("Nb de formes : " + str(len(self.formes)))
        
    
        
class Forme():
    def __init__(self, idFigure, figure, x0, y0, x1, y1, tagUnique, texte):
        self.idFigure=idFigure
        self.figure=figure
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1
        self.tagUnique=tagUnique
        self.texte=texte
        
if __name__ == '__main__':
    c=Controleur()