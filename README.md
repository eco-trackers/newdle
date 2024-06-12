# Newdle

## liens utiles

- [Coding Style](./codingStyle.md)
- [Cahier des charges](./CAHIER_CHARGE.md)

## Objectif

L'objectif de ce projet est de développer une application éco-conçue pour la gestion des notes et des absences dans une école. L'application gérera les élèves, les enseignants, les administrateurs et les matières.

## Fonctionnalités clés

- **Gestion des utilisateurs** : Différents rôles (élève, enseignant, administrateur) avec des droits uniques, connexion des utilisateurs, vérification et modification des notes et des absences, ajout, suppression et réinitialisation de mots de passe des utilisateurs.
- **Gestion des matières** : Création et affectation des matières à des groupes par les administrateurs et les enseignants.
- **Gestion des notes** : Création de notes par les enseignants, consultation des notes et des moyennes, anonymisation automatisée des notes.
- **Gestion des absences** : Système de vérification d'absence amélioré via photo avec participation des élèves sur validation du professeur. Système classique aussi disponible avec renseignement de la présence.

## Guide utilisateur
- Arrivée sur la page d'index qui décrit l'application web éco-conçue Newdle

    - Page Login permet de se connecter, ou réinitialiser son mot de passe (envoi d'un mail) pour tous les utilisateurs si connexion réussie renvoie sur la page principal. Si connecté en admin à login possibilité d'accéder via login à la page de gestion d'utilisateurs. 

        - Page Principal, vue de l'élève et du professeur : ses différentes matières, notes moyennes et absences avec défilement possible.

        - Page Notes, afficher les notes personnelles, si professeur on peut modifier les notes de ses matières et si admin de toutes.

        - Page Absences, vue sur les cours envoie sur une page détails pour chaque cours.
            - Page de détails : absences personnelles liées au cours si élève sinon globale du groupe avec modification et suppresion possible pour un professeur. Trois méthodes de renseignement de la présence possible soit :
                - Le professeur fait l'appel.
                - Les élèves renseignent leur présence eux mêmes.
                - Le professeur prend une photo du groupe, les élèves placent leur pin sur la photo et le professeur valide de manière sécurisée la présence des élèves.

         - Page Group permet d'afficher les membres d'un groupe (son groupe pour l'élève) de les modifier, supprimer ou de créer d'autres groupes (professeur).

        - Page Matières, affiche les matières ou permet d'en créer, modifier, supprimer voir les groupes participants.
       
    - Page Eco-conception, affiche les dernières news, bonnes pratiques et statistiques d'éco-conception de notre site.

    - Page Contact, à voir 

- Retour à la page index toujours possible via logo Newdle.

Commandes custom

- Création d'un 1er admin : python manage.py custom_admin <username> <pwd>

- Initialisation avec des utilisateurs : python manage.py custom_initialize static/csv/testmail.csv
Attention à respecter les entêtes NOM Prénom email password role (student, professor ou admin)
 
