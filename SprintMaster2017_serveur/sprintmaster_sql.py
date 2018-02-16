# -*- coding: utf-8 -*-
from tkinter import *
import sqlite3

class LogicielAffaire(): #modele -> intelligence d'affaire
    def __init__(self):
        self.bd=sqlite3.connect("bdERP.sqlite")
        self.curs=self.bd.cursor()
    
    def ecrireLigne(self,nom="",courriel=""):
        sql="Insert into 'candidat' values('"+nom+"','"+courriel+"')"
        print(sql)
        self.curs.execute(sql)
        self.bd.commit()
        
    def liretables(self):
        pass
    
    def lireLignes(self,table):
        self.curs.execute("Select * from "+table)
        rep=self.curs.fetchall()
        return rep

    def trouvetable(self):
        sql="SELECT name FROM sqlite_master WHERE type='table';"
        self.curs.execute(sql)
        s=list(self.curs.fetchall())
        return s
        
    
class VueGraphique(): #vue -> interface entrée/sortie
    def __init__(self,parent):
        self.parent=parent
        self.cadreactif=None
        self.root=Tk()
        self.creercadremenu()
        self.creercadreinfo()
        self.activerCadre(self.cadremenu)
    
    def creercadremenu(self):
        self.cadremenu=Frame(self.root)
        self.btnlire=Button(self.cadremenu,text="Lire",command=self.lireEnregistrement)
        self.btnlire.pack()
        
    def creercadreinfo(self):
        self.cadreinfo=Frame(self.root)
        self.listeData=Listbox(self.cadreinfo,width=30,height=6)
        
        self.listeData.pack()
        
    def lireEnregistrement(self):
        rep=self.parent.lireEnregistrement()
        for i in rep:
            self.listeData.insert(END,i)
        self.activerCadre(self.cadreinfo)
    
    def activerCadre(self,cadre):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()

    def afficheMsg(self,texte):
        print(texte)
        
    def menu(self):
        pass
            
    def creertable(self):
        print("Création de table") 
        nomc=input("Table nom ")
        if nomc:
            tbdef=[]
            n=1
            while n:
                nomc=input("Champ nom (0 pour arrêter)")
                if nomc!= "0":
                    typi=input("Champ type (text,int,float) ")
                else:
                    n=0
                tbdef.append([nomc,typi])
            return [nomc,tbdef]
        
    def lireNewEnregistrement(self):
        print("Inscrire quelqu'un")
        nom=input("Son nom ")
        cour=input("Son courriel ")
        return [nom,cour]
    
    def gettablenames(self,lt):
        n=1
        for i in lt:
            print(n,i)
            n=n+1
            
        rep=input("Indiquez le no de la table choisie")
        rep2=lt[int(rep)-1]
        return rep2
    
    
class Controleur():
    def __init__(self):
        self.modele=LogicielAffaire()
        self.vue=VueGraphique(self)
        self.vue.root.mainloop()
    
    def ecrireEnregistrement(self):
        rep=self.vue.lireNewEnregistrement()
        self.modele.ecrireLigne(rep[0], rep[1])
        self.vue.menu()
        
    def lireEnregistrement(self):
        nomstables=self.modele.trouvetable()
        rep=self.vue.gettablenames(nomstables)[0]
        rep=self.modele.lireLignes(rep)
        return rep

    def creertable(self,deftb):
        rep=self.modele.creertable(deftb)
        return rep
        
if __name__ == '__main__':
    c=Controleur()
    c.vue.afficheMsg("Fini")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    