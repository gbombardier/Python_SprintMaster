# -*- coding: utf-8 -*-

import os,os.path
import sys
import socket
from subprocess import Popen 
import math
from mandat_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy

class Controleur():
    def __init__(self):
        print("IN CONTROLEUR")
        self.createurId=Id
        self.modele = Modele(self,sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        self.BD="Projet.smid"
        self.loginBD()
        self.vue=Vue(self)
        self.modele.importerMandat()
        self.vue.root.mainloop()
        
        
    def loginBD(self):
        self.serveurBD=ServerProxy(self.modele.adBD, allow_none=True) # se connecter au serveur
        self.serveur=ServerProxy(self.modele.ad, allow_none=True)
    
    

class Modele():
    def __init__(self, parent, nomUser, nomOrg, adBD, ad, idProjet):
        self.parent=parent
        self.idProjet= idProjet
        self.nomUser = nomUser
        self.nomOrg = nomOrg
        self.adBD = adBD
        self.ad = ad
        self.mandatActif=None
        
    
    def importerMandat(self):
        requete="SELECT id,nom FROM FichierTxt WHERE idProjet="+str(self.idProjet)
        reponse=self.parent.serveurBD.requeteSelect(requete, self.parent.BD, self.nomUser)
        
        if reponse=="Vide" or reponse=="Erreur":
            self.parent.vue.creerMandat()
            print("ON EST VIDE", reponse)
        else:
            print("réponse", reponse)
            fichierTexteImporte=reponse[0]
            self.mandatActif=Mandat(fichierTexteImporte[1])
            self.mandatActif.idFichierTxt=fichierTexteImporte[0]
            self.parent.vue.fichierTexte.insert(END, fichierTexteImporte[1])
            
            requete="SELECT nom,type FROM AnalyseTextuelle WHERE nom is not NULL AND idProjet="+str(self.idProjet)
            reponse=self.parent.serveurBD.requeteSelect(requete, self.parent.BD, self.nomUser)
            if reponse!="Vide" and reponse!="Erreur":
                for unNom in reponse:
                    self.mandatActif.creerNom(unNom[0], unNom[1])
                    if unNom[1]==1:
                        self.parent.vue.listboxNomsExplicite.insert(END, unNom[0])
                    elif unNom[1]==2:
                        self.parent.vue.listboxNomsImplicite.insert(END, unNom[0])
                    elif unNom[1]==3:
                        self.parent.vue.listboxNomsSupplementaire.insert(END, unNom[0])
                        
                        
                        
            requete="SELECT verbe,type FROM AnalyseTextuelle WHERE verbe is not NULL AND idProjet="+str(self.idProjet)
            reponse=self.parent.serveurBD.requeteSelect(requete, self.parent.BD, self.nomUser)
            if reponse!="Vide" and reponse!="Erreur":
                for unVerbe in reponse:
                    self.mandatActif.creerVerbe(unVerbe[0], unVerbe[1])
                    if unVerbe[1]==1:
                        self.parent.vue.listboxVerbesExplicite.insert(END, unVerbe[0])
                    elif unVerbe[1]==2:
                        self.parent.vue.listboxVerbesImplicite.insert(END, unVerbe[0])
                    elif unVerbe[1]==3:
                        self.parent.vue.listboxVerbesSupplementaire.insert(END, unVerbe[0])
                        
                        
            
            requete="SELECT attribut,type FROM AnalyseTextuelle WHERE attribut is not NULL AND idProjet="+str(self.idProjet)
            reponse=self.parent.serveurBD.requeteSelect(requete, self.parent.BD, self.nomUser)
            if reponse!="Vide" and reponse!="Erreur":
                for unAttribut in reponse:
                    self.mandatActif.creerAttribut(unAttribut[0], unAttribut[1])
                    if unAttribut[1]==1:
                        self.parent.vue.listboxAdjectifsExplicite.insert(END, unAttribut[0])
                    elif unAttribut[1]==2:
                        self.parent.vue.listboxAdjectifsImplicite.insert(END, unAttribut[0])
                    elif unAttribut[1]==3:
                        self.parent.vue.listboxAdjectifsSupplementaire.insert(END, unAttribut[0])
                        
                        
        
                        
                        
    
    def creerMandat(self, fichierTxt):
        self.mandatActif=Mandat(fichierTxt)
        
    def supprimerMandat(self):
        requete="DELETE FROM AnalyseTextuelle WHERE idProjet="+str(self.idProjet)
        self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
        requete="DELETE FROM FichierTxt WHERE idProjet="+str(self.idProjet)
        self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
        self.mandatActif.idFichierTxt=None
        
    def enregistrerBD(self):        
        if self.mandatActif.idFichierTxt!=None:
            requete="UPDATE FichierTxt SET nom='"+ str(self.mandatActif.fichierTxt)+"'WHERE id="+str(self.mandatActif.idFichierTxt)
            self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
            
            requete="DELETE FROM AnalyseTextuelle WHERE idProjet="+str(self.idProjet)
            self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
            
            for unNom in self.mandatActif.noms:
                vartest=str(self.idProjet) + "," + str(unNom.type) + ",'" + str(unNom.nom)+"'"
                requete="INSERT INTO AnalyseTextuelle (idProjet,type,nom) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
                
            for unVerbe in self.mandatActif.verbes:
                vartest=str(self.idProjet) + "," + str(unVerbe.type) + ",'" + str(unVerbe.verbe)+"'"
                requete="INSERT INTO AnalyseTextuelle (idProjet,type,verbe) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
                
            for unAttribut in self.mandatActif.attributs:
                vartest=str(self.idProjet) + "," + str(unAttribut.type) + ",'" + str(unAttribut.attribut)+"'"
                requete="INSERT INTO AnalyseTextuelle (idProjet,type,attribut) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
            
        else:
            requete="INSERT INTO FichierTxt (nom,idProjet) VALUES ('" + str(self.mandatActif.fichierTxt) + "'," + str(self.idProjet) + ")"
            print(requete)
            self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
            
            for unNom in self.mandatActif.noms:
                vartest=str(self.idProjet) + "," + str(unNom.type) + ",'" + str(unNom.nom)+"'"
                requete="INSERT INTO AnalyseTextuelle (idProjet,type,nom) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
                
            for unVerbe in self.mandatActif.verbes:
                vartest=str(self.idProjet) + "," + str(unVerbe.type) + ",'" + str(unVerbe.verbe)+"'"
                requete="INSERT INTO AnalyseTextuelle (idProjet,type,verbe) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
                
            for unAttribut in self.mandatActif.attributs:
                vartest=str(self.idProjet) + "," + str(unAttribut.type) + ",'" + str(unAttribut.attribut)+"'"
                requete="INSERT INTO AnalyseTextuelle (idProjet,type,attribut) VALUES (" + vartest +")"
                print(requete)
                self.parent.serveurBD.modification(self.parent.BD, requete, self.nomUser)
        
        
class Mandat():
    def __init__(self, fichierTxt):
        self.idFichierTxt=None
        self.noms=[]
        self.verbes=[]
        self.attributs=[]
        self.fichierTxt=fichierTxt
        #self.fichierTxtBD=None
        #self.nomsBD=[]
        #self.verbesBD=[]
        #self.attributsBD=[]
        
        
    def creerNom(self, nom, type):
        nouveauNom=Nom(str(nom), type)
        self.noms.append(nouveauNom)
        pass
    
    def creerVerbe(self, verbe, type):
        nouveauVerbe=Verbe(str(verbe), type)
        self.verbes.append(nouveauVerbe)
    
    def creerAttribut(self, attribut, type):
        nouveauAttribut=Attribut(str(attribut), type)
        self.attributs.append(nouveauAttribut)
        
    def supprimerNom(self, mot, type):
        print("_________________________________________________")
        print(mot)
        print(type)
        
        for unNom in self.noms:
            print(unNom.nom, unNom.type)
            if unNom.nom == str(mot) and unNom.type == type:
                self.noms.remove(unNom)
                
        print("-------------------------------------------------")
        for unNom in self.noms:
            print(unNom.nom, unNom.type)
    
    def supprimerVerbe(self, mot, type):
        print("_________________________________________________")
        print(mot)
        print(type)
        
        for unVerbe in self.verbes:
            print(unVerbe.verbe, unVerbe.type)
            if unVerbe.verbe == str(mot) and unVerbe.type == type:
                self.verbes.remove(unVerbe)
        
        print("-------------------------------------------------")
        for unVerbe in self.verbes:
            print(unVerbe.verbe, unVerbe.type)
    
    def supprimerAdjectif(self, mot, type):
        
        print("_________________________________________________")
        print(mot)
        print(type)
        
        for unAttribut in self.attributs:
            print(unAttribut.attribut, unAttribut.type)
            if unAttribut.attribut == str(mot) and unAttribut.type == type:
                self.attributs.remove(unAttribut)
        
        
        print("-------------------------------------------------")
        for unAttribut in self.attributs:
            print(unAttribut.attribut, unAttribut.type)
 
class Nom():
    def __init__(self, nom, type):
        self.nom=nom
        self.type=type
        
class Verbe():
    def __init__(self, verbe, type):
        self.verbe=verbe
        self.type=type
        
class Attribut():
    def __init__(self, attribut, type):
        self.attribut=attribut
        self.type=type
        
        
if __name__ == '__main__':
    c=Controleur()