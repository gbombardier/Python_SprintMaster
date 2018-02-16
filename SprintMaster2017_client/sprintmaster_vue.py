# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
import sqlite3
from helper import Helper as hlp

class Vue():
    def __init__(self,parent,monip,largeur=800,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.monip=monip
        self.parent=parent
        self.modele=None
        self.nom=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.modes={}
        self.modecourant=None
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.frameAcceuil)
        self.listeNom = ["Justin", "Gab","Danny" , "Ibrahim","Jean-Simon" ,"Camille"]
        self.listeOrg = ["CVM"]
        self.serveurBD=None
        
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
    
    def chargercentral(self,repmodules,repoutils):
        for i in repmodules:
            self.listemodules.insert(END,i)
        for i in repoutils:
            self.listeoutils.insert(END,i)
        self.changecadre(self.cadreModules)
           
    def creercadres(self):
        self.affichageAcceuil()
        #self.afficherCreerClient()
        #self.afficherCreerOrg()
        self.afficherModulesOutils()
                
    def affichageAcceuil(self):
        self.frameAcceuil=Frame(self.root)
        self.canevasAcceuil=Canvas(self.frameAcceuil,width=640,height=480,bg="white")
        self.canevasAcceuil.pack()
        
        self.imgLogin = ImageTk.PhotoImage(file = ".\login.png")
        self.canevasAcceuil.create_image(100,200, image = self.imgLogin, anchor= "nw")
        self.lblId=Label(text="Entrez un identifiant: ");
        self.champId=Entry(text = "Gab", bg="white")
        self.lblOrg=Label(text="Entrez une organisation: ");
        self.champOrg=Entry(text = "CVM", bg="white")
        self.champId.insert(0, "Gab")
        self.champOrg.insert(0, "CVM")
        
        btnconnecter=Button(text="Connexion",bg="lightgray",command=self.loginclient)
        self.balIp=tix.Balloon(self.frameAcceuil,state="balloon")
        self.balIp.bind_widget(btnconnecter,msg="identifiez vous et indiquez l'adresse du serveur")

        self.canevasAcceuil.create_window(225,200,window=self.lblOrg,width=160,height=30)
        self.canevasAcceuil.create_window(400,200,window=self.champOrg,width=150,height=30)
        self.canevasAcceuil.create_window(225,250,window=self.lblId,width=160,height=30)
        self.canevasAcceuil.create_window(400,250,window=self.champId,width=150,height=30)
        self.canevasAcceuil.create_window(310,400,window=btnconnecter,width=150,height=30)
        
    def afficherCreerClient(self):
        self.frameClient=Frame(self.root)
        self.canevasClient=Canvas(self.frameClient,width=640,height=480,bg="white")
        self.canevasClient.pack()
        
        lblTitre=Label(text="CRÉER EMPLOYÉ", bg="white")
        self.canevasClient.create_window(325,35,window=lblTitre,width=300,height=20)
        
        self.lblPasswd=Label(text="Entrez le mot de passe de votre organisation ");
        self.champPasswd=Entry(bg="white")
        self.canevasClient.create_window(225,200,window=self.lblPasswd,width=260,height=30)
        self.canevasClient.create_window(490,200,window=self.champPasswd,width=150,height=30)
        
        btnValider=Button(text="Valider",bg="lightgray",command=self.validerClient)
        self.canevasClient.create_window(310,400,window=btnValider,width=150,height=30)
        
        self.changecadre(self.frameClient)
        
    def validerClient(self):
        #Valider si le mot de passe est le bon
        if(self.champPasswd.get()=="a"):
            self.frameInfosClient=Frame(self.root)
            self.canevasInfosClient=Canvas(self.frameInfosClient,width=640,height=480,bg="white")
            self.canevasInfosClient.pack()
        
            lblTitre=Label(text="CRÉER EMPLOYÉ", bg="white")
            self.canevasInfosClient.create_window(325,35,window=lblTitre,width=300,height=20)
            
            lblInstruc=Label(text="Veuillez entrer les informations de l'employé", bg="white")
            self.canevasInfosClient.create_window(325,60,window=lblInstruc,width=300,height=20)
            
            self.lblID=Label(text="Identifiant: ");
            self.champID=Entry(bg="white")
            self.canevasInfosClient.create_window(225,100,window=self.lblID,width=80,height=30)
            self.canevasInfosClient.create_window(375,100,window=self.champID,width=150,height=30)
            
            self.lblNom=Label(text="Nom: ");
            self.champNomUsager=Entry(bg="white")
            self.canevasInfosClient.create_window(225,135,window=self.lblNom,width=80,height=30)
            self.canevasInfosClient.create_window(375,135,window=self.champNomUsager,width=150,height=30)
            self.champNomUsager.insert(0, self.champId.get())
            self.champNomUsager.config(state='disabled')
        
            self.lblTel=Label(text="Téléphone: ");
            self.champTel=Entry(bg="white")
            self.canevasInfosClient.create_window(225,175,window=self.lblTel,width=80,height=30)
            self.canevasInfosClient.create_window(375,175,window=self.champTel,width=150,height=30)
        
            self.lblAdr=Label(text="Adresse: ");
            self.champAdr=Entry(bg="white")
            self.canevasInfosClient.create_window(225,215,window=self.lblAdr,width=80,height=30)
            self.canevasInfosClient.create_window(375,215,window=self.champAdr,width=150,height=30)
        
            self.lblCourriel=Label(text="Courriel: ");
            self.champCourriel=Entry(bg="white")
            self.canevasInfosClient.create_window(225,255,window=self.lblCourriel,width=80,height=30)
            self.canevasInfosClient.create_window(375,255,window=self.champCourriel,width=150,height=30)

            self.lblRole=Label(text="Rôle: ");
            
            self.canevasInfosClient.create_window(225,320,window=self.lblRole,width=80,height=30)
            
            self.listeRole = Listbox(self.root)
            self.listeRole.insert(END, "Développeur")
            self.listeRole.insert(END, "Technicien")
            self.listeRole.insert(END, "Concierge")
            self.listeRole.insert(END, "Directeur")
            self.listeRole.insert(END, "Designer")
            
            self.canevasInfosClient.create_window(375,320,window=self.listeRole,width=150,height=70)
        
            self.lblStat=Label(text="Statut: ");
            self.canevasInfosClient.create_window(225,390,window=self.lblStat,width=80,height=30)
            
            self.v = StringVar()
            self.v.set("L")
            self.btn1 = Radiobutton(self.root, text="Actif", variable=self.v, value=1)
            self.btn2 = Radiobutton(self.root, text="Inactif", variable=self.v, value=2)
            
            self.canevasInfosClient.create_window(315,390,window=self.btn1,width=70,height=20)
            self.canevasInfosClient.create_window(405,390,window=self.btn2,width=70,height=20)
        
            btnValider=Button(text="Valider",bg="lightgray",command=self.inscrireClient)
            self.canevasInfosClient.create_window(310,440,window=btnValider,width=150,height=30)
        
            self.changecadre(self.frameInfosClient)
        else:
            messagebox.showinfo("Erreur", "Le mot de passe est incorrect. Veuillez recommencer ou contacter votre administrateur.")
            self.changecadre(self.frameClient)
            pass
        
    #Fonction qui inscrit le client dans la base de données
    def inscrireClient(self):
        if(self.v.get()=="1"):
            statut = "Actif"
        elif(self.v.get()=="2"):
            statut = "Inactif"
        else:
            statut = "Mauvais"
        

        if(self.champOrg.get()!="" and self.champID.get()!="" and self.champNomUsager.get()!="" and self.champTel.get()!="" and self.champAdr.get()!="" and self.champCourriel.get()!="" and statut!="Mauvais"):
            self.parent.requeteSQL("INSERT INTO clients (organisation, identifiant, nom, telephone, adresse, courriel, role, statut) VALUES ('"+self.champOrg.get()+"','"+self.champID.get()+"','"+ self.champNomUsager.get()+"','"+ self.champTel.get()+"','"+self.champAdr.get()+"','"+self.champCourriel.get()+"','"+self.listeRole.get(ACTIVE)+"','"+ statut +"')", "usagers.smid")
            self.listeNom.append(self.champNomUsager.get())
            self.changecadre(self.frameAcceuil)
        else:
            messagebox.showinfo("Erreur", "Entrez des valeurs dans toutes les cases")
            
    #Fonction qui inscrit l'org dans la base de données
    def inscrireOrg(self):
        if(self.a.get()=="1"):
            statut = "Actif"
        elif(self.a.get()=="2"):
            statut = "Inactif"
        else:
            statut = "Mauvais"
        
        if(self.champNomOrg.get()!="" and self.champTel.get()!="" and self.champAdr.get()!="" and self.champResp.get()!="" and statut!="Mauvais"):
            self.parent.requeteSQL("INSERT INTO organisations(nom,telephone, adresse, responsable, statut) VALUES ('"+self.champNomOrg.get()+"','"+self.champTel.get()+"','"+self.champAdr.get()+"','"+self.champResp.get()+"','"+ statut+"')", "organisations.smid")
            self.listeOrg.append(self.champNomOrg.get())
            self.changecadre(self.frameAcceuil)
        else:
            messagebox.showinfo("Erreur", "Entrez des valeurs dans toutes les cases")
        
    def afficherCreerOrg(self):   
        self.frameOrg=Frame(self.root)
        self.canevasOrg=Canvas(self.frameOrg,width=640,height=480,bg="white")
        self.canevasOrg.pack()
        
        lblTitre=Label(text="CRÉER ORGANISATION", bg="white")
        self.canevasOrg.create_window(325,35,window=lblTitre,width=300,height=20)
        
        self.lblPasswd=Label(text="Entrez le mot de passe administrateur");
        self.champPasswd=Entry(bg="white")
        
        self.canevasOrg.create_window(225,200,window=self.lblPasswd,width=260,height=30)
        self.canevasOrg.create_window(490,200,window=self.champPasswd,width=150,height=30)
        
        btnValider=Button(text="Valider",bg="lightgray",command=self.validerOrg)
        self.canevasOrg.create_window(310,400,window=btnValider,width=150,height=30)
        
        self.changecadre(self.frameOrg)
        
    def validerOrg(self):
         #Valider si le mot de passe est le bon
        if(self.champPasswd.get()=="a"):

            self.frameInfosOrg=Frame(self.root)
            self.canevasInfosOrg=Canvas(self.frameInfosOrg,width=640,height=480,bg="white")
            self.canevasInfosOrg.pack()
        
            lblTitre=Label(text="CRÉER ORGANISATION", bg="white")
            self.canevasInfosOrg.create_window(325,35,window=lblTitre,width=300,height=20)
            
            lblInstruc=Label(text="Veuillez entrer les informations de l'organisation", bg="white")
            self.canevasInfosOrg.create_window(325,60,window=lblInstruc,width=300,height=20)
            
            self.lblNomOrg=Label(text="Nom: ");
            self.champNomOrg=Entry(bg="white")
            self.canevasInfosOrg.create_window(225,100,window=self.lblNomOrg,width=80,height=30)
            self.canevasInfosOrg.create_window(375,100,window=self.champNomOrg,width=150,height=30)
            self.champNomOrg.insert(0, self.champOrg.get())
            self.champNomOrg.config(state='disabled')
            
            self.lblTel=Label(text="Téléphone: ");
            self.champTel=Entry(bg="white")
            self.canevasInfosOrg.create_window(225,140,window=self.lblTel,width=80,height=30)
            self.canevasInfosOrg.create_window(375,140,window=self.champTel,width=150,height=30)
        
            self.lblAdr=Label(text="Adresse: ");
            self.champAdr=Entry(bg="white")
            self.canevasInfosOrg.create_window(225,180,window=self.lblAdr,width=80,height=30)
            self.canevasInfosOrg.create_window(375,180,window=self.champAdr,width=150,height=30)
        
            self.lblResp=Label(text="Responsable: ");
            self.champResp=Entry(bg="white")
            self.canevasInfosOrg.create_window(225,220,window=self.lblResp,width=80,height=30)
            self.canevasInfosOrg.create_window(375,220,window=self.champResp,width=150,height=30)

            self.lblStat=Label(text="Statut: ");
            self.canevasInfosOrg.create_window(225,270,window=self.lblStat,width=80,height=40)
            
            self.a = StringVar()
            self.a.set("L")
            self.btn1 = Radiobutton(self.root, text="Actif", variable=self.a, value=1)
            self.btn2 = Radiobutton(self.root, text="Inactif", variable=self.a, value=2)
            
            self.canevasInfosOrg.create_window(315,270,window=self.btn1,width=70,height=20)
            self.canevasInfosOrg.create_window(405,270,window=self.btn2,width=70,height=20)

            btnValider=Button(text="Valider",bg="lightgray",command=self.inscrireOrg)
            self.canevasInfosOrg.create_window(310,340,window=btnValider,width=150,height=30)
        
            self.changecadre(self.frameInfosOrg)
        else:
            messagebox.showinfo("Erreur", "Le mot de passe est incorrect. Veuillez recommencer ou contacter votre administrateur.")
            self.changecadre(self.frameOrg)
            pass
    
    def afficherModulesOutils(self):
        self.cadreModules=Frame(self.root)
        self.cadremodule=Frame(self.cadreModules)
        self.canevaModules=Canvas(self.cadremodule,width=640,height=480,bg="white")
        self.canevaModules.pack(side=LEFT)
        
        self.listemodules=Listbox(self.cadremodule,bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        self.ipcentral=Entry(self.cadremodule, bg="white")
        self.ipcentral.insert(0, self.monip)
        btnconnecter=Button(self.cadremodule, text="Choisir un module",bg="lightgray",command=self.requetemodule)
        self.canevaModules.create_window(200,100,window=self.listemodules)
        self.canevaModules.create_window(200,450,window=btnconnecter,width=100,height=30)
        self.cadremodule.pack(side=LEFT)
        #----------------------------------------------------
        self.cadreoutils=Frame(self.cadreModules)
        self.canevaoutils=Canvas(self.cadreoutils,width=640,height=480,bg="white")
        self.canevaoutils.pack()
        
        self.listeoutils=Listbox(bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        btnconnecter=Button(self.cadreoutils, text="Choisir un outil",bg="lightgray",command=self.requeteoutils)
        self.canevaoutils.create_window(200,100,window=self.listeoutils)
        self.canevaoutils.create_window(200,450,window=btnconnecter,width=100,height=30)
        self.cadreoutils.pack(side=LEFT)
    
    def requeteoutils(self):
        mod=self.listeoutils.selection_get()
        if mod:
            self.parent.requeteoutils(mod)
          
    def requetemodule(self):
        mod=self.listemodules.selection_get()
        if mod:
            self.parent.requetemodule(mod)
        
    def loginclient(self):
        self.validerInformations()
                
    def fermerfenetre(self):
        # Ici, on pourrait mettre des actions a faire avant de fermer (sauvegarder, avertir etc)
        self.parent.fermefenetre()

    
    def validerInformations(self):
        self.ipserveur=self.monip# lire le IP dans le champ du layout
        self.nom=self.champId.get() # noter notre nom
        self.org = self.champOrg.get()
        
        orgExiste = 0
        usagerExiste = 0
        
        listeOrg = self.parent.retournerListe('''select nom FROM organisations WHERE statut='Actif' ''', "organisations.smid")
        listeOrgInactif = self.parent.retournerListe('''select nom FROM organisations WHERE statut='Inactif' ''', "organisations.smid")
        
        
        
        for org in listeOrg:
            chaine=org[0]
            if(self.org==chaine):
                orgExiste=1
                listeUsagers = self.parent.retournerListe("select nom FROM clients where organisation='"+self.org+"'" + " AND statut = 'Actif'", "usagers.smid")
                for usager in listeUsagers:
                    chaine=usager[0]
                    if(self.nom==chaine):
                        usagerExiste = 1
                        self.parent.loginclient(self.ipserveur,self.nom, self.org)
                        self.parent.loginBD(self.ipserveur,self.nom, self.org)
        
        if(orgExiste==0):
            for org in listeOrgInactif:
                chaine = org[0]
                if(self.org==chaine):
                    orgExiste=2
                    usagerExiste=2
                    messagebox.showinfo("Erreur", "L'organisation est inactive. Veuillez contacter l'administrateur.")
     
        listeUsagersInactif = self.parent.retournerListe("select nom FROM clients WHERE statut='Inactif' AND organisation='"+ self.org + "'", "usagers.smid")
        if(usagerExiste==0):
            for usager in listeUsagersInactif:
                chaine = usager[0]
                if(self.nom==chaine):
                    orgExiste=2
                    usagerExiste=2
                    messagebox.showinfo("Erreur", "L'usager est inactif. Veuillez contacter l'administrateur.")
                    
        if(orgExiste==0):
            messagebox.showinfo("Erreur", "L'organisation n'existe pas. Veuillez la créer")
            self.afficherCreerOrg()  
        elif(usagerExiste==0):
            messagebox.showinfo("Erreur", "L'usager n'existe pas. Veuillez le créer")
            self.afficherCreerClient()
    
if __name__ == '__main__':
    m=Vue(0,"jmd","127.0.0.1")
    m.root.mainloop()
    