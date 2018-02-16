# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
from PIL.FontFile import WIDTH
from tkinter.ttk import Combobox
from tkinter.constants import LEFT
import datetime
from tkinter import messagebox
#import dateutil.parser

class Vue():
    def __init__(self,parent, modele, org, largeur=800,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=modele
        self.dateJour=datetime.datetime.today().date()
        self.couleurBG="white"
        self.chVarTri=BooleanVar()
        self.Statut=None
        self.Employe=None
        self.Org=org
        self.listeVarStatut=["Actif","Inactif"]
        self.listeVarProjet=[]
        self.listeNoEmploye=["50168","1156","1154","1153"]
        self.listeVarEmploye=[]
        self.index=None
        self.idProjet=None
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.chargerEmploye()
        self.chargerProjet()
        self.chargerStatut()
        self.creercadres()
        self.changecadre(self.frameProjet)
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
        self.CreerCadreProjet()
        self.afficherModules()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def CreerCadreProjet(self):
        #cadre principal projet
        self.frameProjet=Frame(self.root,bg="green")
        #cadre gauche
        self.frameGauche=Frame(self.frameProjet,width=200,height=600,bg=self.couleurBG)
        self.frameGauche.pack_propagate(FALSE)
        self.frameGauche.pack(side=LEFT)
        self.frameListeProjet=LabelFrame(self.frameGauche,text="Liste projet",bg=self.couleurBG)
        self.frameListeProjet.pack(fill=BOTH,expand=1)
        self.listeProjet=Listbox(self.frameListeProjet,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        self.listeProjet.bind('<<ListboxSelect>>', self.changementProjet)
        self.listeProjet.pack(fill=BOTH,expand=1)
        self.chboxTri=Checkbutton(self.frameGauche,text="Afficherinactif",variable=self.chVarTri,onvalue=1,offvalue=0,height=1,width=40,pady=10,bg=self.couleurBG,command=self.Tri)
        self.chboxTri.pack()
        self.btnAnnuler=Button(self.frameGauche,text="Annuler",command=self.Annuler)
        self.btnAnnuler.pack(side=BOTTOM)
        #charger liste
        self.Tri()
        #cadre droit
        self.frameDroit=Frame(self.frameProjet,width=400,height=600,bg=self.couleurBG)
        self.frameDroit.pack_propagate(FALSE)
        self.frameDroit.pack(side=LEFT)
        
        #ligne 1
        self.frameLigne1=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne1.pack(fill=X,expand=1)
        self.frameStatut=LabelFrame(self.frameLigne1,text="Statut du projet:",bg=self.couleurBG)
        self.frameStatut.pack(side=LEFT,fill=X,expand=1)
        self.listeStatut=Combobox(self.frameStatut,text="Statut du projet: ",textvariable=self.Statut,values=self.listeVarStatut,state='readonly')
        self.listeStatut.bind('<<ComboboxSelected>>', self.changementStatut)
        self.listeStatut.pack(fill=X)
        #self.listeStatut.set(self.listeVarStatut[0])
        self.btnEnregistrer=Button(self.frameLigne1,command=self.Enregistrer)
        self.btnEnregistrer.pack(side=LEFT)
        self.setEnregistrer()
        
        #ligne2
        self.frameLigne2=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne2.pack(fill=X,expand=1)
        self.frameNomProjet=LabelFrame(self.frameLigne2,width=200,text="Nom du projet",bg=self.couleurBG)
        self.frameNomProjet.pack(side=LEFT,fill=X,expand=1)
        self.txtNomProjet=Entry(self.frameNomProjet)
        self.txtNomProjet.pack(fill=X)
        self.frameDtCreation=LabelFrame(self.frameLigne2,text="Date création",bg=self.couleurBG)
        self.frameDtCreation.pack(side=LEFT)
        self.txtDtCreation=Entry(self.frameDtCreation)
        self.txtDtCreation.pack()
        self.txtDtCreation.bind('<KeyRelease>', self.dtCheck)
        #ligne 3
        self.frameLigne3=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne3.pack(fill=X,expand=1)
        self.frameEmploye=LabelFrame(self.frameLigne3,text="Liste employé",bg=self.couleurBG)
        self.frameEmploye.pack(side=LEFT,fill=X,expand=1)
        self.listeEmploye=Combobox(self.frameEmploye,text="Responsable: ",textvariable=self.Employe,values=self.listeVarEmploye,state='readonly')
        self.listeEmploye.bind('<<ComboboxSelected>>', self.changementEmploye)
        self.listeEmploye.pack(fill=X)
        self.frameDtSuivi=LabelFrame(self.frameLigne3,text="Date de suivi",bg=self.couleurBG)
        self.frameDtSuivi.pack(side=LEFT,fill=X)
        self.txtDtSuivi=Entry(self.frameDtSuivi)
        self.txtDtSuivi.pack(fill=X)
        self.txtDtSuivi.bind('<KeyRelease>', self.dtCheck)
        #ligne 4
        self.frameLigne4=LabelFrame(self.frameDroit,text="Commentaire",width=400,height=100,bg=self.couleurBG)
        self.frameLigne4.pack(fill=X,expand=1)
        self.txtCommentaire=Text(self.frameLigne4)
        self.txtCommentaire.pack()
        #ligne 5
        self.frameLigne5=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne5.pack(fill=X,expand=1)
        self.btnSuivant=Button(self.frameLigne5,text="Suivant",command=self.suivant)
        self.btnSuivant.pack(side=RIGHT)
        self.initChamp()
        
    def afficherModules(self):
        self.cadreModules=Frame(self.root)
        self.cadremodule=Frame(self.cadreModules)
        self.canevaModules=Canvas(self.cadremodule,width=640,height=480,bg=self.couleurBG)
        self.canevaModules.pack(side=LEFT)
        
        self.listemodules=Listbox(self.cadremodule,bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        self.ipcentral=Entry(self.cadremodule, bg="pink")
        #self.ipcentral.insert(0, self.monip)
        btnconnecter=Button(self.cadremodule, text="Choisir un module",bg="lightgray",command=self.choisirModule)
        self.canevaModules.create_window(200,100,window=self.listemodules)
        self.canevaModules.create_window(200,450,window=btnconnecter,width=100,height=30)
        self.cadremodule.pack(side=LEFT)
    
    def requeteModule(self):
        self.parent.chargerModules();
     
    def dtValidateur(self,champDt):
        try:
            date=datetime.datetime.strptime(champDt.get(),"%Y/%m/%d").date()
            #if (date>self.dateJour):
                #print("date trop grand")
        except:
            #print("Format de date non valide")
            return False
        return True
        
    
    def effaceDernier(self,btn,date):
        btn.delete(0,END)
        date=date[:-1]
        btn.insert(0,date)
    
    def dtCheck(self,Event):
        self.date=Event.widget.get()
        longueur=len(self.date)
        if(longueur !=0):
            if (not self.date[longueur-1] in '0123456789'):
                #efface dernier carac non valide
                self.effaceDernier(Event.widget,self.date)
                longueur-=1
            #ajout automatique / pour faire date format aaaa/mm/dd
            if (longueur==4 or longueur==7):
                self.date+="/"
                Event.widget.insert(longueur,"/")
            #si trop long enlève dernier caractère
            elif(longueur>10):
                self.effaceDernier(Event.widget,self.date)
        
    def chargerStatut(self):
        pass
    
    def chargerProjet(self):
        rep=self.parent.requeteSelect('''SELECT * FROM Projet''')
        for n in rep:
            if n:
                self.listeVarProjet.append(n)
        
    def chargerEmploye(self):
        listeEmp = self.parent.retournerListe("select nom FROM clients Where organisation= '" + self.Org+"'", "usagers.smid")

        for emp in listeEmp:
            chaine=emp[0]
            self.listeVarEmploye.append(chaine);
       
    def suivant(self):
        #print("suivant")
        if(self.idProjet !=None):
            self.changecadre(self.cadreModules)
            self.requeteModule()
        else:
           #print("Vous devez choisir un projet") 
           messagebox.showinfo("Impossible d'Effectuer cette action", "Vous devez choisir un projet!")
    
    def changementEmploye(self,event):
        pass
        #print("changement employe")
    
    def Enregistrer(self):
        enregistrer=1
        if(self.txtDtCreation.get()!="" and self.dtValidateur(self.txtDtCreation)==0):
            messagebox.showinfo("Impossible d'Effectuer cette action", "Date de création on valide!")
            enregistrer=0
        if(self.txtDtSuivi.get()!="" and self.dtValidateur(self.txtDtSuivi)==0):
            messagebox.showinfo("Impossible d'Effectuer cette action", "Date de suivi on valide!")
            enregistrer=0
        projet=self.txtNomProjet.get()
        if(projet==""):
            enregistrer=0
            messagebox.showinfo("Impossible d'Effectuer cette action", "Il faut entrer au moins un nom de projet!")
		
        if(enregistrer==1):
            commentaire=self.txtCommentaire.get("0.0",END)
            dtSuivi=self.txtDtSuivi.get()
            dtCreation=self.txtDtCreation.get()
            employe=self.listeEmploye.get()
            statut=self.listeStatut.get()
            
            if(self.idProjet):
               # print("sélection "+str(self.listeProjet.curselection()))
                #print("sélection "+str(self.listeProjet.curselection()[0]))
                #current=self.listeProjet.curselection()[0]
                #modifie dans la liste locale
                #index=self.trouverIndex(current)
                listTemp=list(self.listeVarProjet[self.index])
                listTemp[1]=projet
                listTemp[2]=dtCreation
                listTemp[6]=dtSuivi
                listTemp[3]=employe
                listTemp[5]=commentaire
                listTemp[4]=statut
                self.listeVarProjet[self.index]=listTemp
                #modifie sql
                sql="Update Projet SET nom='"+projet+"',dtCreation="+dtCreation+",responsable='"+employe+"',statut='"+statut+"',commentaire='"+commentaire+"',dtSuivi='"+dtSuivi+"' WHERE id="+str(self.idProjet)
                #print("update "+sql)
                self.parent.modificationProjet(sql)
            else:
                #print("Nouvel enregistrement")
                #ajout sql
                #list=[projet,dtCreation,employe,statut,commentaire,dtSuivi]
                sql="INSERT INTO Projet (nom,dtCreation,responsable,statut,commentaire,dtSuivi) VALUES ('"+projet+"','"+dtCreation+"','"+employe+"','"+statut+"','"+commentaire+"','"+dtSuivi+"')"
                #print("sql "+sql)
                self.idProjet=self.parent.ajoutProjet(sql)
                #ajout liste locale et reéaffiche
                self.listeVarProjet.append((self.idProjet,projet,dtCreation,employe,statut,commentaire,dtSuivi))
            self.Tri()
            
    def setEnregistrer(self):
        if(self.idProjet):
            self.btnEnregistrer.config(text="Modifier enregistrement")
        else:
            self.btnEnregistrer.config(text="Nouvel enregistrement")
    
    def changementStatut(self,Event):
        pass
        #print("changement statut")

    def changementProjet(self,Event):
        #print("changement projet")
        if(self.listeProjet.curselection()):
            self.effaceChamp()
            current=self.listeProjet.curselection()[0]
            self.index=self.trouverIndex(current)
            self.idProjet=self.listeVarProjet[self.index][0]
            #print(self.idProjet)
            #remplissage des champ
            self.txtNomProjet.insert(0,self.listeVarProjet[self.index][1])
            self.txtDtCreation.insert(0, self.listeVarProjet[self.index][2])
            self.txtDtSuivi.insert(0, self.listeVarProjet[self.index][6])
            self.listeEmploye.set(self.listeVarProjet[self.index][3])
            self.txtCommentaire.insert(0.0,self.listeVarProjet[self.index][5])
            self.listeStatut.set(self.listeVarProjet[self.index][4])
        else:
            self.idProjet=None
        self.setEnregistrer()
        
    def trouverIndex(self,current):
        index=0
        for n in self.listeVarProjet:
            if (n[1]==self.listeProjet.get(current)):
                #print("index "+str(index))
                return index
            else:
                index+=1
        
    def Annuler(self):
        #print("Je veux annuler")
        self.listeProjet.selection_clear(0,self.listeProjet.size())
        self.initChamp()
    
    def effaceChamp(self):
        self.listeEmploye.set('')
        #champ texte à vide
        self.txtCommentaire.delete(0.0, END)
        self.txtDtCreation.delete(0,END)
        self.txtDtSuivi.delete(0,END)
        self.txtNomProjet.delete(0,END)
       
    
    def initChamp(self):
        self.effaceChamp()
        self.changementProjet(0)
        self.listeStatut.set(self.listeVarStatut[0])
        self.txtDtCreation.insert(0,"%s/%s/%s" % (str(self.dateJour.year).zfill(2),str(self.dateJour.month).zfill(2),str(self.dateJour.day).zfill(2)))
        
    def Tri(self):
        self.listeProjet.delete(0, self.listeProjet.size())
        if (self.chVarTri.get()==0):
            #print("affichage actif")
            for n in self.listeVarProjet:
                if (n[4]=="Actif"):
                    self.listeProjet.insert(END,n[1])
        else:
            #print("affichage inactif")
            for n in self.listeVarProjet:
                pass
                if (n[4]=="Inactif"):
                    self.listeProjet.insert(END,n[1])
                
    def chargerModules(self,repmodules):
        for i in repmodules:
            self.listemodules.insert(END,i)
      
    def choisirModule(self):
        mod=self.listemodules.selection_get()
        if mod:
            self.parent.requeteModules(mod)
            
    def salutations(self):
        pass
        #print("HOURRA SA MARCHE")
        
    def fermerfenetre(self):
        self.root.destroy()
    