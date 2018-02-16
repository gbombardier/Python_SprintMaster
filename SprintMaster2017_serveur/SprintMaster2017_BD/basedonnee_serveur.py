# -*- encoding: utf-8 -*-

# import Pyro4
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os, os.path
from threading import Timer
import sys
import socket
import time
import random
import sqlite3
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com", 80))
monip = s.getsockname()[0]
print("MON IP SERVEUR", monip, "port : 9998")
s.close()

# daemon = Pyro4.core.Daemon(host=monip,port=9999) 
daemon = SimpleXMLRPCServer((monip, 9998),allow_none=True)

class Client(object):
    def __init__(self, nom, org):
        self.nom = nom
        self.org = org
        self.cadreCourant = 0
        self.cadreEnAttenteMax = 0
        self.actionsEnAttentes = {}
        
class ModeleService(object):
    def __init__(self, parent, rdseed):
        self.parent = parent
        self.rdseed = rdseed
        self.cadreCourant = 0
        self.cadreFutur = 2
        self.clients = {}
        self.cadreDelta = {}
        self.mylogfile = 'basedonnee.log'
        
    def creerclient(self, nom, org):
        if nom in self.clients.keys():  # on assure un nom unique
            return [0, "Connexion déjà établie"]
        # tout va bien on cree le client et lui retourne la seed pour le random
        c = Client(nom, org)
        self.cadreDelta[nom] = 0
        self.clients[nom] = c
        return [1, "Connexion au serveur BD"]
    

