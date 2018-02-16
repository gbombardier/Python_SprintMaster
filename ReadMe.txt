		Sprint Master
			Un projet de 	Danny Dulong, 
							Jean-Simon Beaudet, 
							Gabriel Bombardier, 
							Justin Dugas, 
							Ibrahim El Hedhiri

						
Logiciel SaaS permettant d'utiliser des modules de gestion de projet utilisant la méthode à Jean-Marc.


Fonctionnement des différents modules : 

Module LOGIN : 
Création des organisations : 
			- On peut créer une organisation avec le mot de passe "a". 
			
Création usager: 	
			- On peut créer un usager dans une organisation avec le mot de passe "a".

Les noms et organisations créer sont reportés dans l'écran de login.

Module SÉLECTION MODULE : 
			- Une liste des modules disponibles est affichée et on peut sélectionner pour l'instant le module PROJET
			
Module projet: 		
			- On peut créer des projets.
			- Les projets sont sauvegardés dans la base de donnée de l'organisation.
			- En cliquant sur suivant, on accède à la liste des modules disponibles pour un projet.

Module mandat:

			- Si non, ouvre une fenêtre de dialogue qui demande de sélectionner un fichier à ouvrir 
			- Importe contenu du fichier sélectionné dans le text widget qui est éditable
			- Si fermeture du dialogue sans sélection de fichier la fenêtre principale ouvre quand même et on peut manuellement insérer du texte
			- Importe le texte dans le text widget éditable
			- Importe les noms, verbes et adjectifs(attributs) dans leurs listbox respectifs selon s'ils sont explicites, implicites ou supplémentaires
			- Sélection de texte dans le text widget avec la souris
			- Clic sur bouton noms, verbes, ou adjectifs au dessus du listbox dans la section Explicite
			- taper un mot dans le champ texte (Entry) au dessous du text widget
			- Clic sur bouton noms, verbes, ou adjectifs au dessus du listbox dans la section Implicite ou Supplémentaire
			- Sélectionner un mot à supprimer dans un listbox
			- Clic sur bouton supprimer au dessus du listbox
			- Clic sur bouton Enregistrer
			- Enregistre le contenu du text widget et des listbox dans la BD
			- Clic sur bouton supprimer
			- Supprime le mandat et le contenu pour le projet actuel dans la BD mais n'affecte pas le travail local
	

Module Cas d'usage/Scenario:
			- A l'ouverture, affiche les cas d'usages dans un listbox en fonction du projet.
			- A L'appui du bouton ajouter, un menu d'ajout de cas d'usage apparait.
			- Ensuite, l'usager entre les interactions de son choix (Usager/ordinateur).
			- Le module cas d'usage permet  de génerer les scénarios d'utilisation.
			- Toutes les modifications sont faites dans la base de données.
			- Le module enregistre les cas dans la base de donnée.
			- Les retraits sont fais dans la BD.
			- L'ordre et le nom des scénarios peuvent etre modifiés.
			- Le nom des cas peuvent etre modifiés.
			- Les cas peuvent tous etre retirés, ainsi que les scénarios.
			- Des interactions peuvent etres ajoutées depuis différent menus.
			- Le module permet l'affichage clair de nos idées.
			- En cliquant sur suivant, on accède au module de CRC.

Module Maquette:
			- importe les titres des maquettes existante dans listBox Choisir une maquette
			- Donner un titre unique à la maquette (pas présent dans listbox)
			- Clic sur bouton créer maquette
			- création de la maquette et la surface de dessin apparait
			- Sélectionner la maquette à ouvrir dans le listbox
			- Clic sur bouton Ouvrir une maquette
			- Si pas déjà présente la surface de dessin apparaît
			- Importe les formes sur la surface de dessin
			- Clic sur bouton Enregistrer
			- Enregistre la maquette et son contenu dans BD
			- Sélectionner une maquette à supprimer dans le listbox 
			- Clic sur bouton supprimer la maquette
			- Supprime la maquette et son contenu de la BD mais n'affecte pas le travail local
			- Sélectionner le bouton de la forme à dessiner
			- Clic sur la surface de dessin et dragger la souris puis relâcher
			- Sélectionner bouton texte
			- Écrire le texte désiré dans le champ juste à côté du bouton
			- Clic sur la surface de dessin à l'endroit désiré
			- Sélectionner bouton supprimer forme
			- Clic sur forme ou texte à supprimer dans la surface de dessin

Module CRC:
			- Le module CRC permet de créer des CRC et des responsabilités liés à des cas d'usage. 
			- On peut voir quel cas d'usage est déjà lié.
			- Les CRC sont enregistrés dans la base de donnée de compagnie.
			
Module Planif:
			- Le module importe les responasabilités des CRC afin de les ordonner en ordre de sprint et d'urgence.
			- Le module permet de les réordonner et de les sauvegarder dans la base de donnée.

Module Sprint:
			- Affiche la planification globale et permet la construction de tâches détaillées.
			- Permet la comptabilisation du temps réel passé sur un projet. 
			- Permet l'enregistrement dans la base de donnée.
			
Outils Meta_SQL : 	
			- Permet d'être superusager sur la structure et le contenu des BD
			- On voit la liste des BD de l'usager connecté
			- On peut ajouter ou supprimer des BD
			- On peut voir les tables des BD et supprimer des tables
			- On peut afficher les insertions


Interactions avec le serveur de base de donnée : 
			- Le serveur de base de donnée prend toutes les requetes de modifications, d'ajout et de suppression des modules.
			- Le serveur effectue les tâches dans les bases de données.
			- Le serveur garde une trace (.log) des tâches effectuées qui sera utilisée pour la facturation.
			- Le serveur renvoie les informations pertinentes suite à la requête au module.

Interactions entre les modules : 
			- Le module projet envoie le ID de projet aux autres modules afin de faire les requetes SQL précises.
			- Les modules qui ouvrent d'autre modules passent par le serveur SaaS pour effectuer le téléchargement des modules.


