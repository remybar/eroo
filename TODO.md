Finalisation:
    - deploiement
        - sécuriser API scrapper (limiter à eroo host + authentication)
        - besoin d'une carte de crédit acceptée par Heroku pour:
            - gestion des emails avec SendGrid
            - gestion des logs/exceptions avec Sentry
            - configurer le domaine eroo.fr pour pointer vers la prod
            - configurer le domaine staging.eroo.fr pour pointer vers la staging
            - SSL & https
        - gestion des medias sur Amazon S3 (ou autre)
        - test de déploiement avec poney-checkup
        - conserver les données scrappées sur Amazon S3 aussi ?

    - dashboard
        - nettoyer les fichiers html et compléter les TODO (<head>)
        - quels keywords dans <head> ?
        - nettoyer le repo en supprimant tout ce qui ne sert à rien (js, images, ...)

    - template 1
        - rendu du footer dans le template website
        - booking bar avec calendriers + pop-up "to be implemented"

    - sécurité
        - django-honeypot
        - django-2fa (pour l'admin)


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