class OutilsSQL:
    def __init__(self,parent):
        self.parent = parent
        self.mylogfile = parent.modele.mylogfile
        
    def lireBD(self, nom):
        org = self.parent.modele.clients[nom].org
        cwd = os.getcwd()
        if os.path.exists(cwd):
            dirmod = cwd + '/' + org
            if os.path.exists(dirmod) == False:
                os.mkdir(dirmod, mode=0o777)
                return 0
            if os.path.exists(dirmod):
                listefichiers = []
                for i in os.listdir(dirmod):
                    if os.path.isfile(dirmod + '/' + i):
                        body, ext= os.path.splitext(i)
                        val = ["fichier", body]
                    else:
                        val = ["dossier", i]
                              
                    listefichiers.append(val)
                return [dirmod, listefichiers]
    
    def nouvelleBd(self, nom, nomBD):
        org = self.parent.modele.clients[nom].org
        cwd = os.getcwd()
        if os.path.exists(cwd):
            dirmod = cwd + '/' + org
            if os.path.exists(dirmod) == False:
                os.mkdir(dirmod, mode=0o777)
        if os.path.exists(dirmod + '/' + nomBD+ '.smid'):
            return "BD existe déjà"
        conn = sqlite3.connect(dirmod + '/' + nomBD+ '.smid')
        c = conn.cursor()
        
        with open("table.txt", "r") as script:
            ligne = script.readlines()
        for l in ligne:
            c.execute(l)
        conn.commit()
        
        if (os.path.isfile(dirmod+'/'+nomBD+'.smid')):
            self.entreeLog(self.parent.modele.clients[nom].org, nom, nomBD, "Créé")
        else:
            self.entreeLog(self.parent.modele.clients[nom].org, nom, nomBD, "Création échouée.")
        conn.close()
        
    
    def nouvelleTable(self,nom,nomBD,nomTable,champTable):
        path = self.trouverPath(nom)
        monpath = path + '/' + nomBD + '.smid'
        conn = sqlite3.connect(monpath)
        c = conn.cursor()

        try:
            c.execute('''CREATE TABLE ''' + nomTable + ''' ''' + champTable)
            rep = "Fonctionné"
            self.entreeLog(self.parent.modele.clients[nom].org, nom, nomBD, "Table " + nomTable + " crée")
        except:
            rep = "Erreur"
            self.entreeLog(self.parent.modele.clients[nom].org, nom, nomBD, "Table " + nomTable + " création échouée.")
        conn.commit()
        conn.close()
        return rep
        
    def listeTable(self, nom, bd, nomBD):
        conn = sqlite3.connect(nomBD)
        
        c = conn.cursor()
        c.execute('''SELECT name FROM sqlite_master WHERE type = 'table' ''')
        listeTable = []
        for table in c.fetchall():
            listeTable.append(table[0])
        conn.close()
        
        #ajout au log
        f = open(self.mylogfile, 'a')
        auj = datetime.datetime.now()
        f.write("[" + str(auj.isoformat()) + "] " + self.parent.modele.clients[nom].org + " : " + nom + " : " + nomBD + " : ouverte " + '\n')
        f.close()
        
        return listeTable
    
    def listeInsertions(self,nom,bd,nomBD,table):
        conn = sqlite3.connect(nomBD)
        c = conn.cursor()
        c.execute(''' SELECT * FROM ''' + table)
        listeInsertions = []
        for ins in c.fetchall():
            listeInsertions.append(ins[0])
        conn.close()
        
        f = open(self.mylogfile, 'a')
        auj = datetime.datetime.now()
        f.write("[" + str(auj.isoformat()) + "] " + self.parent.modele.clients[nom].org + " : " + nom + " : " + nomBD + " : " + table + " : ouverte " + '\n')
        f.close()
        return listeInsertions
    
    def supprimerBD(self,nom,nomBD):
        org = self.parent.modele.clients[nom].org
        cwd = os.getcwd()
        dirmod = cwd + '/' + org
        bdpath = dirmod + '/' + nomBD + '.smid'
        if (os.path.exists(bdpath)):
            os.remove(bdpath)
            return "Base de donnée n'existe pas"
        else:
            return "Erreur"
        return 0
    def supprimerTable(self,nom,nomBD,nomTable):
        org = self.parent.modele.clients[nom].org
        cwd = os.getcwd()
        dirmod = cwd + '/' + org
        bdpath = dirmod + '/' + nomBD + '.smid'
        conn = sqlite3.connect(bdpath)
        c = conn.cursor()
        c.execute('''DROP TABLE ''' + nomTable)
        conn.commit()
        conn.close()
        return 0
    
    def trouverPath(self,nom):
        org = self.parent.modele.clients[nom].org
        cwd = os.getcwd()
        if os.path.exists(cwd):
            dirmod = cwd + '/' + org
            return dirmod
    
    def requeteSelect(self,requete,BD,nom):
        path=self.trouverPath(nom)
        conn = sqlite3.connect(path+"/"+BD)
        c=conn.cursor()
        try:
            c.execute(requete)
            self.entreeLog(self.parent.modele.clients[nom].org, nom, BD, requete + " Effectuée")
            rep = c.fetchall()
            if rep == []:
                rep = "Vide"
        except:
            rep = "Erreur"
            self.entreeLog(self.parent.modele.clients[nom].org, nom, BD, requete + " Échouée.")
        conn.close()
        return rep
    
    def modification(self,BD,req,nom):
        path=self.trouverPath(nom)
        conn=sqlite3.connect(path+"/"+BD)
        c=conn.cursor()
        c.execute(req)
        conn.commit()
        self.entreeLog(self.parent.modele.clients[nom].org, nom, BD, req + " Effectuée")
        conn.close()
        return 0 
        
    def requeteInsertion(self,req,BD, nom):
        path=self.trouverPath(nom)
        conn = sqlite3.connect(path+"/"+BD)
        c=conn.cursor()
        try:
            c.execute(req)
            conn.commit()
            rep = c.lastrowid
            self.entreeLog(self.parent.modele.clients[nom].org, nom, BD, req + " Effectuée")
        except:
            rep = "Erreur"
            self.entreeLog(self.parent.modele.clients[nom].org, nom, BD, req + " Échouée")
            
        conn.close()
        return rep
    
    def supprimer(self,BD,nom, requete):
        path=self.trouverPath(nom)
        conn=sqlite3.connect(path+"/"+BD)
        c=conn.cursor()
        c.execute(requete)
        conn.commit()
        self.entreeLog(self.parent.modele.clients[nom].org, nom, BD, requete + " Effectuée")
        conn.close()
        return 0
    
    def entreeLog(self, organisation, nom, nomBD, message):
        f = open(self.mylogfile, 'a')
        auj = datetime.datetime.now()
        f.write("[" + str(auj.isoformat()) + "] " + organisation + " : " + nom + " : " + nomBD + " : " + message+ '\n')
        f.close()
        return 1
        
