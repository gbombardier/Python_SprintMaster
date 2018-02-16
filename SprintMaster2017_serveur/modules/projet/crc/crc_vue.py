# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from PIL.FontFile import WIDTH
from tkinter.ttk import Combobox
from tkinter.constants import LEFT
import datetime
#import dateutil.parser

class Vue():
    def __init__(self,parent,modele,largeur=800,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=modele
        self.listeCRC = self.modele.listeCRC
        self.dateJour=datetime.datetime.today().date()
        self.couleurBG="white"
        self.chVarTri=BooleanVar()
        self.idCrc=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.frameCRC)
        self.CRCcourant=None
        self.center(self.root)
    
    
    def center(self,toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
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
        #self.creercadresplash()
        self.CreerCadreCRC()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def CreerCadreCRC(self):
        #cadre principal projet
        self.frameCRC=Frame(self.root,bg=self.couleurBG)
        #cadre gauche
        self.frameGauche=Frame(self.frameCRC,width=200,height=600,bg=self.couleurBG)
        self.frameGauche.pack_propagate(FALSE)
        self.frameGauche.pack(side=LEFT)
        self.frameListeCRC=LabelFrame(self.frameGauche,text="Liste CRC",bg=self.couleurBG)
        self.frameListeCRC.pack(fill=BOTH,expand=1)
        self.listeVarCRC=Listbox(self.frameListeCRC,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        self.listeVarCRC.bind('<<ListboxSelect>>', self.changementCRC)
        self.listeVarCRC.pack(fill=BOTH,expand=1)
        self.chboxTri=Checkbutton(self.frameGauche,text="Afficher inactif",variable=self.chVarTri,onvalue=1,offvalue=0,height=1,width=40,pady=10,bg=self.couleurBG,command=self.Tri)
        self.chboxTri.pack()
        self.btnAnnuler=Button(self.frameGauche,text="Annuler",command=self.Annuler)
        self.btnAnnuler.pack(side=BOTTOM)
        #charger liste
        self.Tri()
        #cadre droit
        self.frameDroit=Frame(self.frameCRC,width=400,height=600,bg=self.couleurBG)
        self.frameDroit.pack_propagate(FALSE)
        self.frameDroit.pack(side=LEFT)
        
        #ligne 1
        self.frameLigne1=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne1.pack(fill=X,expand=1)
        self.frameNomCrc=LabelFrame(self.frameLigne1,text="Nom du crc:",bg=self.couleurBG)
        self.frameNomCrc.pack(side=LEFT,fill=X,expand=1)
        self.txtNomCrc=Entry(self.frameNomCrc)
        self.txtNomCrc.pack(fill=X)
        self.btnAjoutCrc=Button(self.frameLigne1,text="Ajouter",command=self.ajoutCrc)
        self.btnAjoutCrc.pack(side=LEFT)
        
       #ligne 2
        self.frameLigne2=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne2.pack(fill=X,expand=1)
        self.frameNomCollaborateur=LabelFrame(self.frameLigne2,text="Collaborateur:",bg=self.couleurBG)
        self.frameNomCollaborateur.pack(side=LEFT,fill=X,expand=1)
        self.txtNomCollaborateur=Entry(self.frameNomCollaborateur)
        self.txtNomCollaborateur.pack(fill=X)
        self.btnAjoutCollaborateur=Button(self.frameLigne2,text="Ajouter",command=self.ajoutCollaborateur)

        #ligne 3
        self.frameLigne3=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne3.pack(fill=X,expand=1)
        self.frameNomResponsabilite=LabelFrame(self.frameLigne3,text="Responsabilité:",bg=self.couleurBG)
        self.frameNomResponsabilite.pack(side=LEFT,fill=X,expand=1)
        self.txtNomResponsabilite=Entry(self.frameNomResponsabilite)
        self.txtNomResponsabilite.pack(fill=X)
        self.btnAjoutResponsabilite=Button(self.frameLigne3,text="Ajouter",command=self.ajoutResponsabilite)
        
       #ligne 4
        self.frameLigne4=LabelFrame(self.frameDroit,text="Liste collaborateur: ",width=400,height=100,bg=self.couleurBG)
        self.frameLigne4.pack(fill=X,expand=1)
        self.listeCollaborateur=Listbox(self.frameLigne4,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        self.listeCollaborateur.pack(fill=BOTH,expand=1)
        #ligne 5
        self.frameLigne5=LabelFrame(self.frameDroit,text="Liste responsabilité: ",width=400,height=100,bg=self.couleurBG)
        self.frameLigne5.pack(fill=X,expand=1)
        self.listeResponsabilite=Listbox(self.frameLigne5,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        self.listeResponsabilite.pack(fill=BOTH,expand=1)
       #ligne 6
        self.frameLigne6=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne6.pack(fill=X,expand=1)
        self.btnSuivant=Button(self.frameLigne6,text="Suivant",command=self.suivant)
        self.btnSuivant.pack(side=RIGHT)
        
        #cadre Cas Usage
        self.cadreCU= Frame(self.frameCRC, width=300, height=600, bg=self.couleurBG)
        self.cadreCU.pack(side=RIGHT)
        self.tree = ttk.Treeview(self.cadreCU)
        self.tree['show'] = 'headings'
        self.tree["columns"]=("Cas d'usage","Attribué")
        self.tree.column("Cas d'usage", width=200, anchor="c" )
        self.tree.column("Attribué", width=100, anchor="c")
        
        self.tree.heading("Cas d'usage", text="Cas d'usage")
        self.tree.heading("Attribué", text="Attribué")
        self.treeValues = []
        self.importerCasUsage()
        
        
    def importerCasUsage(self):

        listeCasUsage = self.parent.importerCasUsage()
        
        if self.treeValues != []:
            for item in self.treeValues:
                self.tree.delete(item)

        self.treeValues=[]
        self.treeValues.append(self.tree.insert("", "end", values=("Pas un cas d'usage","--")))
        self.tree.pack(side=RIGHT)
        
        for cas in listeCasUsage:
            if cas == "V":
                return 0
            if cas[1] == 1:
                cas[1] = "Attribué"
            else:
                cas[1] = "Non attribué"
            self.treeValues.append(self.tree.insert("","end", values=(cas[0],cas[1])))
        
        
    
    def ajoutCrc(self):
        if self.txtNomCrc.get() != "":
            rep = self.modele.ajoutCRC(str(self.txtNomCrc.get()), self.modele.nomUser, [])
            self.CRCcourant = rep
            self.Tri()
            self.listeVarCRC.selection_set(END, END)
            self.btnAjoutResponsabilite.pack(side=LEFT)
            self.btnAjoutCollaborateur.pack(side=LEFT)
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom de CRC.")
        
    def ajoutResponsabilite(self):
        if self.txtNomResponsabilite.get() != "":
            selection = self.CRCcourant.id
            cas = self.tree.item(self.tree.focus())
            if cas.get('values') == '':
                messagebox.showwarning("Erreur","Veuillez choisir un cas d'usage.")
            else:
                rep = self.parent.ajoutResp(selection, self.txtNomResponsabilite.get(), cas.get('values')[0])
                self.listeResponsabilite.delete(0,END)
                for crc in self.modele.listeCRC:
                    if selection == crc.id:
                        for resp in self.modele.listeResp:
                            if resp.idCRC == selection:
                                self.listeResponsabilite.insert(END, resp.nom)
        else:
            messagebox.showwarning("Erreur","Veuillez entrer un nom de responsabilité.")
                        
        
    def ajoutCollaborateur(self):
        if self.txtNomCollaborateur.get() != "":
            selection = self.CRCcourant.id
            rep = self.parent.ajoutCollab(selection, self.txtNomCollaborateur.get())
            if self.CRCcourant.collaboration != []:
                self.listeCollaborateur.delete(0,END)
                for collab in self.CRCcourant.collaboration:
                    for crc in self.modele.listeCRC:
                        if collab == crc.id:
                            self.listeCollaborateur.insert(END,crc.nom)
                            return 0

            messagebox.showwarning("Erreur", "La classe collaboratrice doit exister.")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom de collaborateur.")
            return 0
        

    
    def requeteModule(self):
        self.parent.chargerModules();
    
    def changementCRC(self,event):
        if self.modele.listeCRC != []:
            self.btnAjoutResponsabilite.pack(side=LEFT)
            self.btnAjoutCollaborateur.pack(side=LEFT)
            self.chargeCRC()
            self.effaceChamp()
            self.txtNomCrc.insert(0,self.modele.listeCRC[self.listeVarCRC.curselection()[0]].nom)
            if self.CRCcourant.collaboration != []:
                for collab in self.CRCcourant.collaboration:
                    for crc in self.modele.listeCRC:
                        if collab == crc.id:
                            self.listeCollaborateur.insert(END,crc.nom)
            if self.modele.listeResp != []:
                for crc in self.modele.listeCRC:
                    if self.CRCcourant.id == crc.id:
                        for resp in self.modele.listeResp:
                            if resp.idCRC == self.CRCcourant.id:
                                self.listeResponsabilite.insert(END, resp.nom)
        
    def chargeCRC(self):
        if (self.modele.listeCRC != []):
            self.CRCcourant = self.modele.listeCRC[self.listeVarCRC.curselection()[0]]
            self.btnAjoutCrc.pack_forget()
#         self.txtNomResponsabilite.insert(END,self.listeCRC[self.listeVarCrc.curselection()[0]].resp)   
        
    def suivant(self):
#         self.changecadre(self.cadreModules)
#         self.requeteModule()
        self.parent.requeteModules("planif")         
    
    def Annuler(self):
        self.btnAjoutCrc.pack(side=LEFT)
        self.listeVarCRC.selection_clear(0,self.listeVarCRC.size())
        self.initChamp()
        self.btnAjoutCollaborateur.pack_forget()
        self.btnAjoutResponsabilite.pack_forget()
    
    def effaceChamp(self):
#         champ texte à vide
        self.txtNomCrc.delete(0,END)
        self.txtNomCollaborateur.delete(0,END)
        self.txtNomResponsabilite.delete(0,END)
        self.listeCollaborateur.delete(0,self.listeCollaborateur.size())
        self.listeResponsabilite.delete(0,END)
       
    def initChamp(self):
        self.effaceChamp()
        #self.changementProjet(0)
        #self.listeStatut.set(self.listeVarStatut[0])
        #self.txtDtCreation.insert(0,"%s/%s/%s" % (self.dateJour.year,self.dateJour.month,self.dateJour.day) )
        
    def Tri(self):
        self.listeVarCRC.delete(0, self.listeVarCRC.size())
        if (self.chVarTri.get()==0):
            for n in self.listeCRC:
                self.listeVarCRC.insert(END,n.nom)
        else:
            for n in self.listeCRC:
                self.listeVarCRC.insert(END,n.nom)
                
        
    def fermerfenetre(self):
        self.root.destroy()