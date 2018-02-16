# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
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
        self.afficherModules()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def CreerCadreCRC(self):
        #cadre principal projet
        self.frameCRC=Frame(self.root,bg="green")
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
        self.btnAjoutCollaborateur.pack(side=LEFT)
        #ligne 3
        self.frameLigne3=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne3.pack(fill=X,expand=1)
        self.frameNomResponsabilite=LabelFrame(self.frameLigne3,text="Responsabilité:",bg=self.couleurBG)
        self.frameNomResponsabilite.pack(side=LEFT,fill=X,expand=1)
        self.txtNomResponsabilite=Entry(self.frameNomResponsabilite)
        self.txtNomResponsabilite.pack(fill=X)
        self.btnAjoutResponsabilite=Button(self.frameLigne3,text="Ajouter",command=self.ajoutResponsabilite)
        self.btnAjoutResponsabilite.pack(side=LEFT)
       #ligne 4
        self.frameLigne4=LabelFrame(self.frameDroit,text="Liste collaborateur: ",width=400,height=100,bg=self.couleurBG)
        self.frameLigne4.pack(fill=X,expand=1)
        self.listeCollaborateur=Listbox(self.frameLigne4,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        self.listeCollaborateur.bind('<<ListboxSelect>>', self.changementCollaborateur)
        self.listeCollaborateur.pack(fill=BOTH,expand=1)
        #ligne 5
        self.frameLigne5=LabelFrame(self.frameDroit,text="Liste responsabilité: ",width=400,height=100,bg=self.couleurBG)
        self.frameLigne5.pack(fill=X,expand=1)
        self.listeResponsabilite=Listbox(self.frameLigne5,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        self.listeResponsabilite.bind('<<ListboxSelect>>', self.changementResponsabilite)
        self.listeResponsabilite.pack(fill=BOTH,expand=1)
       #ligne 6
        self.frameLigne6=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne6.pack(fill=X,expand=1)
        self.btnSuivant=Button(self.frameLigne6,text="Suivant",command=self.suivant)
        self.btnSuivant.pack(side=RIGHT)
 
    def afficherModules(self):
        self.cadreModules=Frame(self.root)
        self.cadremodule=Frame(self.cadreModules)
        self.canevaModules=Canvas(self.cadremodule,width=640,height=480,bg="green")
        self.canevaModules.pack(side=LEFT)
        
        self.listemodules=Listbox(self.cadremodule,bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        self.ipcentral=Entry(self.cadremodule, bg="pink")
        #self.ipcentral.insert(0, self.monip)
        btnconnecter=Button(self.cadremodule, text="Choisir un module",bg="pink",command=self.choisirModule)
        self.canevaModules.create_window(200,100,window=self.listemodules)
        self.canevaModules.create_window(200,450,window=btnconnecter,width=100,height=30)
        self.cadremodule.pack(side=LEFT)
    
    def ajoutCrc(self):
        rep = self.modele.ajoutCRC(str(self.txtNomCrc.get()), self.modele.nomUser, [])
        print(rep)
        self.Tri()
        
    def ajoutResponsabilite(self):
        print("ajout responsabilite")
        
    def ajoutCollaborateur(self):
        selection = self.CRCcourant.id
        rep = self.parent.ajoutCollab(selection, self.txtNomCollaborateur.get())
        print(rep)
        self.Tri()
    
    def requeteModule(self):
        self.parent.chargerModules();
    
    def changementCRC(self,event):
        self.chargeCRC()
        self.effaceChamp()
        self.txtNomCrc.insert(0,self.modele.listeCRC[self.listeVarCRC.curselection()[0]].nom)
        if self.CRCcourant.collaboration != []:
            for collab in self.CRCcourant.collaboration:
                for crc in self.modele.listeCRC:
                    if collab[0] == crc.id:
                        self.listeCollaborateur.insert(END,crc.nom)
        
    def chargeCRC(self):
        self.CRCcourant = self.listeCRC[self.listeVarCRC.curselection()[0]]
        self.btnAjoutCrc.pack_forget()
#         self.txtNomResponsabilite.insert(END,self.listeCRC[self.listeVarCrc.curselection()[0]].resp)   
    def changementCollaborateur(self,event):
        print("changement collaborateur")
        
    def changementResponsabilite(self,event):
        print("changement responsabilite")
     
#     def dtValidateur(self,champDt):
#         try:
#             date=datetime.datetime.strptime(champDt.get(),"%Y/%m/%d").date()
#             if (date>self.dateJour):
#                 print("date trop grand")
#         except:
#             print("Format de date non valide")
#             return False
#         return True
#         
#     
#     def effaceDernier(self,btn,date):
#         btn.delete(0,END)
#         date=date[:-1]
#         btn.insert(0,date)
#     
#     def dtCheck(self,Event):
#         self.date=Event.widget.get()
#         if (not self.date[len(self.date)-1] in '0123456789'):
#             #efface dernier carac non valide
#             self.effaceDernier(Event.widget,self.date)
#         #ajout automatique / pour faire date format aaaa/mm/dd
#         if (len(self.date)==4 or len(self.date)==7):
#             self.date+="/"
#             Event.widget.insert(END,"/")
#         #si trop long enlève dernier caractère
#         elif(len(self.date)>10):
#             self.effaceDernier(Event.widget,self.date)
#     
       
    def suivant(self):
        print("suivant")
        self.requeteModule()
    
    def Enregistrer(self):
        pass
    
    def setEnregistrer(self):
        pass
         
    
    def Annuler(self):
        self.btnAjoutCrc.pack(side=LEFT)
        self.listeVarCRC.selection_clear(0,self.listeVarCRC.size())
        self.initChamp()
        print("Je veux annuler")
        #self.listeCRC.selection_clear(0,self.listeCRC.size())
    
    def effaceChamp(self):
#         champ texte à vide
        self.txtNomCrc.delete(0,END)
        self.txtNomCollaborateur.delete(0,END)
        self.txtNomResponsabilite.delete(0,END)
        self.listeCollaborateur.delete(0,self.listeCollaborateur.size())
       
    def initChamp(self):
        self.effaceChamp()
        #self.changementProjet(0)
        #self.listeStatut.set(self.listeVarStatut[0])
        #self.txtDtCreation.insert(0,"%s/%s/%s" % (self.dateJour.year,self.dateJour.month,self.dateJour.day) )
        
    def Tri(self):
        self.listeVarCRC.delete(0, self.listeVarCRC.size())
        if (self.chVarTri.get()==0):
            print("affichage actif")
            for n in self.listeCRC:
                self.listeVarCRC.insert(END,n.nom)
        else:
            print("affichage inactif")
            for n in self.listeCRC:
                self.listeVarCRC.insert(END,n.nom)
                
    def chargerModules(self,repmodules):
        for i in repmodules:
            self.listemodules.insert(END,i)
      
    def choisirModule(self):
        mod=self.listemodules.selection_get()
        if mod:
            self.parent.requetemodule(mod)
        
    def fermerfenetre(self):
        print("ONFERME la fenetre")