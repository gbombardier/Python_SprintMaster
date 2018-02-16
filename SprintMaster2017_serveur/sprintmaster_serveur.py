# -*- encoding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os,os.path
from threading import Timer
import sys
import socket
import time
import random
import sqlite3

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
monip=s.getsockname()[0]
print("MON IP SERVEUR",monip)
s.close()

daemon = SimpleXMLRPCServer((monip,9999), allow_none=True)

class Client(object):
    def __init__(self,nom, org):
        self.nom=nom
        self.org=org
        self.cadreCourant=0
        self.cadreEnAttenteMax=0
        self.actionsEnAttentes={}
        
class ModeleService(object):
    def __init__(self,parent,rdseed):
        self.parent=parent
        self.modulesdisponibles={"projet":"projet"}
        self.outilsdisponibles={"meta_sql":"meta_sql"}
        self.modulesProjets={"cas_usage":"cas_usage",
                             "crc":"crc",
                             "maquette":"maquette",
                             "mandat":"mandat",
                             "planif":"planif",
                             "sprint":"sprint"}
        self.etatJeu=0
        self.rdseed=rdseed
        self.cadreCourant=0
        self.cadreFutur=2
        self.clients={}
        self.cadreDelta={}
        self.conn=None
        self.curseur=None
        
    def creerclient(self,nom, org):
        if self.etatJeu==0:  # si le jeu n'est pas partie sinon voir else
            if nom in self.clients.keys(): # on assure un nom unique
                return [0,"Erreur de nom"]
            # tout va bien on cree le client et lui retourne la seed pour le random
            c=Client(nom, org)
            self.cadreDelta[nom]=0
            self.clients[nom]=c
            return [1,"Connexion au serveur de modules",list(self.modulesdisponibles.keys()),list(self.outilsdisponibles.keys())]
        else:
            return [0,"Simulation deja en cours"]
        
    def nouvelleBd(self,nomBD):
        conn = sqlite3.connect(nomBD)
        if (os.path.isfile(nomBD)):
            return 1
        else:
            return 0
        
    def lireBD(self,nom):
        org = self.clients[nom].org
        cwd=os.getcwd()
        if os.path.exists(cwd):
            dirmod=cwd+'/'+org
            if os.path.exists(dirmod) == False:
                os.mkdir(dirmod, mode=0o777)
            if os.path.exists(dirmod):
                listefichiers=[]
                for i in os.listdir(dirmod):
                    if os.path.isfile(dirmod+'/'+i):
                        val=["fichier",i]
                    else:
                        val=["dossier",i]
                              
                    listefichiers.append(val)
                return [dirmod,listefichiers]
    
    def requeteSQL(self, requete, nomBD):
        conn = sqlite3.connect(nomBD)
        curseur=conn.cursor()
        curseur.execute(requete)
        conn.commit()
        conn.close()
        return 0
    
    def retournerListe(self, requete, nomBD):
        conn = sqlite3.connect(nomBD)
        curseur=conn.cursor()
        curseur.execute(requete)
        rep = curseur.fetchall()
        conn.commit()
        conn.close()
        return rep
    
    def obtenirModules(self):
        return [1,"Connexion au serveur de modules",list(self.modulesProjets.keys())]
 
class ControleurServeur(object):
    def __init__(self):
        rand=random.randrange(1000)+1000
        #self.checkping=0
        self.delaitimeout=25   # delai de 5 secondes
        self.modele=ModeleService(self,rand)
        
    def testPyro(self):
        return 42
    
    def lireBD(self,nom):
        listeBD = self.modele.lireBD(nom)
        return listeBD
    
    def nouvelleBD(self,nomBD):
        rep = self.modele.nouvelleBd(nomBD)
        return rep
    
    def retournerListe(self,requete,nomBD):
        rep = self.modele.retournerListe(requete, nomBD)
        return rep
        
    def loginauserveur(self,nom, org):
        rep=self.modele.creerclient(nom, org)
        return rep
    
    def requeteSQL(self, requete, nomBD):
        rep = self.modele.requeteSQL(requete, nomBD)
        return rep
    
    def obtenirModules(self):
        return self.modele.obtenirModules()
    
    def requeteoutils(self,mod):
        if mod in self.modele.outilsdisponibles.keys():
            cwd=os.getcwd()
            if os.path.exists(cwd+"/outils/"):
                dirmod=cwd+"/outils/"+self.modele.outilsdisponibles[mod]+"/"
                if os.path.exists(dirmod):
                    listefichiers=[]
                    for i in os.listdir(dirmod):
                        if os.path.isfile(dirmod+i):
                            val=["fichier",i]
                        else:
                            val=["dossier",i]
                            
                        listefichiers.append(val)
                    return [mod,dirmod,listefichiers]
                
    def requetemodule(self,mod):
        if mod in self.modele.modulesdisponibles.keys():
            cwd=os.getcwd()
            if os.path.exists(cwd+"/modules/"):
                dirmod=cwd+"/modules/"+self.modele.modulesdisponibles[mod]+"/"
                if os.path.exists(dirmod):
                    listefichiers=[]
                    for i in os.listdir(dirmod):
                        if os.path.isfile(dirmod+i):
                            val=["fichier",i]
                        else:
                            val=["dossier",i]
                            
                        listefichiers.append(val)
                    return [mod,dirmod,listefichiers]
            
    def requeteProjet(self,mod):
        if mod in self.modele.modulesProjets.keys():
            cwd=os.getcwd()+"/modules/projet"
            if os.path.exists(cwd):
                dirmod=cwd+"/"+self.modele.modulesProjets[mod]+"/"
                if os.path.exists(dirmod):
                    listefichiers=[]
                    for i in os.listdir(dirmod):
                        if os.path.isfile(dirmod+i):
                            val=["fichier",i]
                        else:
                            val=["dossier",i]
                            
                        listefichiers.append(val)
                    return [mod,dirmod,listefichiers]
                
    def requetefichier(self,lieu):
        fiche=open(lieu,"rb")
        contenu=fiche.read()
        fiche.close()
        return xmlrpc.client.Binary(contenu)
            
    
    def verifiecontinuation(self):
        t=int(time.time())
        if (t-self.checkping) > self.delaitimeout: 
            self.fermer()
        else:
            tim=Timer(1,self.verifiecontinuation)
            tim.start()
        
    def quitter(self):
        t=Timer(1,self.fermer)
        t.start()
        return "ferme"
    
    def jequitte(self,nom):
        del self.modele.clients[nom]
        del self.modele.cadreDelta[nom]
        if not self.modele.clients:
            self.quitter()
        return 1
    
    def fermer(self):
        daemon.shutdown()

controleurServeur=ControleurServeur()
daemon.register_instance(controleurServeur)
print("Serveur XMLRPC actif sous le nom \'controleurServeur\'")
daemon.serve_forever()