Finalisation:
    - dashboard
        - meilleure affichage des erreurs sur le dashboard (alert) + dismiss
        - gestion de la limite de sites web générés
        - ne pas télécharger les medias qui existent déjà (photos) + vérifier que ça fonctionne bien (doublons)
        - nettoyer les fichiers html et compléter les TODO (<head>)
        - quels keywords dans <head> ?

    - template 1
        - rendu du footer dans le template website
        - booking bar avec calendriers + pop-up "to be implemented"

    - deploiement
        - utiliser postgres au lieu de sqlite
        - nettoyer le repo en supprimant tout ce qui ne sert à rien (js, images, ...)
        - gestion des medias sur Amazon S3 (ou autre)
        - gestion des emails avec SendGrid (avoir un mail contact@eroo.fr)
        - avoir un pipeline staging/production pour pouvoir vérifier que tout roule en staging avant de déployer en production.
        - pouvoir monitorer tout ça et principalement les erreurs (du scrapper notamment)
        - scrapper: garder les données scrappées pour pouvoir investiguer en cas d'erreur (dans un fichier json)
        - envoi de mail en cas d'erreur de scrapping/de conversion des données/etc...

Questions:
    - comment vais-je gérer/tester les mises à jour ? (migrations de db, ...)
    - comment récolter du feedback utilisateur ?
    - quel espace disque ?

Marketing
    - valider le problème via Facebook groups
    - mettre en place un lieu d'échange/de feedback





- futur
    - avoir la possibilité de proposer des features (boite à idée) + envoi d'un mail aux gens qui ont proposé l'idée quand elle est implémentée.
    - possibilité d'éditer les données avant génération ?
    - améliorer la sécurité du panel d'admin
        https://hackernoon.com/5-ways-to-make-django-admin-safer-eb7753698ac8
