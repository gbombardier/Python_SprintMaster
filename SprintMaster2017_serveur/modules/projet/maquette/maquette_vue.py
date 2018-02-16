# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
from ctypes.test.test_incomplete import MyTestCase

class Vue():
    def __init__(self,parent,largeur=800,hauteur=1000):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.cadreCreation)
        self.figure="";
        self.tagMaker=0
        
        
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
        self.cadreCreation=Frame(self.root)
        self.cadreListBox=Frame(self.cadreCreation)
        self.cadreOutils=Frame(self.root)
        self.cadreDessin=Frame(self.root)
       
        self.canevasSurfaceDessin=Canvas(self.cadreDessin,width=800,height=700,bg="white")
        self.canevasSurfaceDessin.pack()
        
        self.lblImporterMaquette=Label(self.cadreCreation, text="Choisir une maquette : ")
        
        self.scrollbar = Scrollbar(self.cadreListBox)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.cadreListBox, yscrollcommand=self.scrollbar.set, height=3)
        self.listbox.pack(side=LEFT, fill=BOTH)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.btnOuvrirMaquette=Button(self.cadreCreation, text="Ouvrir une maquette", command=self.ouvrirMaquette)
        
        
        self.lblTitreMaquette=Label(self.cadreCreation, text="Titre : ")
        self.entryTitre=Entry(self.cadreCreation, bg="white")
        self.btnCreerMaquette=Button(self.cadreCreation, text="Créer nouvelle maquette", command=self.creerNouvelleMaquette)
        self.btnSupprimerMaquette=Button(self.cadreCreation, text="Supprimer la maquette", command=self.supprimerMaquette)
        self.btnEnregistrerBD=Button(self.cadreCreation, text="Enregistrer", command=self.enregistrerBD)
        
        self.lblImporterMaquette.grid(row=0, column=0)
        self.cadreListBox.grid(row=1, column=0 , rowspan=2)
        self.btnOuvrirMaquette.grid(row=3, column=0) 
        
        self.lblTitreMaquette.grid(row=0, column=1)
        self.entryTitre.grid(row=0, column=2)
        self.btnCreerMaquette.grid(row=1, column=2 ,columnspan=2)
        self.btnSupprimerMaquette.grid(row=2, column=1, columnspan=2)
        self.btnEnregistrerBD.grid(row=3, column=1 ,columnspan=2)
        
        
        #btns formes
        self.controleFormes = StringVar()
        self.btnLigne=Radiobutton(self.cadreOutils,text="Ligne", variable=self.controleFormes, value='ligne',indicatoron=0, command=self.creerLigne)
        self.btnRectangle=Radiobutton(self.cadreOutils, text="Rectangle", variable=self.controleFormes, value='rectangle',indicatoron=0, command=self.creerRectangle)
        self.btnCercle=Radiobutton(self.cadreOutils, text="Cercle", variable=self.controleFormes, value='cercle',indicatoron=0, command=self.creerCercle)
        self.btnSupprimerForme=Radiobutton(self.cadreOutils, text="Supprimer forme", variable=self.controleFormes, value='supprimer',indicatoron=0, command=self.supprimerForme)
        self.btnTexte=Radiobutton(self.cadreOutils, text="Texte", variable=self.controleFormes, value='texte',indicatoron=0, command=self.creerTexte)
        self.entryTexte=Entry(self.cadreOutils, bg="white")
        
        self.btnLigne.pack(side=LEFT)
        self.btnRectangle.pack(side=LEFT)
        self.btnCercle.pack(side=LEFT)
        self.btnSupprimerForme.pack(side=LEFT)
        self.btnTexte.pack(side=LEFT)
        self.entryTexte.pack(side=LEFT)
        
        self.canevasSurfaceDessin.bind("<Button-1>",self.clic1)
        self.canevasSurfaceDessin.bind("<B1-Motion>",self.tenirClic1)
        self.canevasSurfaceDessin.bind("<ButtonRelease-1>",self.releaseClic1)
        
        self.cadreCreation.pack()
        self.cadreOutils.pack()
        
            
    
    def enregistrerBD(self):
        if self.parent.modele.maquetteActive != None:
            self.parent.enregistrerBD()
            self.listbox.delete(0, END)
            self.parent.modele.chargerIdEtTitre()
        
    def creerNouvelleMaquette(self):
        print("in creerMaquette")
        titreUnique = True
        print( self.parent.modele.IdEtTitre)
        
        if self.parent.modele.IdEtTitre != "Vide":
            for i in self.parent.modele.IdEtTitre:
                if self.entryTitre.get()==str(i[1]):
                    titreUnique = False
        
        if self.entryTitre.get()=="" or titreUnique == False:
            print("Veuillez entrer un titre différent")
            if titreUnique==False:
                print("titre non unique")
                
        else:
            self.parent.creerNouvelleMaquette(self.entryTitre.get())
            self.canevasSurfaceDessin.delete("all")
            print("maquette créée")
            
            

    def ouvrirMaquette(self):
        if self.listbox.curselection():
            self.parent.ouvrirMaquetteExistante(self.listbox.get(self.listbox.curselection()))
        
        
    
    def supprimerMaquette(self):
        if self.listbox.curselection():
            self.parent.supprimerMaquette(self.listbox.get(self.listbox.curselection()))
            n=self.listbox.curselection()
            self.listbox.delete(n[0])
        
        
    def clic1(self, event):
        self.x0 = event.x
        self.y0 = event.y
        t=self.canevasSurfaceDessin.gettags(CURRENT)
        print (t)
        
    
    def tenirClic1(self, event):
        pass
    
    def releaseClic1(self, event):
        print(self.x0, self.y0)
        self.x1 = event.x
        self.y1 = event.y
        if self.figure=="ligne":
            self.canevasSurfaceDessin.create_line(self.x0, self.y0, self.x1, self.y1, tags= (self.figure, str(self.tagMaker)))
            self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, self.x0, self.y0, self.x1, self.y1, str(self.tagMaker), "")
            self.tagMaker+=1
        if self.figure=="cercle":
            self.canevasSurfaceDessin.create_oval(self.x0, self.y0, self.x1, self.y1, tags= (self.figure, str(self.tagMaker)))
            self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, self.x0, self.y0, self.x1, self.y1, str(self.tagMaker), "")
            self.tagMaker+=1
        if self.figure=="rectangle":
            self.canevasSurfaceDessin.create_rectangle(self.x0, self.y0, self.x1, self.y1, tags= (self.figure, str(self.tagMaker)))
            self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, self.x0, self.y0, self.x1, self.y1, str(self.tagMaker), "")
            self.tagMaker+=1
        if self.figure=="texte" and self.entryTexte.get()!="":
            self.canevasSurfaceDessin.create_text(self.x1, self.y1, anchor=NW, text=self.entryTexte.get(), tags= (self.figure, str(self.tagMaker)))
            self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, 0, 0, self.x1, self.y1, str(self.tagMaker), self.entryTexte.get())
            self.tagMaker+=1
            
        
        if self.figure=="supprimer":
            tagsCourants=self.canevasSurfaceDessin.gettags(CURRENT)
            for uneForme in self.parent.modele.maquetteActive.formes:
                if uneForme.tagUnique in tagsCourants:
                    self.canevasSurfaceDessin.delete('current')
                    self.parent.modele.maquetteActive.formes.remove(uneForme)
        
        
        
    
    def redessinerFormesImportees(self):
        self.canevasSurfaceDessin.delete("all")
        self.tagMaker=0
        for uneForme in self.parent.modele.formesImportees:
            if uneForme[0]==0:
                self.creerLigne()
            elif uneForme[0]==1:
                self.creerRectangle()
            elif uneForme[0]==2:
                self.creerCercle()
            else:
                self.creerTexte()
            
            if self.figure=="ligne":
                self.canevasSurfaceDessin.create_line(uneForme[1], uneForme[2], uneForme[3], uneForme[4], tags= (self.figure, str(self.tagMaker)))
                self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, uneForme[1], uneForme[2], uneForme[3], uneForme[4], str(self.tagMaker), "")
                self.tagMaker+=1
            if self.figure=="cercle":
                self.canevasSurfaceDessin.create_oval(uneForme[1], uneForme[2], uneForme[3], uneForme[4], tags= (self.figure, str(self.tagMaker)))
                self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, uneForme[1], uneForme[2], uneForme[3], uneForme[4], str(self.tagMaker), "")
                self.tagMaker+=1
            if self.figure=="rectangle":
                self.canevasSurfaceDessin.create_rectangle(uneForme[1], uneForme[2], uneForme[3], uneForme[4], tags= (self.figure, str(self.tagMaker)))
                self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, uneForme[1], uneForme[2], uneForme[3], uneForme[4], str(self.tagMaker), "")
                self.tagMaker+=1
            if self.figure=="texte":
                self.canevasSurfaceDessin.create_text(uneForme[3], uneForme[4], anchor=NW, text=uneForme[5], tags= (self.figure, str(self.tagMaker)))
                self.parent.modele.maquetteActive.creerForme(self.idFigure, self.figure, 0, 0, uneForme[3], uneForme[4], str(self.tagMaker), uneForme[5])
                self.tagMaker+=1
        
        
    def creerLigne(self):
        self.figure="ligne"
        self.idFigure=0
    
    def creerRectangle(self):
        self.figure="rectangle"
        self.idFigure=1
    
    def creerCercle(self):
        self.figure="cercle"
        self.idFigure=2
        
    def creerTexte(self):
        self.figure="texte"
        self.idFigure=3
    
    
    def supprimerForme(self):
        self.figure="supprimer"
    
    def salutations(self):
        print("HOURRA SA MARCHE")
    
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    