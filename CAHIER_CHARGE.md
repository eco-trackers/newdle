# cahier des charges

## Objectif

L'objectif de ce projet est de réaliser une application eco-concu de gestion de notes et d'absence pour une école. Cette application doit permettre de gérer les élèves, les professeurs, les matières.

## Fonctionnalités

### Gestion des Utilisateurs

- Différencier les utilisateurs en fonction de leur rôle (élève, professeur, administrateur), et leur donner des droits différents
- Permettre aux utilisateurs de se connecter
- Permettre aux élèves de consulter leurs notes et leurs absences, ainsi que valider leurs présences
- Permettre aux professeurs de consulter les notes et les absences de leurs élèves, ainsi que de les modifier
- Permettre aux administrateurs de gérer les utilisateurs, de créer des classes, maquettes, matières, etc, et de modifier les notes et les absences

### Gestion des Matières

- Creation de matières par les administrateurs et professeurs
- Affectation des matières aux maquettes
- Affectation des matières aux classes
- Affectation des matières aux professeurs

### Gestion des Notes

- Creation de notes par les professeurs sur une matière en reference à la maquette
- Consultation des notes par les élèves et les professeurs
- Consultation des moyennes (individuelle, par UE, par maquette)
- Anonymisation des notes automatisé et eco concue
- Generation des rapports (type ENSISA)

### Gestion des Absences

- Ajout des absences par les professeurs
- Consultation des absences par les élèves et les professeurs
- Renseignement des absences par les élèves (anotation d'image par les élèves (RGPD TMTC))
- Generation de rapport d'absence (type ENSISA meme si ca existe pas)

## Technologie

### Frontend

- HTML,CSS,JS
- Bootstrap (autoformation)
- JQuerry
- Responsive design

### Backend

- Django/Python
- Modules Django externes potentiel (django-rest-framework, django-crispy-forms, etc.)

## listes des fonctionnalités

### General

- Eco conception
- droit (custom? ou django+custom? ou django?)
- EDT (si possible)
- gestion classe + groupe
- system de connection
- messagerie interne (si vraiment possible)
- Responsive design
- _**CGU**_

### Note

- Maquette modifiable
- traitement 
- assignation a une matière
- exportation (type ENSISA)
- anonymisation
- notif de nouvelle note par mail (si possible)
- API (si vraiment on a le temps et on se fait chier)

### Absence

- systeme amélioré de gestion des absences
