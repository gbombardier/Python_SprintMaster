# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from cas_usage import *
from helper import Helper as hlp
from _overlapped import NULL
from tkinter import messagebox

class Vue():
    def __init__(self,parent,largeur=800,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.titreafficher= "le titre va etre affiché icitte"
        self.creercadres()
        self.compteurcreerCadre=0
        self.changecadre(self.cadrescenario)
        

        
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
        self.creercadrescenario()
        self.creercadresAjouterTitre()
        self.creercadresAjouterCas()
        self.creercadreAfficherCas()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def creercadrescenario(self):
        self.cadrescenario=Frame(self.root)
        self.canevascenario=Canvas(self.cadrescenario,width=400,height=450,bg="white")
        self.canevascenario.pack()

        self.listecas=Listbox(self.cadrescenario,bg="lightgray",borderwidth=0,relief=FLAT,width=50,height=10)
        self.canevascenario.create_window(200,150,window=self.listecas)
        
       
        rep=self.parent.afficherLesCas()
        if rep!="Vide":
            for n in rep:
                self.listecas.insert(END, n[0])
                
        
        self.btnajouter=Button(text="Ajouter",bg="lightgray",command=self.ajoutertitre)
        self.btnafficher=Button(text="Afficher",bg="lightgray",command=self.afficherscenario)
        self.btnretirer=Button(text="Retirer",bg="lightgray",command=self.retirerscenario)

        self.canevascenario.create_window(150,300,window=self.btnafficher,width=100,height=30)
        self.canevascenario.create_window(275,300,window=self.btnretirer,width=100,height=30)
        self.canevascenario.create_window(350,20,window=self.btnajouter,width=100,height=30)
        
        self.btnSuivant=Button(text="Suivant",bg="lightgray",command=self.suivant)
        self.canevascenario.create_window(300,400,window=self.btnSuivant,width=100,height=30)
        
    def creercadresAjouterTitre(self):
        self.cadreAjouterTitre=Frame(self.root)
        self.canevaAjouter=Canvas(self.cadreAjouterTitre,width=400,height=350,bg="white")
        self.canevaAjouter.pack()
        
        self.titreInsertion=Entry(bg="lightgray")
        self.titreInsertion.insert(0, "Entrez votre titre ici")
        self.titreTitre=Label(text="Titre : ", bg= "white")
        self.btnTitre=Button(text="Ajouter",bg="lightgray",command=self.ajoutercas)
        
        self.canevaAjouter.create_window(55,100,window=self.titreTitre,width=100,height=30)
        self.canevaAjouter.create_window(205,130,window=self.titreInsertion,width=400,height=30)
        self.canevaAjouter.create_window(180,300,window=self.btnTitre,width=100,height=30)
        
        
    def creercadresAjouterCas(self):
        self.cadreAjouterCas=Frame(self.root)
        self.canevaAjouterCas=Canvas(self.cadreAjouterCas,width=400,height=350,bg="white")
        self.canevaAjouterCas.pack()
        
        self.casInsertion=Entry(bg="lightgray")
        self.casInsertion.insert(0, "Entrez votre interaction ici")
        self.titreTitre=Label(text="Interaction:  ", bg= "white")
        
        self.btnTermine=Button(text="Terminé",bg="lightgray",command=self.termine)
        self.btnOrdinateur=Button(text="Ordinateur",bg="lightgray",command=self.ajoutercasordi)
        self.btnUtilisateur=Button(text="Utilisateur",bg="lightgray",command=self.ajoutercasusager)
        
        self.canevaAjouterCas.create_window(55,100,window=self.titreTitre,width=100,height=30)
        self.canevaAjouterCas.create_window(210,130,window=self.casInsertion,width=400,height=30)
        self.canevaAjouterCas.create_window(180,300,window=self.btnTermine,width=100,height=30)
        self.canevaAjouterCas.create_window(100,200,window=self.btnOrdinateur,width=100,height=30)
        self.canevaAjouterCas.create_window(260,200,window=self.btnUtilisateur,width=100,height=30)
        
    def creercadreAfficherCas(self):
        self.cadreAfficherCas=Frame(self.root)
        self.canevaAfficherCas=Canvas(self.cadreAfficherCas,width=900,height=500,bg="white")
        self.canevaAfficherCas.pack()
        
        
        self.entreeTitre=Entry(text=self.titreafficher, bg="lightgray")
        self.lblOrdi=Label (text="Ordinateur: ", bg="white")
        self.lblUser=Label(text="Usager: ", bg="white")
        
        self.listeOrdinateur=Listbox(self.cadreAfficherCas,bg="lightgray",borderwidth=0,relief=FLAT,width=50,height=20)
        
        self.listeUsager=Listbox(self.cadreAfficherCas,bg="lightgray",borderwidth=0,relief=FLAT,width=50,height=20)
        
        self.btnChangerTitre=Button(text="Modifier titre", bg="lightgray", command=self.modifierTitre)
        self.btnModifier=Button(text="Modifier",bg="lightgray",command=self.modifierscenario)
        self.btnRetour=Button (text= "Retour", bg="lightgray", command=self.termine)
        self.entreeMachine=Entry(bg="lightgray")
        self.entreeUser=Entry(bg="lightgray")
        self.btnAjouterUser=Button(text="Ajouter", bg="lightgray", command=self.ajouterCasUsagerMenu)
        self.btnAjouterMachine=Button(text="Ajouter", bg="lightgray", command=self.ajouterCasOrdiMenu)


        
        self.canevaAfficherCas.create_window(350,30,window=self.entreeTitre,width=400,height=30)
        self.canevaAfficherCas.create_window(150,70,window=self.lblOrdi,width=100,height=30)
        self.canevaAfficherCas.create_window(500,70,window=self.lblUser,width=100,height=30)
        self.canevaAfficherCas.create_window(250,250,window=self.listeOrdinateur)
        self.canevaAfficherCas.create_window(600,250,window=self.listeUsager)
        self.canevaAfficherCas.create_window(50,30, window=self.btnRetour, width=100, height=30)
        self.canevaAfficherCas.create_window(550,30,window=self.btnChangerTitre,width=100,height=30)
        self.canevaAfficherCas.create_window(425,470,window=self.btnModifier,width=100,height=30)
        self.canevaAfficherCas.create_window(250,425,window=self.entreeMachine,width=300,height=30)
        self.canevaAfficherCas.create_window(600,425,window=self.entreeUser,width=300,height=30)
        self.canevaAfficherCas.create_window(370,425,window=self.btnAjouterMachine,width=60,height=30)
        self.canevaAfficherCas.create_window(720,425,window=self.btnAjouterUser,width=60,height=30)
        
    def creercadresModifierCas(self):
        self.cadreModifierCas=Frame(self.root)
        self.canevaModifierCas=Canvas(self.cadreModifierCas,width=400,height=350,bg="white")
        self.canevaModifierCas.pack()
        
        self.entreeDescription=Entry(text="", bg="lightgray")
        self.entreeDescription.insert(0,str(self.descAfficher))
        self.entreeOrdre=Entry(text="", bg="lightgray")
        self.entreeOrdre.insert(0,str(self.ordreAfficher))
        self.labelDescription=Label(text="Description: ", bg="white")
        self.labelOrdre=Label(text="Ordre: ", bg="white")
        
        self.btnDescription=Button(text="Modifier", bg="lightgray", command=self.modifierDescription)
        self.btnOrdre=Button(text="Modifier", bg="lightgray", command=self.modifierOrdre)
        self.btnRetirer=Button(text="Retirer", bg="lightgray", command=self.retirerCasUserMachine)
        self.btnBack=Button(text="Retour", bg="lightgray", command=self.termine)
        
        self.canevaModifierCas.create_window(80,70,window=self.labelDescription,width=100,height=30)
        self.canevaModifierCas.create_window(80,140,window=self.labelOrdre,width=100,height=30)
        self.canevaModifierCas.create_window(240,70,window=self.entreeDescription,width=200,height=30)
        self.canevaModifierCas.create_window(240,140,window=self.entreeOrdre,width=200,height=30)
        self.canevaModifierCas.create_window(350,70,window=self.btnDescription,width=100,height=30)
        self.canevaModifierCas.create_window(350,140,window=self.btnOrdre,width=100,height=30)
        self.canevaModifierCas.create_window(200,330,window=self.btnRetirer,width=100,height=30)
        self.canevaModifierCas.create_window(50,25, window=self.btnBack, width=100, height=30)       
        
    def retour(self):
        self.changecadre(self.cadreAfficherCas)
        
        
    def retirerscenario(self):
        selection=self.listecas.curselection()
        if selection:
            self.item = self.listecas.curselection()
            self.CAS = self.listecas.get(self.item, self.item)
            self.parent.deleteTitreBD()
            self.listecas.delete(self.item, self.item)
        else:
            messagebox.showinfo("Action impossible", "Veuillez choisir un cas")
        
    def retirerCasUserMachine(self):
        self.parent.deleteCasUserMachine()
        self.changecadre(self.cadrescenario)
        
    def ajoutertitre(self):
        self.changecadre(self.cadreAjouterTitre)
        
    def ajoutercas(self):
        self.parent.ajouterTitreBD()
        self.changecadre(self.cadreAjouterCas)
        
        
        
    def ajoutercasordi(self):
        self.leCas= self.casInsertion.get()
        self.parent.ajouterCasOrdiBD(self.leCas)
        self.casInsertion.delete(0, 5000)
        
        
    def ajoutercasusager(self):
        self.leCas= self.casInsertion.get()
        self.parent.ajouterCasUsagerBD(self.leCas)
        self.casInsertion.delete(0, 5000)
        
    def ajouterCasOrdiMenu(self):
        self.parent.ajouterCasOrdiMENU()
        self.entreeMachine.delete(0,END)
        self.changecadre(self.cadrescenario)
        
    def ajouterCasUsagerMenu(self):
        self.parent.ajouterCasUsagerMENU()
        self.entreeUser.delete(0,END)
        self.changecadre(self.cadrescenario)
        
    def termine(self):
        self.position =0
        self.titrecourant=""
        
        rep=self.parent.afficherLesCas()
        self.listecas.delete(0, 100)
        for n in rep:
            self.listecas.insert(END, n[0])
            
        self.changecadre(self.cadrescenario)
        
    def retourCasUserMachine(self):
        
        self.changecadre(self.cadreAfficherCas)

    
    def modifierTitre(self):
        self.titrecourant=self.entreeTitre.get()
        self.parent.modifierTitre(self.titreafficher, self.titrecourant)
        self.titreafficher=self.titrecourant
        
    def modifierscenario(self):
        self.titreafficher=self.entreeTitre.get()
        if (self.listeOrdinateur.curselection()):
            self.selectionOrdi= self.listeOrdinateur.get(self.listeOrdinateur.curselection(),self.listeOrdinateur.curselection())
            self.descAfficher=self.selectionOrdi[0]
            
        if(self.listeUsager.curselection()):
            self.selectionUser= self.listeUsager.get(self.listeUsager.curselection(),self.listeUsager.curselection())
            self.descAfficher=self.selectionUser[0]
            
        
        rep= self.parent.afficherOrdre(self.descAfficher,self.titreafficher)
        self.ordreAfficher=rep[0][0]
            
        if(self.compteurcreerCadre==0):
            self.creercadresModifierCas()
            self.compteurcreerCadre=1
        else:
            rep=self.parent.descriptionAfficher(self.descAfficher)
            self.descAfficher=rep[0][0]
            
            self.entreeDescription.delete(0, 5000)
            self.entreeDescription.insert(0,str(self.descAfficher))
            self.entreeOrdre.delete(0, 5000)
            self.entreeOrdre.insert(0,str(self.ordreAfficher))
            
        self.changecadre(self.cadreModifierCas)
    
    def afficherscenario(self):
        if self.listecas.curselection():
            self.selection = self.listecas.get(self.listecas.curselection())
            self.titreafficher=self.selection
            self.titreafficher= self.selection
            self.entreeTitre.delete(0,5000)
            self.entreeTitre.insert(0,self.titreafficher)
            
            repMachine= self.parent.afficherInteractionMachine(self.titreafficher)
            repUser=self.parent.afficherInteractionUser(self.titreafficher)            
            self.nbCas=0
            for i in repMachine:
                self.nbCas+=1
            for i in repUser:
                self.nbCas+=1
                
            self.listeOrdinateur.delete(0,END)
            self.listeUsager.delete(0,END)
            
            if repMachine!="Vide":
                for i in range(self.nbCas):
                    self.cheval=False
                    for t in repMachine:
                        if (t[1]==i+1):
                            self.cheval=True
                            self.Inserer=t[0]
                    if(self.cheval): 
                        self.listeOrdinateur.insert(END,str(self.Inserer))  
                    else:
                        self.listeOrdinateur.insert(END,"")
                         
            if repUser!="Vide":
                for i in range(self.nbCas):
                    self.cheval=False
                    for t in repUser:
                        if (t[1]==i+1):
                            self.cheval=True
                            self.Inserer=t[0]
                    if(self.cheval):
                        self.listeUsager.insert(END,str(self.Inserer))  
                    else:
                        self.listeUsager.insert(END,"")
                        
                        
            self.changecadre(self.cadreAfficherCas)
        else:
            messagebox.showinfo("Action impossible", "Veuillez choisir un cas")
            
    def modifierDescription(self):
        self.vieuxTitre=self.descAfficher
        self.nouveauTitre=self.entreeDescription.get()
        self.parent.modifierDescription(self.vieuxTitre, self.nouveauTitre, self.titreafficher)
        self.titreAfficher=self.nouveauTitre
        self.changecadre(self.cadrescenario)
        
    def modifierOrdre(self):
        self.vieuxOrdre=self.ordreAfficher
        self.nouvelOrdre=int(self.entreeOrdre.get())
        self.parent.modifierOrdre(self.vieuxOrdre, self.nouvelOrdre, self.titreafficher)
        self.ordreAfficher=self.nouvelOrdre
        self.changecadre(self.cadrescenario)
        
    def fermerfenetre(self):
        self.root.destroy()
        
    def suivant(self):
        self.parent.requeteModules("crc")
        
    