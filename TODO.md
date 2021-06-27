Finalisation:
    - améliorer CSS email
    - popup non dispo pour le bouton réserver en haut à droite
    - résoudre error unicode
    - ajouter logging propre sur Heroku pour voir un peu plus ce qu'il se passe
    - ajuster les droits sur amazon S3
    - gérer eroo.fr => app prod
    - Amazon S3 => à tester pour media files
    - ajouter de pages correctes pour les erreurs 404, 500, ...
    - bien tout tester! (erreur JS qui apparaissent de temps en temps ...)

    - ajouter un domaine à mailgun pour voir mg.eroo.fr
    - mettre en place un coffre-fort de mots de passe pro
    - ajouter des tests unitaires pour la CI
    - comprendre le fonctionnement des domaines, DNS, etc ...


Questions:
    - comment gérer proprement les migrations avec Django ?
        - comment les tester avant de les appliquer réellement ?
        - comment revenir en arrière en cas d'erreur ?

        https://sobolevn.me/2019/10/testing-django-migrations
        https://github.com/wemake-services/django-test-migrations#credits


    - quelle procédure pour mettre à jour la production ?
        - faut-il couper le service pendant le déploiement ?
        - faut-il prévoir une rotation de 2 serveurs pour switcher sur la nouvelle prod une fois vérifiée que tout va bien ?
    - comment récolter du feedback utilisateur ?
    - quel espace disque par utilisateur ? => calcul du coût d'un utilisateur
    - quelle stratégie SEO ?

Futures améliorations de l'infra
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
