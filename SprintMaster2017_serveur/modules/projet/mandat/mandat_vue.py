# -*- coding: utf-8 -*-
from tkinter import *
#from tkinter import tix
#from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
from ctypes.test.test_incomplete import MyTestCase
from tkinter import filedialog

class Vue():
    def __init__(self,parent):
        self.root=Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.cadreFichier)
        
        
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
        self.cadreFichier=Frame(self.root)
        
        
        #self.btnOuvrirFichier=Button(self.cadreFichier, text="Ouvrir un fichier texte", command=self.ouvrirFichier)
        self.entryMotAAjouter=Entry(self.cadreFichier, bg="white", width=100)
        
        self.cadreCreationMandat=Frame(self.root)
        
        #self.lblTitreMandat=Label(self.cadreCreationMandat, text="Titre du mandat : ")
        #self.entryTitre=Entry(self.cadreCreationMandat, bg="white")
        #self.btnCreer=Button(self.cadreCreationMandat, text="Creer un mandat", command=self.creerMandat)
        self.btnEnregistrer=Button(self.cadreCreationMandat, text="Enregistrer", command=self.enregistrerSurBD)
        self.btnSupprimerMandat=Button(self.cadreCreationMandat, text="Supprimer un mandat", command=self.supprimerUnMandat)
        
        
      
        #self.lblTitreMandat.pack(side=LEFT)
        #self.entryTitre.pack(side=LEFT)
        #self.btnCreer.pack(side=LEFT)
        self.btnEnregistrer.pack(side=LEFT)
        self.btnSupprimerMandat.pack(side=LEFT)
        
        
        
        #######################################################Explicicte##############################################################################
        self.cadreAnalyseExplicite=Frame(self.root)
        
        self.lblExplicite=Label(self.cadreAnalyseExplicite, text="Explicite :            ")
        self.btnNomsExplicite=Button(self.cadreAnalyseExplicite, text="Noms (objets)", command=self.ajouterNomExplicite)
        self.btnVerbesExplicite=Button(self.cadreAnalyseExplicite, text="Verbes (actions)", command=self.ajouterVerbeExplicite)
        self.btnAdjectifsExplicite=Button(self.cadreAnalyseExplicite, text="Adjectifs (attributs)", command=self.ajouterAdjectifExplicite)
        
        self.cadreListBoxNomsExplicite=Frame(self.cadreAnalyseExplicite)
        self.scrollbarNomsExplicite = Scrollbar(self.cadreListBoxNomsExplicite)
        self.scrollbarNomsExplicite.pack(side=RIGHT, fill=Y)
        self.listboxNomsExplicite = Listbox(self.cadreListBoxNomsExplicite, yscrollcommand=self.scrollbarNomsExplicite.set, height=6)
        self.listboxNomsExplicite.pack(side=LEFT, fill=BOTH)
        self.scrollbarNomsExplicite.config(command=self.listboxNomsExplicite.yview)
        
        
        self.cadreListBoxVerbesExplicite=Frame(self.cadreAnalyseExplicite)
        self.scrollbarVerbesExplicite = Scrollbar(self.cadreListBoxVerbesExplicite)
        self.scrollbarVerbesExplicite.pack(side=RIGHT, fill=Y)
        self.listboxVerbesExplicite = Listbox(self.cadreListBoxVerbesExplicite, yscrollcommand=self.scrollbarVerbesExplicite.set, height=6)
        self.listboxVerbesExplicite.pack(side=LEFT, fill=BOTH)
        self.scrollbarVerbesExplicite.config(command=self.listboxVerbesExplicite.yview)
        
        
        self.cadreListBoxAdjectifsExplicite=Frame(self.cadreAnalyseExplicite)
        self.scrollbarAdjectifsExplicite = Scrollbar(self.cadreListBoxAdjectifsExplicite)
        self.scrollbarAdjectifsExplicite.pack(side=RIGHT, fill=Y)
        self.listboxAdjectifsExplicite = Listbox(self.cadreListBoxAdjectifsExplicite, yscrollcommand=self.scrollbarAdjectifsExplicite.set, height=6)
        self.listboxAdjectifsExplicite.pack(side=LEFT, fill=BOTH)
        self.scrollbarAdjectifsExplicite.config(command=self.listboxVerbesExplicite.yview)
        
        
        self.btnSupprimerNomEx=Button(self.cadreAnalyseExplicite, text="Supprimer nom", command=self.supprimerNomEx)
        self.btnSupprimerVerbeEx=Button(self.cadreAnalyseExplicite, text="Supprimer verbe", command=self.supprimerVerbeEx)
        self.btnSupprimerAdjectifEx=Button(self.cadreAnalyseExplicite, text="Supprimer adjectif", command=self.supprimerAdjectifEx)
        
        
        self.lblExplicite.grid(row=0, column=0)
        self.btnNomsExplicite.grid(row=0, column=1)
        self.btnSupprimerNomEx.grid(row=0, column=2)
        self.btnVerbesExplicite.grid(row=0, column=3)
        self.btnSupprimerVerbeEx.grid(row=0, column=4)
        self.btnAdjectifsExplicite.grid(row=0, column=5)
        self.btnSupprimerAdjectifEx.grid(row=0, column=6)
        
        
        self.cadreListBoxNomsExplicite.grid(row=1, column=1, columnspan=2)
        self.cadreListBoxVerbesExplicite.grid(row=1, column=3, columnspan=2)
        self.cadreListBoxAdjectifsExplicite.grid(row=1, column=5, columnspan=2)
        
        
        
        ###Implicite####################################################################################################################################
        self.cadreAnalyseImplicite=Frame(self.root)
        
        self.lblImplicite=Label(self.cadreAnalyseImplicite, text="Implicite :            ")
        self.btnNomsImplicite=Button(self.cadreAnalyseImplicite, text="Noms (objets)", command=self.ajouterNomImplicite)
        self.btnVerbesImplicite=Button(self.cadreAnalyseImplicite, text="Verbes (actions)", command=self.ajouterVerbeImplicite)
        self.btnAdjectifsImplicite=Button(self.cadreAnalyseImplicite, text="Adjectifs (attributs)", command=self.ajouterAdjectifImplicite)
        
        self.cadreListBoxNomsImplicite=Frame(self.cadreAnalyseImplicite)
        self.scrollbarNomsImplicite = Scrollbar(self.cadreListBoxNomsImplicite)
        self.scrollbarNomsImplicite.pack(side=RIGHT, fill=Y)
        self.listboxNomsImplicite = Listbox(self.cadreListBoxNomsImplicite, yscrollcommand=self.scrollbarNomsImplicite.set, height=6)
        self.listboxNomsImplicite.pack(side=LEFT, fill=BOTH)
        self.scrollbarNomsImplicite.config(command=self.listboxNomsImplicite.yview)
        
        
        self.cadreListBoxVerbesImplicite=Frame(self.cadreAnalyseImplicite)
        self.scrollbarVerbesImplicite = Scrollbar(self.cadreListBoxVerbesImplicite)
        self.scrollbarVerbesImplicite.pack(side=RIGHT, fill=Y)
        self.listboxVerbesImplicite = Listbox(self.cadreListBoxVerbesImplicite, yscrollcommand=self.scrollbarVerbesImplicite.set, height=6)
        self.listboxVerbesImplicite.pack(side=LEFT, fill=BOTH)
        self.scrollbarVerbesImplicite.config(command=self.listboxVerbesImplicite.yview)
        
        
        self.cadreListBoxAdjectifsImplicite=Frame(self.cadreAnalyseImplicite)
        self.scrollbarAdjectifsImplicite = Scrollbar(self.cadreListBoxAdjectifsImplicite)
        self.scrollbarAdjectifsImplicite.pack(side=RIGHT, fill=Y)
        self.listboxAdjectifsImplicite = Listbox(self.cadreListBoxAdjectifsImplicite, yscrollcommand=self.scrollbarAdjectifsImplicite.set, height=6)
        self.listboxAdjectifsImplicite.pack(side=LEFT, fill=BOTH)
        self.scrollbarAdjectifsImplicite.config(command=self.listboxVerbesImplicite.yview)
        
        
        self.btnSupprimerNomImp=Button(self.cadreAnalyseImplicite, text="Supprimer nom", command=self.supprimerNomImp)
        self.btnSupprimerVerbeImp=Button(self.cadreAnalyseImplicite, text="Supprimer verbe", command=self.supprimerVerbeImp)
        self.btnSupprimerAdjectifImp=Button(self.cadreAnalyseImplicite, text="Supprimer adjectif", command=self.supprimerAdjectifImp)
        
        self.lblImplicite.grid(row=0, column=0)
        
        self.btnNomsImplicite.grid(row=0, column=1)
        self.btnSupprimerNomImp.grid(row=0, column=2)
        self.btnVerbesImplicite.grid(row=0, column=3)
        self.btnSupprimerVerbeImp.grid(row=0, column=4)
        self.btnAdjectifsImplicite.grid(row=0, column=5)
        self.btnSupprimerAdjectifImp.grid(row=0, column=6)
        
        self.cadreListBoxNomsImplicite.grid(row=1, column=1, columnspan=2)
        self.cadreListBoxVerbesImplicite.grid(row=1, column=3, columnspan=2)
        self.cadreListBoxAdjectifsImplicite.grid(row=1, column=5, columnspan=2)
        
        
        
        
        
    ###Supplementaire####################################################################################################################################
        self.cadreAnalyseSupplementaire=Frame(self.root)
        
        self.lblSupplementaire=Label(self.cadreAnalyseSupplementaire, text="Supplémentaire : ")
        self.btnNomsSupplementaire=Button(self.cadreAnalyseSupplementaire, text="Noms (objets)", command=self.ajouterNomSupplementaire)
        self.btnVerbesSupplementaire=Button(self.cadreAnalyseSupplementaire, text="Verbes (actions)", command=self.ajouterVerbeSupplementaire)
        self.btnAdjectifsSupplementaire=Button(self.cadreAnalyseSupplementaire, text="Adjectifs (attributs)", command=self.ajouterAdjectifSupplementaire)
        
        self.cadreListBoxNomsSupplementaire=Frame(self.cadreAnalyseSupplementaire)
        self.scrollbarNomsSupplementaire = Scrollbar(self.cadreListBoxNomsSupplementaire)
        self.scrollbarNomsSupplementaire.pack(side=RIGHT, fill=Y)
        self.listboxNomsSupplementaire = Listbox(self.cadreListBoxNomsSupplementaire, yscrollcommand=self.scrollbarNomsSupplementaire.set, height=6)
        self.listboxNomsSupplementaire.pack(side=LEFT, fill=BOTH)
        self.scrollbarNomsSupplementaire.config(command=self.listboxNomsSupplementaire.yview)
        
        
        self.cadreListBoxVerbesSupplementaire=Frame(self.cadreAnalyseSupplementaire)
        self.scrollbarVerbesSupplementaire = Scrollbar(self.cadreListBoxVerbesSupplementaire)
        self.scrollbarVerbesSupplementaire.pack(side=RIGHT, fill=Y)
        self.listboxVerbesSupplementaire = Listbox(self.cadreListBoxVerbesSupplementaire, yscrollcommand=self.scrollbarVerbesSupplementaire.set, height=6)
        self.listboxVerbesSupplementaire.pack(side=LEFT, fill=BOTH)
        self.scrollbarVerbesSupplementaire.config(command=self.listboxVerbesImplicite.yview)
        
        
        self.cadreListBoxAdjectifsSupplementaire=Frame(self.cadreAnalyseSupplementaire)
        self.scrollbarAdjectifsSupplementaire = Scrollbar(self.cadreListBoxAdjectifsSupplementaire)
        self.scrollbarAdjectifsSupplementaire.pack(side=RIGHT, fill=Y)
        self.listboxAdjectifsSupplementaire = Listbox(self.cadreListBoxAdjectifsSupplementaire, yscrollcommand=self.scrollbarAdjectifsSupplementaire.set, height=6)
        self.listboxAdjectifsSupplementaire.pack(side=LEFT, fill=BOTH)
        self.scrollbarAdjectifsSupplementaire.config(command=self.listboxVerbesSupplementaire.yview)
        
        self.btnSupprimerNomSup=Button(self.cadreAnalyseSupplementaire, text="Supprimer nom", command=self.supprimerNomSup)
        self.btnSupprimerVerbeSup=Button(self.cadreAnalyseSupplementaire, text="Supprimer verbe", command=self.supprimerVerbeSup)
        self.btnSupprimerAdjectifSup=Button(self.cadreAnalyseSupplementaire, text="Supprimer adjectif", command=self.supprimerAdjectifSup)
        
        
        
        self.lblSupplementaire.grid(row=0, column=0)
        
        self.btnNomsSupplementaire.grid(row=0, column=1)
        self.btnSupprimerNomSup.grid(row=0, column=2)
        self.btnVerbesSupplementaire.grid(row=0, column=3)
        self.btnSupprimerVerbeSup.grid(row=0, column=4)
        self.btnAdjectifsSupplementaire.grid(row=0, column=5)
        self.btnSupprimerAdjectifSup.grid(row=0, column=6)
        
        
        self.cadreListBoxNomsSupplementaire.grid(row=1, column=1, columnspan=2)
        self.cadreListBoxVerbesSupplementaire.grid(row=1, column=3, columnspan=2)
        self.cadreListBoxAdjectifsSupplementaire.grid(row=1, column=5, columnspan=2)
        
        
        self.fichierTexte=Text(self.cadreFichier, height=15, width=100)
        self.fichierTexte.pack()
        self.cadreFichier.pack()
        
        self.cadreCreationMandat.pack()
        
        
        #self.btnOuvrirFichier.pack()
        self.entryMotAAjouter.pack()
        self.cadreAnalyseExplicite.pack()
        self.cadreAnalyseImplicite.pack()
        self.cadreAnalyseSupplementaire.pack()
        
        
    
        
    
    #explicite
    def ajouterNomExplicite(self):
        try:
            mot=self.fichierTexte.get(SEL_FIRST, SEL_LAST)
            contenuListBox=self.listboxNomsExplicite.get(0, END)
            print("ajout nom ex", mot, contenuListBox)
            if(mot!="" and mot not in contenuListBox):
                self.listboxNomsExplicite.insert(END, mot)
                self.parent.modele.mandatActif.creerNom(mot, 1)
        except:
            print("Sélectionnez un mot")
    
    def ajouterVerbeExplicite(self):
        try:
            mot=self.fichierTexte.get(SEL_FIRST, SEL_LAST)
            contenuListBox=self.listboxVerbesExplicite.get(0, END)
            print("ajout verbe ex", mot, contenuListBox)
            if(mot!="" and mot not in contenuListBox):
                self.listboxVerbesExplicite.insert(END, mot)
                self.parent.modele.mandatActif.creerVerbe(mot, 1)
        except:
            print("Sélectionnez un mot")
    
    def ajouterAdjectifExplicite(self):
        try:
            mot=self.fichierTexte.get(SEL_FIRST, SEL_LAST)
            contenuListBox=self.listboxAdjectifsExplicite.get(0, END)
            print("ajout adjectif ex", mot, contenuListBox)
            if(mot!="" and mot not in contenuListBox):
                self.listboxAdjectifsExplicite.insert(END, mot)
                self.parent.modele.mandatActif.creerAttribut(mot, 1)
        except:
            print("Sélectionnez un mot")
    
    
    #implicite
    def ajouterNomImplicite(self):
        mot=self.entryMotAAjouter.get()
        contenuListBox=self.listboxNomsImplicite.get(0, END)
        print("ajout nom imp", mot, contenuListBox)
        if(mot!="" and mot not in contenuListBox):
            self.listboxNomsImplicite.insert(END, mot)
            self.parent.modele.mandatActif.creerNom(mot, 2)
        
    
    def ajouterVerbeImplicite(self):
        mot=self.entryMotAAjouter.get()
        contenuListBox=self.listboxVerbesImplicite.get(0, END)
        print("ajout verbe imp", mot, contenuListBox)
        if(mot!="" and mot not in contenuListBox):
            self.listboxVerbesImplicite.insert(END, mot)
            self.parent.modele.mandatActif.creerVerbe(mot, 2)
    
    
    def ajouterAdjectifImplicite(self):
        mot=self.entryMotAAjouter.get()
        contenuListBox=self.listboxAdjectifsImplicite.get(0, END)
        print("ajout adjectif imp", mot, contenuListBox)
        if(mot!="" and mot not in contenuListBox):
            self.listboxAdjectifsImplicite.insert(END, mot)
            self.parent.modele.mandatActif.creerAttribut(mot, 2)
    
    #Supplementaire
    def ajouterNomSupplementaire(self):
        mot=self.entryMotAAjouter.get()
        contenuListBox=self.listboxNomsSupplementaire.get(0, END)
        print("ajout nom sup", mot, contenuListBox)
        if(mot!="" and mot not in contenuListBox):
            self.listboxNomsSupplementaire.insert(END, mot)
            self.parent.modele.mandatActif.creerNom(mot, 3)
    
    def ajouterVerbeSupplementaire(self):
        mot=self.entryMotAAjouter.get()
        contenuListBox=self.listboxVerbesSupplementaire.get(0, END)
        print("ajout verbe sup", mot, contenuListBox)
        if(mot!="" and mot not in contenuListBox):
            self.listboxVerbesSupplementaire.insert(END, mot)
            self.parent.modele.mandatActif.creerVerbe(mot, 3)
    
    def ajouterAdjectifSupplementaire(self):
        mot=self.entryMotAAjouter.get()
        contenuListBox=self.listboxAdjectifsSupplementaire.get(0, END)
        print("ajout adjectif sup", mot, contenuListBox)
        if(mot!="" and mot not in contenuListBox):
            self.listboxAdjectifsSupplementaire.insert(END, mot)
            self.parent.modele.mandatActif.creerAttribut(mot, 3)
    
    
    
    def importerMandat(self):
        pass
    
    
    def ouvrirFichier(self):
        self.fichierTexte.delete(1.0, END)
        nomFichier=filedialog.askopenfilename()
        if nomFichier:
            fichier=open(nomFichier,'r')
            fic=fichier.read()
            self.fichierTexte.insert(1.0, fic)
            fichier.close()
        self.root.iconify()
        self.root.deiconify()
    
    def creerMandat(self):
        self.ouvrirFichier()
        contenuTexte=self.fichierTexte.get(1.0, END)
        print(contenuTexte)
        self.parent.modele.creerMandat(contenuTexte)
        
        
    
    
    def enregistrerSurBD(self):
        self.parent.modele.enregistrerBD()
    
    def supprimerUnMandat(self):
        self.parent.modele.supprimerMandat()
    
    
    
    
    def supprimerNomEx(self):
        if self.listboxNomsExplicite.curselection():
            mot = self.listboxNomsExplicite.get(self.listboxNomsExplicite.curselection())
            self.parent.modele.mandatActif.supprimerNom(mot, 1)
            selection=self.listboxNomsExplicite.curselection()
            self.listboxNomsExplicite.delete(selection[0])
        
    
    def supprimerVerbeEx(self):
        if self.listboxVerbesExplicite.curselection():
            mot = self.listboxVerbesExplicite.get(self.listboxVerbesExplicite.curselection())
            self.parent.modele.mandatActif.supprimerVerbe(mot, 1)
            selection=self.listboxVerbesExplicite.curselection()
            self.listboxVerbesExplicite.delete(selection[0])
    
    def supprimerAdjectifEx(self):
        if self.listboxAdjectifsExplicite.curselection():
            mot = self.listboxAdjectifsExplicite.get(self.listboxAdjectifsExplicite.curselection())
            self.parent.modele.mandatActif.supprimerAdjectif(mot, 1)
            selection=self.listboxAdjectifsExplicite.curselection()
            self.listboxAdjectifsExplicite.delete(selection[0])
    
    
    
    def supprimerNomImp(self):
        if self.listboxNomsImplicite.curselection():
            mot = self.listboxNomsImplicite.get(self.listboxNomsImplicite.curselection())
            self.parent.modele.mandatActif.supprimerNom(mot, 2)
            selection=self.listboxNomsImplicite.curselection()
            self.listboxNomsImplicite.delete(selection[0])
    
    def supprimerVerbeImp(self):
        if self.listboxVerbesImplicite.curselection():
            mot = self.listboxVerbesImplicite.get(self.listboxVerbesImplicite.curselection())
            self.parent.modele.mandatActif.supprimerVerbe(mot, 2)
            selection=self.listboxVerbesImplicite.curselection()
            self.listboxVerbesImplicite.delete(selection[0])
    
    def supprimerAdjectifImp(self):
        if self.listboxAdjectifsImplicite.curselection():
            mot = self.listboxAdjectifsImplicite.get(self.listboxAdjectifsImplicite.curselection())
            self.parent.modele.mandatActif.supprimerAdjectif(mot, 2)
            selection=self.listboxAdjectifsImplicite.curselection()
            self.listboxAdjectifsImplicite.delete(selection[0])
    
    
    
    def supprimerNomSup(self):
        if self.listboxNomsSupplementaire.curselection():
            mot = self.listboxNomsSupplementaire.get(self.listboxNomsSupplementaire.curselection())
            self.parent.modele.mandatActif.supprimerNom(mot, 3)
            selection=self.listboxNomsSupplementaire.curselection()
            self.listboxNomsSupplementaire.delete(selection[0])
    
    def supprimerVerbeSup(self):
        if self.listboxVerbesSupplementaire.curselection():
            mot = self.listboxVerbesSupplementaire.get(self.listboxVerbesSupplementaire.curselection())
            self.parent.modele.mandatActif.supprimerVerbe(mot, 3)
            selection=self.listboxVerbesSupplementaire.curselection()
            self.listboxVerbesSupplementaire.delete(selection[0])
    
    def supprimerAdjectifSup(self):
        if self.listboxAdjectifsSupplementaire.curselection():
            mot = self.listboxAdjectifsSupplementaire.get(self.listboxAdjectifsSupplementaire.curselection())
            self.parent.modele.mandatActif.supprimerAdjectif(mot, 3)
            selection=self.listboxAdjectifsSupplementaire.curselection()
            self.listboxAdjectifsSupplementaire.delete(selection[0])
    
    
    
    def salutations(self):
        print("HOURRA SA MARCHE")
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    