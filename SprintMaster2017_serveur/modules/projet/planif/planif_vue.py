# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from IdMaker import *
from PIL import Image,ImageDraw, ImageTk
from tkinter import messagebox
import os,os.path
import math
from helper import Helper as hlp

class Vue():
    def __init__(self,parent,usager, org, idProjet, largeur=800,Urgentur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=None
        self.largeur=largeur
        self.Urgentur=Urgentur
        self.images={}
        self.respo=[]
        #self.treeValues=[]
        #self.tree = ttk.Treeview(self.root)
        self.cadreactif=None
        self.nomUser=usager
        self.nomOrg=org
        self.nomBD = "Projet.smid"
        self.idProjet = idProjet
        self.creercadres()
        self.changecadre(self.cadreEdition)
        self.id = Id()
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
    
     
    def ajoutRespo(self, idCrc, nom, prio, sprint, temps):
        self.parent.ajoutRespo(idCrc, nom, prio, sprint, temps)
       
    def remplirBox(self):
        #self.parent.requeteSQL("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "Créer Interface" + "','" + "24" + "','"+ "2"+ "','" + "1" + "','" + "Urgent"+ "','" + self.idProjet + "')", self.nomBD, self.nomUser)
        #self.parent.requeteSQL("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+"Construire Justin Dugas" + "','" + "24" + "','" +"2"+ "','" + "3" + "','" + "Moyen"+ "','" + self.idProjet + "')", self.nomBD, self.nomUser)
        #self.parent.requeteSQL("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "Appeller la Police" + "','" + "24" + "','" +"2"+ "','" + "3" + "','" + "Bas"+ "','" + self.idProjet + "')", self.nomBD, self.nomUser)
        #self.parent.requeteSQL("INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ "Quitter le Pays" + "','" + "24" + "','" +"2"+ "','" + "4" + "','" + "Moyen"+ "','" + self.idProjet + "')", self.nomBD, self.nomUser)

        listeRespo = self.parent.retournerListe("select idCrc, nom, previsionHre, sprintVise, priorite FROM Responsabilite WHERE idProjet = "+self.idProjet+" ORDER BY sprintVise ", "Projet.smid")
        if (listeRespo != "Vide"):
            for respo in listeRespo:
                idCrc=respo[0]
                nom=respo[1]
                temps=respo[2]
                sprint=respo[3]
                prio=respo[4]
                self.ajoutRespo(idCrc, nom, prio, sprint, temps)
    
    def creercadres(self):
        self.creerPageEdition()
                
    def creerPageEdition(self):
        self.cadreEdition=Frame(self.root)
        self.canevaEdition=Canvas(self.cadreEdition,width=600,height=600,bg="white")
        self.canevaEdition.pack()
        
        self.titreTexte = "Organisation: " + self.nomOrg + "     Usager: " + self.nomUser + "     Projet: " + "A MODIFIER"
        self.labelTitre=Label(text=self.titreTexte)
        
        self.remplirBox()
        
        #Treeview
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"]=("Priorité","Temps", "Sprint")
        self.tree.column("Priorité", width=100, anchor="c" )
        self.tree.column("Temps", width=100, anchor="c")
        self.tree.column("Sprint", width=100, anchor="c")
        
        self.tree.heading("Priorité", text="Priorité")
        self.tree.heading("Temps", text="Temps")
        self.tree.heading("Sprint", text="Sprint")
        
        self.treeValues=[]
        self.treeValues.append(self.tree.insert("","end", text="Tâches supplémentaires", values=("","", ""))) 
        
        listeRespo = self.parent.retournerListe("select idCrc, nom, previsionHre, sprintVise, priorite FROM Responsabilite WHERE idProjet = "+self.idProjet+" ORDER BY sprintVise ", "Projet.smid")
        if (listeRespo != "Vide"):
            sprintMax = self.parent.modele.respo[len(self.parent.modele.respo)-1].sprint
        else:
            sprintMax = 0
        
        compteur=1
        while(compteur<=sprintMax):
             for item in self.parent.modele.respo:                
                if(item.sprint==compteur):
                     if(item.idCrc==9999 and item.prio=="Urgent"):
                         self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=item.nom, values=(item.prio,item.temps, item.sprint)))
                     if (item.prio == "Urgent" and item.idCrc!=9999):
                         self.treeValues.append(self.tree.insert("", "end", text=item.nom, values=(item.prio,item.temps, item.sprint))) 
             for item in self.parent.modele.respo:
                 if(item.sprint==compteur):
                     if(item.idCrc==9999 and item.prio=="Moyen"):
                         self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=item.nom, values=(item.prio,item.temps, item.sprint)))
                     if (item.prio == "Moyen" and item.idCrc!=9999):
                         self.treeValues.append(self.tree.insert("", "end", text=item.nom, values=(item.prio,item.temps, item.sprint))) 
             for item in self.parent.modele.respo:
                 if(item.sprint==compteur):
                     if(item.idCrc==9999 and item.prio=="Bas"):
                         self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=item.nom, values=(item.prio,item.temps, item.sprint)))
                     if (item.prio == "Bas" and item.idCrc!=9999):
                         self.treeValues.append(self.tree.insert("", "end", text=item.nom, values=(item.prio,item.temps, item.sprint))) 
             compteur+=1    
                 
        self.canevaEdition.create_window(300,190, window=self.tree, width=580, height = 150)
        
        #Temps
        self.lblTemps = Label(text="Temps de réalisation: ")
        self.entryTemps = Entry(bg="white")
        self.canevaEdition.create_window(230, 320, window=self.lblTemps, width=200, height = 30)
        self.canevaEdition.create_window(390, 320, window=self.entryTemps, width=40, height = 30)
        
        #Sprint
        self.lblSprint = Label(text="Numéro du sprint: ")
        self.entrySprint = Entry(bg="white")
        self.canevaEdition.create_window(230, 360, window=self.lblSprint, width=200, height = 30)
        self.canevaEdition.create_window(390, 360, window=self.entrySprint, width=40, height = 30)

        #Priorite
        self.lblPrio = Label(text="Priorité: ")
        self.entryPrio = Entry(bg="white")
        self.canevaEdition.create_window(230, 400, window=self.lblPrio, width=200, height = 30)
        self.canevaEdition.create_window(390, 400, window=self.entryPrio, width=40, height = 30)
        
        btnSauvegarde=Button(text="Valider Modifs",bg="lightgray",command=self.sauvegarder)
        self.canevaEdition.create_window(300,450,window=btnSauvegarde,width=120,height=30)
        
        #Autres tâches
        self.lblTache = Label(text="Nouvelle tâche: ")
        self.entryTache = Entry(bg="white")
        self.canevaEdition.create_window(170, 500, window=self.lblTache, width=100, height = 30)
        self.canevaEdition.create_window(340, 500, window=self.entryTache, width=200, height = 30)
        
        
        btnSoumettre=Button(text="Soumettre la tâche",bg="lightgray",command=self.nouvTache)
        self.canevaEdition.create_window(300,540,window=btnSoumettre,width=120,height=30)
        
        self.canevaEdition.create_window(300,30,window=self.labelTitre,width=400,height=30)
    
    def sauvegarder(self):
        if(self.entryTemps.get()!="" and self.entrySprint.get()!="" and self.entryPrio.get()!=""):
            if(self.entryPrio.get()=="Urgent" or self.entryPrio.get()=="Moyen" or self.entryPrio.get()=="Bas"):
                if(int(self.entryTemps.get())>0 and int(self.entrySprint.get())>0 and int(self.entryTemps.get())<=200 and int(self.entrySprint.get())<=20):
                    curItem = self.tree.focus()
                    respo = self.tree.item(curItem)['text']
            
                    compteur=0
                    indDelete=None
                    for item in self.treeValues:
                        if(item==curItem):
                            indDelete=compteur
                        compteur+=1
                        
                    if(indDelete!=None):
                        self.tree.delete(self.treeValues[indDelete])
                        self.tree.insert("", "end", respo, text = respo, values=(self.entryPrio.get(),self.entryTemps.get(), self.entrySprint.get()))
                        requete = "UPDATE Responsabilite SET previsionHre = '"+self.entryTemps.get()+"', priorite = '"+self.entryPrio.get()+"', sprintVise = '"+self.entrySprint.get()+"' WHERE nom = '"+respo+"'"
                        self.parent.requeteSQL(requete, self.nomBD, self.nomUser)
                    else:
                        messagebox.showinfo("Erreur", "Veuillez sélectionner une responsabilité")
                else:
                    messagebox.showinfo("Erreur", "Le sprint doit être entre 0 et 20. Le temps doit être entre 0 et 200")
            else:
                messagebox.showinfo("Erreur", "Les valeurs adéquates pour la priorité sont Urgent, Moyen ou Bas")
                self.entryPrio.insert(0, "")
        else:
            messagebox.showinfo("Erreur", "Veuillez entrer des valeurs adéquates")
        
    def nouvTache(self):
        if(self.entryTache.get()!="" and self.entryTemps.get()!="" and self.entrySprint.get()!="" and self.entryPrio.get()!=""):
            if(self.entryPrio.get()=="Urgent" or self.entryPrio.get()=="Moyen" or self.entryPrio.get()=="Bas"):
                if(int(self.entryTemps.get())>0 and int(self.entrySprint.get())>0 and int(self.entryTemps.get())<=200 and int(self.entrySprint.get())<=20):
                    if(self.entryPrio.get()=="Urgent"):
                        self.treeValues.append(self.tree.insert(self.treeValues[0], 0, text=self.entryTache.get(), values=(self.entryPrio.get(),self.entryTemps.get(), self.entrySprint.get())))   
                    else:
                        self.treeValues.append(self.tree.insert(self.treeValues[0], "end", text=self.entryTache.get(), values=(self.entryPrio.get(),self.entryTemps.get(), self.entrySprint.get())))   
                    requete = "INSERT INTO Responsabilite(nom, idCrc, previsionHre, sprintVise, priorite, idProjet) values ('"+ self.entryTache.get() + "','" + "9999" + "','"+ self.entryTemps.get() + "','" + self.entrySprint.get() + "','" + self.entryPrio.get()+ "','" + self.idProjet + "')"
                    self.entryPrio.insert(0, "")
                    self.parent.requeteSQL(requete, self.nomBD, self.nomUser)
                else:
                    messagebox.showinfo("Erreur", "Le sprint doit être entre 0 et 20. Le temps doit être entre 0 et 200")
            else:
                messagebox.showinfo("Erreur", "Les valeurs adéquates pour la priorité sont Urgent, Moyen ou Bas")
        else:
            messagebox.showinfo("Erreur", "Veuillez entrer des valeurs adéquates")
           
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    