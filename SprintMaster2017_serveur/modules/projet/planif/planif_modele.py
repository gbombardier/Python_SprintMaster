
class Modele():
    

    def __init__(self,parent):
        self.parent=parent
        self.respo = []
        #chargerProjet()
    
    def chargerProjet(self):
        self.parent.lireProjet()
        
    def ajoutRespo(self, idCrc, nom, prio, sprint, temps):
        respo = Responsabilite(self, idCrc, nom, prio, sprint, temps)
        self.respo.append(respo)
        

class Responsabilite():
    

    def __init__(self,parent, idCrc, nom, prio, sprint, temps):
        self.parent=parent
        self.respo = []
        self.idCrc = idCrc
        self.nom = nom
        self.prio = prio
        self.sprint=sprint
        self.temps=temps
    
    def modifTexte(self, texte):
        self.texte = texte
