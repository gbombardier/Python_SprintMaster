# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
from tkinter import messagebox

class Vue():
    def __init__(self,parent,largeur=800,hauteur=1000):
        self.root=tix.Tk()
        #self.root.title(os.path.basename(sys.argv[0]))
        self.root.title("MetaSQL")
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=self.parent.modele
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.cadrelogin)

        
    def changemode(self,cadre):
        if self.modecourant:
            self.modecourant.pack_forget()
        self.modecourant=cadre
        self.modecourant.pack(expand=1,fill=BOTH)            

    def changecadre(self,cadre,etend=0):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        if etend:
            self.cadreactif.pack(expand=1,fill=BOTH)
        else:
            self.cadreactif.pack()
    
        
    def creercadres(self):
        self.creercadrelogin()
        self.creercadreBD()
        self.creercadreTable()
        self.creercadreInsertions()
    
                
    def creercadrelogin(self):
        self.cadrelogin=Frame(self.root)
        self.canevalogin=Canvas(self.cadrelogin,width=400,height=350,bg="limegreen")
        self.canevalogin.pack()
        label_nom=Label(text="Identifié en tant que : " + self.modele.nom,bg="darkgray")
        btn_connecter=Button(text="Débuter SQL",bg="lightgray",command=self.ouvreBD)
        self.canevalogin.create_window(200,200,window=label_nom,width=300,height=30)
        self.canevalogin.create_window(200,300,window=btn_connecter,width=100,height=30)
        
    def ouvreBD(self):
        self.changecadre(self.cadreBD)
        self.root.title("Base de données")
        
    def creercadreBD(self):
        self.cadreBD = Frame(self.root)
        label_nouvelleBD = Label(text="Ajouter une nouvelle BD", bg="lightgray", fg = "black")
        label_nomBD = Label(text = "Nom :",bg="lightgray", fg = "black")
        self.entry_nomBD = Entry(bg = "lightgray")
        btn_nouveau = Button(text = "Créer", bg = "lightgray", command=self.nouvelleBD)
        label_nom = Label(text="Liste des bases de données accessibles", bg="lightgray", fg = "black")
        btn_ouvrir = Button(text = "Ouvrir", bg = "lightgray", command=self.ouvrirBD)
        btn_supprimer = Button(text = "Supprimer", bg = "lightgray", command=self.supprimerBD)
        self.canevaBD = Canvas(self.cadreBD,width=400,height=350,bg="white")
        self.canevaBD.pack()
        self.listeBD = Listbox(self.cadreBD, bg = "white", borderwidth=1,relief=FLAT)
        
        scrollbar = Scrollbar(self.listeBD)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listeBD.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listeBD.yview)
        
        self.chargerBD()
        self.canevaBD.create_window(100, 25, window = label_nouvelleBD,width=200,height=30)
        self.canevaBD.create_window(50, 65, window = label_nomBD,width=100,height=30)
        self.canevaBD.create_window(175, 65, window = self.entry_nomBD, width=100,height=30)
        self.canevaBD.create_window(275, 65, window = btn_nouveau, width=75, height=30)
        self.canevaBD.create_window(100, 100, window = label_nom,width=200,height=30)
        self.lb_listeBD = self.canevaBD.create_window(100, 200, window = self.listeBD, width = 200, height = 150)
        self.canevaBD.create_window(275, 150, window = btn_ouvrir, width = 75, height = 30)
        self.canevaBD.create_window(275, 200, window = btn_supprimer, width = 75, height = 30)
        
    def creercadreTable(self):
        self.cadreTable = Frame(self.root)
        label_nouvelleTable = Label(text="Ajouter une nouvelle table", bg="lightgray", fg = "black")
        
        label_nomTable = Label(text = "Nom :",bg="lightgray", fg = "black")
        self.entry_nomTable = Entry(bg = "lightgray")
        label_champTable = Label(text = "Entrer la liste des champs : \n([nomduchamp TYPE [PRIMARY KEY AUTOINCREMENT][UNIQUE]][,...]) \nTYPE = INTEGER ou TEXT ", bg = "lightgray", fg = "black")
        self.entry_champTable = Entry(bg = "lightgray")
    
        btn_nouveau = Button(text = "Créer", bg = "lightgray", command=self.nouvelleTable)
        label_nom = Label(text="Liste des tables", bg="lightgray", fg = "black")
        btn_ouvrir = Button(text = "Ouvrir", bg = "lightgray", command=self.ouvrirTable)
        btn_supprimer = Button(text = "Supprimer", bg = "lightgray", command=self.supprimerTable)
        
        self.canevaTable = Canvas(self.cadreTable, width=600,height=600,bg="white")
        self.canevaTable.pack()
        self.listeTable = Listbox(self.cadreTable, bg = "white", borderwidth=1,relief=FLAT)
        
        scrollbar = Scrollbar(self.listeTable)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listeTable.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listeTable.yview)
        
        self.canevaTable.create_window(100, 25, window=label_nouvelleTable,width=200,height=30)
        self.canevaTable.create_window(50, 65, window=label_nomTable,width=100,height=30)
        self.canevaTable.create_window(200, 125, window=label_champTable,width=400,height=50)
        self.canevaTable.create_window(175, 65, window = self.entry_nomTable, width=100,height=30)
        self.canevaTable.create_window(175, 200, window = self.entry_champTable, width=300,height=30)
        self.canevaTable.create_window(275, 250, window=btn_nouveau, width=75, height=30)
        self.canevaTable.create_window(100, 350, window=label_nom,width=200,height=30)
        self.lb_listeTable = self.canevaTable.create_window(100, 450, window=self.listeTable, width = 200, height = 150)
        self.canevaTable.create_window(275, 400, window = btn_ouvrir, width = 75, height = 30)
        self.canevaTable.create_window(275, 500, window = btn_supprimer, width = 75, height = 30)
        
        
        
    def creercadreInsertions(self):
        self.cadreInsertions = Frame(self.root)
        label_nouvelleInsertions = Label(text="Ajouter une nouvelle Insertions", bg="lightgray", fg = "black")
        label_nomInsertions = Label(text = "Nom :",bg="lightgray", fg = "black")
        self.entry_nomInsertions = Entry(bg = "lightgray")
        btn_nouveau = Button(text = "Créer", bg = "lightgray", command=self.nouvelleInsertions)
        label_nom = Label(text="Liste des Insertions", bg="lightgray", fg = "black")
        #btn_ouvrir = Button(text = "Ouvrir", bg = "lightgray", command=self.ouvrirInsertions)
        self.canevaInsertions = Canvas(self.cadreInsertions, width=400,height=350,bg="white")
        self.canevaInsertions.pack()
        self.listeInsertions = Listbox(self.cadreInsertions, bg = "white", borderwidth=1,relief=FLAT)
        
        scrollbar = Scrollbar(self.listeInsertions)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listeInsertions.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listeInsertions.yview)
        
        self.canevaInsertions.create_window(100, 25, window=label_nouvelleInsertions,width=200,height=30)
        self.canevaInsertions.create_window(50, 65, window=label_nomInsertions,width=100,height=30)
        self.canevaInsertions.create_window(175, 65, window = self.entry_nomInsertions, width=100,height=30)
        self.canevaInsertions.create_window(275, 65, window=btn_nouveau, width=75, height=30)
        self.canevaInsertions.create_window(100, 100, window=label_nom,width=200,height=30)
        self.lb_listeInsertions = self.canevaInsertions.create_window(100, 200, window=self.listeInsertions, width = 200, height = 150)
        #self.canevaInsertions.create_window(300, 200, window = btn_ouvrir, width = 75, height = 30)
        
    def ouvrirBD(self):
        self.root.title("Tables")
        
        if self.modele.BDcourante == None:
            self.modele.BDcourante = self.listeBD.selection_get()
            
        liste = self.parent.ouvrirBD(self.modele.BDcourante)
        for i in liste:
            self.listeTable.insert(END,i)
            
        self.changecadre(self.cadreTable)
    
    def supprimerBD(self):
        self.parent.supprimerBD(self.listeBD.selection_get())
        self.modele.BDcourante=None
        self.refresh()
       
    def chargerBD(self):
        liste = self.parent.chargerBD()
        for i in liste:
            self.listeBD.insert(END,i)
            
    def nouvelleBD(self):
        nomBD = self.entry_nomBD.get()
        self.parent.nouvelleBD(nomBD)
        self.refresh()
    
    def nouvelleTable(self):
        nomTable = self.entry_nomTable.get()
        listeTable = self.listeTable.get(0,END)
        champTable = self.entry_champTable.get()
        for table in listeTable:
            if table == nomTable:
                messagebox.showwarning("Alerte", "La table existe déjà.")
                return 0
            
        rep = self.parent.nouvelleTable(nomTable,champTable)
        self.refreshTable()
        
        
    def supprimerTable(self):
        if self.modele.tablecourante == None:
            self.modele.tablecourante = self.listeTable.selection_get()
            
        self.parent.supprimerTable()
        self.modele.tablecourante = None
        self.refreshTable()
    
    def ouvrirTable(self):
        choix = self.listeTable.selection_get()
        listeInsertions = self.parent.listeInsertions(choix)
        if listeInsertions:
            for i in listeInsertions:
                self.listeInsertions.insert(END,i)
        else:
            self.listeInsertions.insert(END,"poopi")
        self.root.title("Insertions")
        self.changecadre(self.cadreInsertions)
    
    def nouvelleInsertions(self):
        pass

    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    
    def refresh(self):
        self.canevaBD.delete(self.lb_listeBD)
        self.listeBD = Listbox(self.cadreBD, bg = "white", borderwidth=1,relief=FLAT)
        self.chargerBD()
        self.canevaBD.create_window(100, 250, window=self.listeBD, width = 200, height = 150)
        
    def refreshTable(self):
        self.canevaTable.delete(self.lb_listeTable)
        self.listeTable = Listbox(self.cadreTable, bg = "white", borderwidth=1,relief=FLAT)
        self.ouvrirBD()
        self.canevaTable.create_window(100, 450, window=self.listeTable, width = 200, height = 150)