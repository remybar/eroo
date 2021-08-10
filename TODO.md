Finalisation:
    - utiliser Celery pour générer le site web (scrap + download images + création data)
        - mise à jour du JS pour poller le state de la task celery
    - ajouter des tests pour le coeur de l'app
        - download des données
        - création des données
        - suppression des données
    - ajouter rapport coverage et essayer de faire grimper le % au fur et à mesure du projet

    - améliorer CSS email
    - rotation de l'api key airbnb


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
    - mettre en place un coffre-fort de mots de passe pro
    - envoi de mail avec Celery

Futures features
    - réservation
    - paiement
    - customisation du site
    - customisation des textes
    - SEO
    - partage pub (facebook, instagram, ...)
    - avoir la possibilité de proposer des features (boite à idée) + envoi d'un mail aux gens qui ont proposé l'idée quand elle est implémentée.
    - bon panel d'admin pour assurer un support efficace
