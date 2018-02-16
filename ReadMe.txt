		Sprint Master
			Un projet de 	Danny Dulong, 
							Jean-Simon Beaudet, 
							Gabriel Bombardier, 
							Justin Dugas, 
							Ibrahim El Hedhiri

						
Logiciel SaaS permettant d'utiliser des modules de gestion de projet utilisant la m�thode � Jean-Marc.


Fonctionnement des diff�rents modules : 

Module LOGIN : 
Cr�ation des organisations : 
			- On peut cr�er une organisation avec le mot de passe "a". 
			
Cr�ation usager: 	
			- On peut cr�er un usager dans une organisation avec le mot de passe "a".

Les noms et organisations cr�er sont report�s dans l'�cran de login.

Module S�LECTION MODULE : 
			- Une liste des modules disponibles est affich�e et on peut s�lectionner pour l'instant le module PROJET
			
Module projet: 		
			- On peut cr�er des projets.
			- Les projets sont sauvegard�s dans la base de donn�e de l'organisation.
			- En cliquant sur suivant, on acc�de � la liste des modules disponibles pour un projet.

Module mandat:

			- Si non, ouvre une fen�tre de dialogue qui demande de s�lectionner un fichier � ouvrir 
			- Importe contenu du fichier s�lectionn� dans le text widget qui est �ditable
			- Si fermeture du dialogue sans s�lection de fichier la fen�tre principale ouvre quand m�me et on peut manuellement ins�rer du texte
			- Importe le texte dans le text widget �ditable
			- Importe les noms, verbes et adjectifs(attributs) dans leurs listbox respectifs selon s'ils sont explicites, implicites ou suppl�mentaires
			- S�lection de texte dans le text widget avec la souris
			- Clic sur bouton noms, verbes, ou adjectifs au dessus du listbox dans la section Explicite
			- taper un mot dans le champ texte (Entry) au dessous du text widget
			- Clic sur bouton noms, verbes, ou adjectifs au dessus du listbox dans la section Implicite ou Suppl�mentaire
			- S�lectionner un mot � supprimer dans un listbox
			- Clic sur bouton supprimer au dessus du listbox
			- Clic sur bouton Enregistrer
			- Enregistre le contenu du text widget et des listbox dans la BD
			- Clic sur bouton supprimer
			- Supprime le mandat et le contenu pour le projet actuel dans la BD mais n'affecte pas le travail local
	

Module Cas d'usage/Scenario:
			- A l'ouverture, affiche les cas d'usages dans un listbox en fonction du projet.
			- A L'appui du bouton ajouter, un menu d'ajout de cas d'usage apparait.
			- Ensuite, l'usager entre les interactions de son choix (Usager/ordinateur).
			- Le module cas d'usage permet  de g�nerer les sc�narios d'utilisation.
			- Toutes les modifications sont faites dans la base de donn�es.
			- Le module enregistre les cas dans la base de donn�e.
			- Les retraits sont fais dans la BD.
			- L'ordre et le nom des sc�narios peuvent etre modifi�s.
			- Le nom des cas peuvent etre modifi�s.
			- Les cas peuvent tous etre retir�s, ainsi que les sc�narios.
			- Des interactions peuvent etres ajout�es depuis diff�rent menus.
			- Le module permet l'affichage clair de nos id�es.
			- En cliquant sur suivant, on acc�de au module de CRC.

Module Maquette:
			- importe les titres des maquettes existante dans listBox Choisir une maquette
			- Donner un titre unique � la maquette (pas pr�sent dans listbox)
			- Clic sur bouton cr�er maquette
			- cr�ation de la maquette et la surface de dessin apparait
			- S�lectionner la maquette � ouvrir dans le listbox
			- Clic sur bouton Ouvrir une maquette
			- Si pas d�j� pr�sente la surface de dessin appara�t
			- Importe les formes sur la surface de dessin
			- Clic sur bouton Enregistrer
			- Enregistre la maquette et son contenu dans BD
			- S�lectionner une maquette � supprimer dans le listbox 
			- Clic sur bouton supprimer la maquette
			- Supprime la maquette et son contenu de la BD mais n'affecte pas le travail local
			- S�lectionner le bouton de la forme � dessiner
			- Clic sur la surface de dessin et dragger la souris puis rel�cher
			- S�lectionner bouton texte
			- �crire le texte d�sir� dans le champ juste � c�t� du bouton
			- Clic sur la surface de dessin � l'endroit d�sir�
			- S�lectionner bouton supprimer forme
			- Clic sur forme ou texte � supprimer dans la surface de dessin

Module CRC:
			- Le module CRC permet de cr�er des CRC et des responsabilit�s li�s � des cas d'usage. 
			- On peut voir quel cas d'usage est d�j� li�.
			- Les CRC sont enregistr�s dans la base de donn�e de compagnie.
			
Module Planif:
			- Le module importe les responasabilit�s des CRC afin de les ordonner en ordre de sprint et d'urgence.
			- Le module permet de les r�ordonner et de les sauvegarder dans la base de donn�e.

Module Sprint:
			- Affiche la planification globale et permet la construction de t�ches d�taill�es.
			- Permet la comptabilisation du temps r�el pass� sur un projet. 
			- Permet l'enregistrement dans la base de donn�e.
			
Outils Meta_SQL : 	
			- Permet d'�tre superusager sur la structure et le contenu des BD
			- On voit la liste des BD de l'usager connect�
			- On peut ajouter ou supprimer des BD
			- On peut voir les tables des BD et supprimer des tables
			- On peut afficher les insertions


Interactions avec le serveur de base de donn�e : 
			- Le serveur de base de donn�e prend toutes les requetes de modifications, d'ajout et de suppression des modules.
			- Le serveur effectue les t�ches dans les bases de donn�es.
			- Le serveur garde une trace (.log) des t�ches effectu�es qui sera utilis�e pour la facturation.
			- Le serveur renvoie les informations pertinentes suite � la requ�te au module.

Interactions entre les modules : 
			- Le module projet envoie le ID de projet aux autres modules afin de faire les requetes SQL pr�cises.
			- Les modules qui ouvrent d'autre modules passent par le serveur SaaS pour effectuer le t�l�chargement des modules.


