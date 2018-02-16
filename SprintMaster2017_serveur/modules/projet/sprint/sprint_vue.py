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
from tkinter import messagebox
#import dateutil.parser

class Vue():
    def __init__(self,parent,modele,largeur=800,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=modele
        self.dateJour=datetime.datetime.today().date()
        self.couleurBG="white"
        self.chVarTri=BooleanVar()
        self.chVarFini=BooleanVar()
        self.dTimer=None
        self.fTimer=None
        self.idTache=None
        self.idSousTache=None
        self.index=None
        self.responsable=None
        self.treeValues=[]         
        self.listeVarResponsable=[]
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.frameSprint)
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
        self.CreerCadreSprint()
        self.afficherModules()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def CreerCadreSprint(self):
        #cadre principal projet
        self.frameSprint=Frame(self.root,bg="green")
        #cadre gauche
        self.frameGauche=LabelFrame(self.frameSprint,text="Liste planification globale",width=800,height=200,bg=self.couleurBG)
        self.frameGauche.pack_propagate(FALSE)
        self.frameGauche.pack()
        ##self.frameGauche.pack(side=LEFT)
        #self.frameListePlanif=LabelFrame(self.frameGauche,text="Liste taches globales",bg=self.couleurBG)
        #self.frameListePlanif.pack(fill=BOTH,expand=1)
        ##arbre
        #self.canevaEdition=Canvas(self.frameGauche,bg=self.couleurBG)
        #self.canevaEdition.pack(fill=BOTH,expand=1)
        self.tree = ttk.Treeview(self.frameGauche)
        self.tree["columns"]=("Priorité","Temps", "Sprint")
        self.tree.column("Priorité", width=100, anchor="c" )
        self.tree.column("Temps", width=100, anchor="c")
        self.tree.column("Sprint", width=100, anchor="c")
        
        self.tree.heading("Priorité", text="Priorité")
        self.tree.heading("Temps", text="Temps")
        self.tree.heading("Sprint", text="Sprint")
        
        #self.treeValues.append(self.tree.insert("","end", text="Tâches supplémentaires", values=("","", "")))
        self.tree.pack(fill=BOTH,expand=1)
        self.tree.bind('<ButtonRelease-1>', self.changementTache)
        self.remplirArbre()
        #self.canevaEdition.create_window(0,0, window=self.tree, width=800, height = 150)
        #fin arbre
        #self.listeTache=Listbox(self.frameListePlanif,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=40,height=6)
        #self.listeTache.bind('<<ListboxSelect>>', self.changementTache)
        #self.listeTache.pack(fill=BOTH,expand=1)
        #self.chboxTri=Checkbutton(self.frameGauche,text="Afficherinactif",variable=self.chVarTri,onvalue=1,offvalue=0,height=1,width=40,pady=10,bg=self.couleurBG,command=self.Tri)
        #self.chboxTri.pack()
        
        #charger liste
        self.Tri()
        #cadre droit
        self.frameDroit=Frame(self.frameSprint,width=800,height=500,bg=self.couleurBG)
        self.frameDroit.pack_propagate(FALSE)
        self.frameDroit.pack()
        #self.frameDroit.pack(side=LEFT)
        self.btnAnnuler=Button(self.frameDroit,text="Annuler",command=self.Annuler)
        self.btnAnnuler.pack()
        
        #ligne 1
        self.frameLigne1=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne1.pack(fill=X,expand=1)
        self.chboxFini=Checkbutton(self.frameLigne1,text="Complété",variable=self.chVarFini,onvalue=1,offvalue=0,bg=self.couleurBG,command=self.dtComplet)
        self.chboxFini.pack(side=LEFT)
        self.frameDateFini=LabelFrame(self.frameLigne1,text="Date complétée",bg=self.couleurBG)
        self.frameDateFini.pack(side=LEFT)
        self.txtDateFini=Entry(self.frameDateFini)
        self.txtDateFini.pack(fill=X)
        self.txtDateFini.bind('<KeyRelease>', self.dtCheck)
        self.btnDtComplete=Button(self.frameLigne1,text="Maintenant",command=self.inscrireDateComplete)
        self.btnDtComplete.pack(side=LEFT)
        self.btnEnregistrer=Button(self.frameLigne1,text="Enregistrer",command=self.ajoutSousTache)
        self.btnEnregistrer.pack(side=LEFT)
        self.btnReset=Button(self.frameLigne1,text="Effacer champ",command=self.reset)
        self.btnReset.pack(side=LEFT)
        
        #ligne 4
        self.chargerEmploye()
        self.frameLigne4=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne4.pack(fill=X,expand=1)
        self.frameSousTache=LabelFrame(self.frameLigne4,text="Sous tache",bg=self.couleurBG)
        self.frameSousTache.pack(side=LEFT,fill=X,expand=1)
        self.txtSousTache=Entry(self.frameSousTache)
        self.txtSousTache.pack(fill=X)
        self.frameResponsable=LabelFrame(self.frameLigne4,text="Responsable du projet:",bg=self.couleurBG)
        self.frameResponsable.pack(side=LEFT,fill=X,expand=1)
        self.listeResponsable=Combobox(self.frameResponsable,text="Responsable: ",textvariable=self.responsable,values=self.listeVarResponsable,state='readonly')
        self.listeResponsable.bind('<<ComboboxSelected>>', self.changementResponsable)
        self.listeResponsable.pack(fill=X)
        
        
        #ligne 2
        self.frameLigne2=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne2.pack(fill=X,expand=1)
        self.frameDtPrevue=LabelFrame(self.frameLigne2,text="Date prévue",bg=self.couleurBG)
        self.frameDtPrevue.pack(side=LEFT,fill=X)
        self.txtDtPrevue=Entry(self.frameDtPrevue)
        self.txtDtPrevue.pack(fill=X)
        self.txtDtPrevue.bind('<KeyRelease>', self.dtCheck)
        self.btnDtPrevue=Button(self.frameLigne2,text="Maintenant",command=self.inscrireDatePrevue)
        self.btnDtPrevue.pack(side=LEFT)
        self.frameTempsPrevu=LabelFrame(self.frameLigne2,text="Temps prévu",bg=self.couleurBG)
        self.frameTempsPrevu.pack(side=LEFT,fill=X)
        self.txtTempsPrevu=Entry(self.frameTempsPrevu)
        self.txtTempsPrevu.pack(fill=X)
        
         #ligne 3
        self.frameLigne3=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne3.pack(fill=X,expand=1)
        self.frameDtReelle=LabelFrame(self.frameLigne3,text="Date réelle",bg=self.couleurBG)
        self.frameDtReelle.pack(side=LEFT,fill=X)
        self.txtDtReelle=Entry(self.frameDtReelle)
        self.txtDtReelle.pack(fill=X)
        self.txtDtReelle.bind('<KeyRelease>', self.dtCheck)
        self.btnDtReelle=Button(self.frameLigne3,text="Maintenant",command=self.inscrireDateReelle)
        self.btnDtReelle.pack(side=LEFT)
        self.frameTempsReel=LabelFrame(self.frameLigne3,text="Temps réel",bg=self.couleurBG)
        self.frameTempsReel.pack(side=LEFT,fill=X)
        self.txtTempsReel=Entry(self.frameTempsReel)
        self.txtTempsReel.pack(fill=X)
        self.frameOrdre=LabelFrame(self.frameLigne3,text="Ordre de priorité",bg=self.couleurBG)
        self.frameOrdre.pack(side=LEFT,fill=X)
        self.txtOrdre=Entry(self.frameOrdre)
        self.txtOrdre.pack(fill=X)
        
        #ligne timer
        self.frameTimer=LabelFrame(self.frameDroit,text="Calculateur de temps",bg=self.couleurBG)
        self.frameTimer.pack(fill=X,expand=1)
        self.frameTimer.pack()
        self.btnDebut=Button(self.frameTimer,text="Début",command=self.debutTimer)
        self.btnDebut.pack(side=LEFT)
        self.btnFin=Button(self.frameTimer,text="Arrêt",command=self.finTimer)
        self.btnFin.pack(side=LEFT)
        self.txtAjoutTemps=Entry(self.frameTimer)
        self.txtAjoutTemps.pack(side=LEFT)
        self.btnAjoutTemps=Button(self.frameTimer,text="Ajout temps",command=self.ajoutTemps)
        self.btnAjoutTemps.pack(side=LEFT)
        
        #ligne 4
        self.frameLigne4=LabelFrame(self.frameDroit,text="Liste sous tache",width=400,height=100,bg=self.couleurBG)
        self.frameLigne4.pack(fill=X,expand=1)
        self.listSousTache=Listbox(self.frameLigne4,bg=self.couleurBG,borderwidth=2,relief=FLAT,width=400,height=6)
        self.listSousTache.bind('<<ListboxSelect>>', self.changementSousTache)
        self.listSousTache.pack()
        
         #ligne 5
        self.frameLigne5=LabelFrame(self.frameDroit,text="Problème",width=400,height=100,bg=self.couleurBG)
        self.frameLigne5.pack(fill=X,expand=1)
        self.txtCommentaire=Text(self.frameLigne5)
        self.txtCommentaire.pack()
        
        #ligne 6
        self.frameLigne6=Frame(self.frameDroit,width=400,height=100,bg=self.couleurBG)
        self.frameLigne6.pack(fill=X,expand=1)
        self.btnSuivant=Button(self.frameLigne6,text="Suivant",command=self.suivant)
        self.btnSuivant.pack(side=RIGHT)
        
        self.initChamp()
    
    def remplirArbre(self):
        self.treeValues=[]
        self.treeValues.append(self.tree.insert("","end", text="Tâches supplémentaires", values=("","", ""))) 
        
        temp=len(self.parent.modele.planif)
        if(temp!=0):
            sprintMax = self.parent.modele.planif[temp-1].sprintVise
            compteur=1
            #print("sprintMax "+str(sprintMax))
            while(compteur<=sprintMax):
                for item in self.parent.modele.planif:
                    if(item.sprintVise==compteur):
                        if(item.idCrc==9999 and item.priorite=="Urgent"):
                            self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=item.nom, values=(item.priorite,item.previsionHre, item.sprintVise)))
                        if (item.priorite == "Urgent" and item.idCrc!=9999):
                            self.treeValues.append(self.tree.insert("", "end", text=item.nom, values=(item.priorite,item.previsionHre, item.sprintVise))) 
                for item in self.parent.modele.planif:
                     if(item.sprintVise==compteur):
                         #print(item.nom)
                         if(item.idCrc==9999 and item.priorite=="Moyen"):
                            self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=item.nom, values=(item.priorite,item.previsionHre, item.sprintVise)))
                         if (item.priorite == "Moyen" and item.idCrc!=9999):
                            self.treeValues.append(self.tree.insert("", "end", text=item.nom, values=(item.priorite,item.previsionHre, item.sprintVise))) 
                for item in self.parent.modele.planif:
                    if(item.sprintVise==compteur):
                        #print(item.nom)
                        if(item.idCrc==9999 and item.priorite=="Bas"):
                            self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=item.nom, values=(item.priorite,item.previsionHre, item.sprintVise)))
                        if (item.priorite == "Bas" and item.idCrc!=9999):
                            self.treeValues.append(self.tree.insert("", "end", text=item.nom, values=(item.priorite,item.previsionHre, item.sprintVise))) 
                compteur+=1
    
    def chargerEmploye(self):
        listeEmp = self.parent.retournerListe("select nom FROM clients Where organisation= '" + self.parent.nomOrg+"'", "usagers.smid")

        for emp in listeEmp:
            chaine=emp[0]
            self.listeVarResponsable.append(chaine);
    
    def inscrireDateComplete(self):
        #print("inscrireDateComplete")
        self.txtDateFini.delete(0,END)
        self.txtDateFini.insert(0,"%s/%s/%s" % (str(self.dateJour.year).zfill(2),str(self.dateJour.month).zfill(2),str(self.dateJour.day).zfill(2)))
        
    def inscrireDateReelle(self):
        #print("inscrireDateReelle")
        self.txtDtReelle.delete(0, END)
        self.txtDtReelle.insert(0,"%s/%s/%s" % (str(self.dateJour.year).zfill(2),str(self.dateJour.month).zfill(2),str(self.dateJour.day).zfill(2)))
        
    def inscrireDatePrevue(self):
        #print("inscrireDatePrevue")
        self.txtDtPrevue.delete(0,END)
        self.txtDtPrevue.insert(0,"%s/%s/%s" % (str(self.dateJour.year).zfill(2),str(self.dateJour.month).zfill(2),str(self.dateJour.day).zfill(2)))
       
    def dtValidateur(self,champDt):
        try:
            date=datetime.datetime.strptime(champDt.get(),"%Y/%m/%d").date()
            #if (date>self.dateJour):
                #print("date trop grand")
        except:
            #print("Format de date non valide")
            return False
        return True
         
    def setEnregistrer(self):
        #print("setEnregistrer")
        if(self.idSousTache!=None):
            self.btnEnregistrer.config(text="Modifier enregistrement")
        else:
            self.btnEnregistrer.config(text="Nouvel enregistrement")
            
    def effaceDernier(self,btn,date):
        btn.delete(0,END)
        date=date[:-1]
        btn.insert(0,date)
    
    def dtCheck(self,Event):
        date=Event.widget.get()
        longueur=len(date)
        if(longueur !=0):
            if (not date[longueur-1] in '0123456789'):
                #efface dernier carac non valide
                self.effaceDernier(Event.widget,date)
                longueur-=1
            #ajout automatique / pour faire date format aaaa/mm/dd
            if (longueur==4 or longueur==7):
                date+="/"
                Event.widget.insert(longueur,"/")
            #si trop long enlève dernier caractère
            elif(longueur>10):
                self.effaceDernier(Event.widget,date)
    
    def changementResponsable(self,event):
        pass
        #print("Responsable")
        
    def dtComplet(self):
        #print("complet"+str(self.chVarFini.get()))
        if(self.chVarFini.get()==1):
            self.inscrireDateComplete()
    
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
    
    def ajoutSousTache(self):
        if(self.idTache!=None):
            self.enregistrer()
        else:
            messagebox.showinfo("Impossible d'Effectuer cette action", "Aucune tache sélectionnée")
            
    def modification(self):
        pass
    
    def enregistrer(self):
        #print("ajout sous tache")
        ##set Variable
        nom=self.txtSousTache.get()
        if(nom==""):
            messagebox.showinfo("Impossible d'Effectuer cette action", "Il faut au moins une description de sous tâche!")
        else:
            dtFini=self.txtDateFini.get()
            if(dtFini==""):
                dtFini="None"
            dtPrevue=self.txtDtPrevue.get()
            if (dtPrevue==""):
                dtPrevue="None"
            dtRelle=self.txtDtReelle.get()
            #print("date reelle "+dtRelle)
            if(dtRelle==""):
                dtRelle="None"
            dtSousTache=self.txtSousTache.get()
            tempsPrevu=self.txtTempsPrevu.get()
            if (tempsPrevu==""):
                tempsPrevu="None"
            tempsReel=self.txtTempsReel.get()
            if (tempsReel==""):
                tempsReel="None"
            probleme=self.txtCommentaire.get(0.0,END)
            if(probleme==""):
                probleme="None"
            responsable=self.listeResponsable.get()
            if(responsable==""):
                responsable="None"
            ordre=self.txtOrdre.get()
            if(ordre==""):
                ordre=int(1)
            else:
                ordre=int(ordre)
            
            ##modif ou enregistre
            if(self.idSousTache!=None):
                if(ordre<1):
                    ordre=1
                elif(ordre>len(self.modele.planif[self.idTache].sousTache)):
                    ordre=len(self.modele.planif[self.idTache].sousTache)
                self.parent.modifSousTache(self.idTache,self.idSousTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
            else:
                if(ordre<1):
                    ordre=1
                elif(ordre>len(self.modele.planif[self.idTache].sousTache)+1):
                    ordre=len(self.modele.planif[self.idTache].sousTache)+1
                self.parent.ajoutSousTache(self.idTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
            self.chargementSousTache()
            self.listSousTache.select_set(ordre-1)
            self.changementSousTache(0)
                
        
    def ajoutTemps(self):
        if (self.txtAjoutTemps.get()==""):
            ajout=0
        else:
            ajout=int(self.txtAjoutTemps.get())
        if(self.txtTempsReel.get()==""):
            present=0
        else:
            present=int(self.txtTempsReel.get())
            
        reel=present+ajout
        self.txtTempsReel.delete(0, END)
        self.txtTempsReel.insert(0, reel)
        
    def debutTimer(self):
        #print("début timer")
        #print(datetime.datetime.now())
        self.dTimer=datetime.datetime.now()
    
    def finTimer(self):
        #print("fin timer")
        if(self.dTimer==None):
            self.dTimer=datetime.datetime.now()
            
        self.fTimer=datetime.datetime.now()
        #vide le champ
        self.txtAjoutTemps.delete(0, END)
        #nombre de minutes
        self.txtAjoutTemps.insert(0,(int((self.fTimer-self.dTimer).total_seconds())//60))
        #remet à zéro le timer
        self.dTimer=datetime.datetime.now()
    
    def requeteModule(self):
        self.parent.chargerModules();
    
    def changementSousTache(self,event):
        try:
            current=self.listSousTache.curselection()[0]
            self.idSousTache=self.parent.trouverIndexSous(current,self.idTache)
            self.chargementInfoSousTache()
            self.setEnregistrer()
        except:
            pass
            #print("Aucune sous tache")
        
    def chargementInfoSousTache(self):
        self.effaceChamp()
        info=self.modele.planif[self.idTache].sousTache[self.idSousTache]
        if(info.probleme!="None"):
            self.txtCommentaire.insert(0.0,info.probleme)
        if(info.dtComplete!="None"):
            self.txtDateFini.insert(0,info.dtComplete)
        if(info.responsable!="None"):
            self.listeResponsable.set(info.responsable)
        if(info.dtReel!="None"):   
            self.txtDtReelle.insert(0,info.dtReel)
        if(info.tempsPrevu!="None"):
            self.txtTempsPrevu.insert(0,info.tempsPrevu)
        if(info.dtPrevu!="None"):
            self.txtDtPrevue.insert(0,info.dtPrevu)
        if(info.tempsFait!="None"):
            self.txtTempsReel.insert(0,info.tempsFait)
        if(info.sousTache!="None"):
            self.txtSousTache.insert(0,info.sousTache)
        self.txtOrdre.insert(0, info.ordre)
    
    def changementTache(self,event):
        #print("Changement tache")
        try:
            curItem = self.tree.focus()
            current=self.tree.item(curItem).get("text")
            self.idTache=self.parent.trouverIndex(current)
            self.chargementSousTache()
            self.txtOrdre.insert(0, str(len(self.modele.planif[self.idTache].sousTache)+1))
        except:
            pass
    
    def chargementSousTache(self):
        self.listSousTache.delete(0, self.listSousTache.size())
        self.idSousTache=None
        self.effaceChamp()
        self.setEnregistrer()
        if(self.idTache!=None):
            for n in self.modele.planif[self.idTache].sousTache:
                #print(n)
                self.listSousTache.insert(END,n.sousTache)
        
    def suivant(self):
        #print("suivant")
        self.requeteModule()         
    
    def Annuler(self):
        #print("Je veux annuler")
        #self.listeProjet.selection_clear(0,self.listeProjet.size())
        self.idTache=None
        self.initChamp()

    def reset(self):
        try:
            self.effaceChamp()
            self.idSousTache=None
            self.setEnregistrer()
            self.txtOrdre.insert(0, str(len(self.modele.planif[self.idTache].sousTache)+1))
        except:
            pass
        
    def effaceChamp(self):
        #efface les champs textes
        self.txtAjoutTemps.delete(0,END)
        self.txtCommentaire.delete(0.0,END)
        self.txtDateFini.delete(0,END)
        self.txtDtPrevue.delete(0,END)
        self.txtDtReelle.delete(0,END)
        self.txtTempsPrevu.delete(0,END)
        self.txtSousTache.delete(0,END)
        self.txtTempsReel.delete(0,END)
        self.listeResponsable.set('')
        self.txtOrdre.delete(0,END)
        #self.listeEmploye.set('')
        #champ texte à vide
        #self.txtCommentaire.delete(0.0, END) lorsque champ text
        #self.txtDtCreation.delete(0,END) lorsque champ entry
        #self.txtDtSuivi.delete(0,END)
        #self.txtNomProjet.delete(0,END)
       
    def initChamp(self):
        self.effaceChamp()
        self.listSousTache.delete(0, self.listSousTache.size())
        self.idSousTache=None
        self.setEnregistrer()
        #self.changementProjet(0)
        #self.listeStatut.set(self.listeVarStatut[0])
        #self.txtDtCreation.insert(0,"%s/%s/%s" % (self.dateJour.year,self.dateJour.month,self.dateJour.day) )
        
    def Tri(self):
        pass
        #print("tri")
        #self.listeTache.delete(0, self.listeTache.size())
        #for n in self.modele.planif:
        #    self.listeTache.insert(END,n.nom)
#         self.listeProjet.delete(0, self.listeProjet.size())
#         if (self.chVarTri.get()==0):
#             print("affichage actif")
#             for n in self.listeVarProjet:
#                 if (n[4]=="Actif"):
#                     self.listeProjet.insert(END,n[1])    
#         else:
#             print("affichage inactif")
#             for n in self.listeVarProjet:
#                 pass
#                 if (n[4]=="Inactif"):
#                     self.listeProjet.insert(END,n[1])
                
    def chargerModules(self,repmodules):
        for i in repmodules:
            self.listemodules.insert(END,i)
      
    def choisirModule(self):
        mod=self.listemodules.selection_get()
        if mod:
            self.parent.requetemodule(mod)
            
    def salutations(self):
        pass
        #print("HOURRA SA MARCHE")
        
    def fermerfenetre(self):
        self.root.destroy()
        #print("ONFERME la fenetre")
    