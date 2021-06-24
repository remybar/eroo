Finalisation:
    - bien tout tester! (erreur JS qui apparaissent de temps en temps ...)
    - deploiement
        - Amazon S3 => à tester!

        - besoin d'une carte de crédit acceptée par Heroku pour:
            - gestion des emails avec SendGrid
            - gestion des logs/exceptions avec Sentry
            - configurer le domaine eroo.fr pour pointer vers la prod
            - configurer le domaine staging.eroo.fr pour pointer vers la staging
            - SSL & https
        - test de déploiement avec poney-checkup

    - sécurité
        - manage.py check --deploy
        - django-honeypot
        - django-2fa (pour l'admin)

    - tests
        - ajouter des tests unitaires pour la CI

Questions:
    - comment gérer proprement les migrations avec Django ?
        - comment les tester avant de les appliquer réellement ?
        - comment revenir en arrière en cas d'erreur ?
    - quelle procédure pour mettre à jour la production ?
        - faut-il couper le service pendant le déploiement ?
        - faut-il prévoir une rotation de 2 serveurs pour switcher sur la nouvelle prod une fois vérifiée que tout va bien ?
    - comment récolter du feedback utilisateur ?
    - quel espace disque par utilisateur ? => calcul du coût d'un utilisateur
    - quelle stratégie SEO ?

Futures améliorations de l'infra
    - utiliser un CDN pour les assets statiques (amazon S3 ? cdn cloudfare ?)
    - utiliser celery pour gérer la génération du site web ?
    - penser à utiliser un cache

Futures features
    - réservation
    - paiement
    - customisation du site
    - customisation des textes
    - SEO
    - partage pub (facebook, instagram, ...)
    - avoir la possibilité de proposer des features (boite à idée) + envoi d'un mail aux gens qui ont proposé l'idée quand elle est implémentée.
    - bon panel d'admin pour assurer un support efficace
