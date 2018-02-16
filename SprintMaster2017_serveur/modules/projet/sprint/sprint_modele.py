class Modele():
    def __init__(self,parent):
        self.parent=parent
        self.planif=[]
        self.loadPlanif()
       
        
    def trouverIndexSous(self,current,idTache):
        index=0
        for n in self.planif[idTache].sousTache:
            if (n.sousTache==self.parent.vue.listSousTache.get(current)):
                print("index "+str(index))
                return index
            else:
                index+=1
        
    def trouverIndex(self,current):
        index=0
        for n in self.planif:
            #if (n.nom==self.parent.vue.listeTache.get(current)):
            if (n.nom==current):
                print("index "+str(index))
                return index
            else:
                index+=1
       
    def loadPlanif(self):
        rep=self.parent.loadData("SELECT * FROM Responsabilite WHERE idProjet="+str(self.parent.idProjet)+" ORDER BY sprintVise ")
        for n in rep:
            if n:
                self.planif.append(Planif(self,n[0],n[1],n[3],n[4],n[5],n[2]))
    
    def modifSousTache(self,idTache,idSousTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        self.planif[idTache].modifSousTache(idSousTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
               
    def ajoutSousTache(self,idTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        return self.planif[idTache].ajoutSousTache(idTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
         
class Planif():
    def __init__(self,parent,id,nom,previsionHre,sprintVise,priorite,idCrc):
        self.parent=parent
        self.idCrc=idCrc
        self.id=id
        self.nom=nom
        self.previsionHre=previsionHre
        self.sprintVise=sprintVise
        self.priorite=priorite
        self.sousTache=[]
        self.loadSousTache()
        self.sousTache.sort()
    
    def modifSousTache(self,idSousTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        ordreST=self.sousTache[idSousTache].ordre
        if(ordre>ordreST):
            self.diminuerPrio(ordre,ordreST)
        elif(ordre<ordreST):
            self.augmenterPrio(ordre,ordreST)
        self.sousTache[idSousTache].modifSousTache(nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre)
        self.sousTache.sort()
    
    def ajoutSousTache(self,idTache,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        sql="INSERT INTO Sprint (idResponsabilite,sousEtape,responsable,tempsPrevu,tempsReel,dtcomplete,probleme,dtVise,dtReel,idProjet,Ordre) VALUES ("+str(self.id)+",'"+nom+"','"+responsable+"','"+tempsPrevu+"','"+tempsReel+"','"+dtFini+"','"+probleme+"','"+dtPrevue+"','"+dtRelle+"',"+str(self.parent.parent.idProjet)+","+str(ordre)+")"
        id=self.parent.parent.ajout(sql)
        ##modif ordre d�j� existante si insert pas � la fin
        ordreST=len(self.sousTache)
        if (ordre<=ordreST):
            self.augmenterPrio(ordre,ordreST)
        ##fin
        self.sousTache.append(SousTache(self,id,nom,responsable,tempsPrevu,tempsReel,probleme,dtRelle,dtFini,dtPrevue,ordre))
        self.sousTache.sort()
        return id
    
    def augmenterPrio(self,ordreNew,ordreOld):
        while ordreNew<=ordreOld:
            self.sousTache[ordreNew-1].ordre+=1
            self.sousTache[ordreNew-1].modifOrdre()
            ordreNew+=1
    
    def diminuerPrio(self,ordreNew,ordreOld):
        while ordreNew>=ordreOld:
            self.sousTache[ordreNew-1].ordre-=1
            self.sousTache[ordreNew-1].modifOrdre()
            ordreNew-=1
            
       
    def loadSousTache(self):
        rep=self.parent.parent.loadData("SELECT * FROM Sprint WHERE idResponsabilite="+str(self.id))
        for n in rep:
            print(n)
            self.sousTache.append(SousTache(self,n[0],n[2],n[3],n[4],n[5],n[7],n[9],n[6],n[8],n[11]))
             
class SousTache():
    def __init__(self,parent,id,sousTache,responsable,tempsPrevu,tempsFait,probleme,dtReel,dtComplete,dtPrevu,ordre):
        print("test load")
        print(id)
        print(sousTache)
        print(responsable)
        print(tempsPrevu)
        self.parent=parent
        self.id=id
        self.responsable=responsable
        self.tempsPrevu=tempsPrevu
        self.tempsFait=tempsFait
        self.probleme=probleme
        self.dtComplete=dtComplete
        self.dtPrevu=dtPrevu
        self.dtReel=dtReel
        self.ordre=ordre
        self.sousTache=sousTache
    
    def __lt__(self,other):
        return self.ordre<other.ordre
    
    def modifOrdre(self):
        sql="Update Sprint SET Ordre="+str(self.ordre)+" WHERE id="+str(self.id)
        print(sql)
        self.parent.parent.parent.modification(sql)
    
    def modifSousTache(self,nom,dtFini,dtPrevue,dtRelle,dtSousTache,tempsPrevu,tempsReel,probleme,responsable,ordre):
        self.responsable=responsable
        self.tempsPrevu=tempsPrevu
        self.tempsFait=tempsReel
        self.probleme=probleme
        self.dtComplete=dtFini
        self.dtPrevu=dtPrevue
        self.dtReel=dtRelle
        self.sousTache=nom
        self.ordre=ordre
        sql="Update Sprint SET sousEtape='"+self.sousTache+"',responsable='"+self.responsable+"',tempsPrevu='"+self.tempsPrevu+"',tempsReel='"+self.tempsFait+"',dtcomplete='"+self.dtComplete+"',probleme='"+self.probleme+"',dtVise='"+self.dtPrevu+"',dtReel='"+self.dtReel+"',Ordre="+str(self.ordre)+" WHERE id="+str(self.id)
        print(sql)
        self.parent.parent.parent.modification(sql)
        
       