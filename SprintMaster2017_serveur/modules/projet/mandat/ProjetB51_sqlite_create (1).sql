CREATE TABLE Cie (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text,
	noCivic text,
	rue text,
	noSuite text,
	telephone text,
	statut integer,
	dtStatut text,
	responsable integer
);

CREATE TABLE StatutCie (
	id integer PRIMARY KEY AUTOINCREMENT,
	statut text
);

CREATE TABLE Employe (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text,
	prenom text,
	adresseCourriel text,
	role integer,
	cie integer,
	dateNaissance text,
	dateEmbauche text,
	statut integer,
	motPasse text
);

CREATE TABLE Role (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text
);

CREATE TABLE Log (
	id integer PRIMARY KEY AUTOINCREMENT,
	idEmploye integer,
	dtDebut text,
	dtFin text
);

CREATE TABLE FichierTxt (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text,
	idProjet integer
);

CREATE TABLE Projet (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text,
	dtCreation text,
	responsable integer,
	statut integer,
	commentaire text,
	dtSuivi text
);

CREATE TABLE AnalyseTextuelle (
	id integer PRIMARY KEY AUTOINCREMENT,
	idProjet integer,
	type integer,
	nom text,
	verbe text,
	attribut text,
	ordre integer
);

CREATE TABLE CasUsage (
	id integer PRIMARY KEY AUTOINCREMENT,
	idProjet integer,
	nom text,
	ordre integer,
	TraiterMaquette integer
);

CREATE TABLE TypeCas (
	id integer PRIMARY KEY AUTOINCREMENT,
	cas text
);

CREATE TABLE CasUserMachine (
	id integer PRIMARY KEY AUTOINCREMENT,
	idCas integer,
	typeCas integer,
	ordre integer,
	description text
);

CREATE TABLE Maquette (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text,
	idProjet integer,
	nomFichier text
);

CREATE TABLE MaquetteAction (
	id integer PRIMARY KEY AUTOINCREMENT,
	idMaquette integer,
	type integer,
	x1 integer,
	y1 integer,
	x2 integer,
	y2 integer,
	rouge integer,
	vert integer,
	bleu integer,
	largeur integer,
	fill integer
);

CREATE TABLE TypeAction (
	id integer PRIMARY KEY AUTOINCREMENT,
	action text
);

CREATE TABLE CRC (
	id integer PRIMARY KEY AUTOINCREMENT,
	nomClasse text,
	proprietaire integer,
	idProjet integer
);

CREATE TABLE Responsabilite (
	id integer PRIMARY KEY AUTOINCREMENT,
	nom text,
	idCrc integer,
	previsionHre integer,
	sprintVise integer,
	priorite text,
	idProjet integer
);

CREATE TABLE Sprint (
	id integer PRIMARY KEY AUTOINCREMENT,
	idResponsabilite integer,
	sousEtape text,
	responsable integer,
	tempsPrevu text,
	tempsReel text,
	dtcomplete text,
	probleme text,
	dtVise text,
	dtReel text,
	idProjet integer,
	Ordre integer
);

CREATE TABLE Collaboration (
	id integer PRIMARY KEY AUTOINCREMENT,
	idCRC1 integer,
	idCRC2 integer
);

CREATE TABLE CrcCasUsage (
	id integer PRIMARY KEY AUTOINCREMENT,
	idCRC integer,
	idCasUsage integer
);

CREATE TABLE StatutEmp (
	id integer PRIMARY KEY AUTOINCREMENT,
	statut text
);

CREATE TABLE StatutProjet (
	id integer PRIMARY KEY AUTOINCREMENT,
	statut text
);