class ControleurServeur(object):
    def __init__(self):
        rand = random.randrange(1000) + 1000
        # self.checkping=0
        self.delaitimeout = 25  # delai de 5 secondes
        self.modele = ModeleService(self, rand)
        self.outils = OutilsSQL(self)
        
        
    def lireBD(self, nom):
        listeBD = self.outils.lireBD(nom)
        return listeBD
        
    def ajout(self,BD,req,nom):
        return self.outils.requeteInsertion(req,BD,nom)
    
    def nouvelleBD(self, nom, nomBD):
        rep = self.outils.nouvelleBd(nom, nomBD)
        return rep
    
    def nouvelleTable(self, nom,nomBD,nomTable,champTable):
        rep = self.outils.nouvelleTable(nom, nomBD, nomTable, champTable)
        return rep
    
    def requeteSelect(self,req,BD,nom):
        rep=self.outils.requeteSelect(req,BD,nom)
        return rep
    
    def nouveauCRC(self,req,BD,nom):
        rep = self.outils.requeteInsertion(req,BD,nom)
        return rep
    
    def listeTable(self,nom,bd,nomBD):
        listeTable = self.outils.listeTable(nom,bd,nomBD)
        return listeTable
    
    def listeInsertions(self, nom, bd, bdpath, table):
        listeInsertions = self.outils.listeInsertions(nom, bd, bdpath, table)
        return listeInsertions
    
    def loginauserveur(self, nom, org):
        rep = self.modele.creerclient(nom, org)
        return rep
    
    def ajoutMaquette(self,BD,nom,requete):
        return self.outils.requeteInsertion(requete, BD, nom)
    
    def ajoutForme(self,BD,nom,requete):
        return self.outils.requeteInsertion(requete, BD, nom)
    
    def requeteIdEtTitreMaquette(self, BD, nom, requete):
        return self.outils.requeteSelect(requete, BD, nom)
    
    def requeteFormesMaquette(self, BD, nom, requete):
        return self.outils.requeteSelect(requete, BD, nom)
    
    def supprimerFormes(self,BD,nom, requete):
        return self.outils.supprimer(BD, nom, requete)
    
    def supprimerMaquette(self,BD,nom, requete):
        return self.outils.supprimer(BD, nom, requete)
    
    def verifiecontinuation(self):
        t = int(time.time())
        if (t - self.checkping) > self.delaitimeout: 
            return "testserveur"
            self.fermer()
        else:
            tim = Timer(1, self.verifiecontinuation)
            tim.start()
        
    def modificationCasUsage(self, nomUser, nomBD, chaine):
        self.outils.modification(nomBD,chaine,nomUser)
    
    def modification(self,BD,req,nomUser):
        self.outils.modification(BD,req,nomUser)
        
    def selectCasUsage(self,nomUser,nomBD,chaine):
        return self.outils.requeteSelect(chaine, nomBD, nomUser)
    
    def quitter(self):
        t = Timer(1, self.fermer)
        t.start()
        return "ferme"
    
    def jequitte(self, nom):
        del self.modele.clients[nom]
        del self.modele.cadreDelta[nom]
        if not self.modele.clients:
            self.quitter()
        return 1
    
    def supprimerBD(self,nom, nomBD):
        rep = self.outils.supprimerBD(nom, nomBD)
        return rep
    def supprimerTable(self,nom,nomBD,nomTable):
        rep = self.outils.supprimerTable(nom,nomBD,nomTable)
        return rep
    def fermer(self):
        daemon.shutdown()

controleurServeur = ControleurServeur()
# daemon.register(controleurServeur, "controleurServeur")  
daemon.register_instance(controleurServeur)
print("Serveur XMLRPC actif sous le nom \'Serveur base de données\'")
# daemon.requestLoop()
daemon.serve_forever()
