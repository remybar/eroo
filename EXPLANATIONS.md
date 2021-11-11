# Architecture

- domaine `eroo.fr`
- mail: sendgrid + OVH: `contact@eroo.fr`
- hosting sur heroku avec 2 workers : le serveur web + celery
- sentry pour les erreurs/exceptions
- database: postgres
- storage des assets : Amazon S3
- logging: logentries
- google map: via gcp remy.baranx@gmail.com (Map Javascript API)

# Celery

- use Redis as message broker:
    `redis-cli ping` checks that Redis server is running

- start the worker process
    `celery -A eroo worker -l info` 

- test that the Celery task scheduler is ready for action:
    `celery -A eroo beat -l info`

- use `django-celery-results` to store tasks results in the database (backend)

# Heroku

- voir les apps: `heroku apps`

- sélectionner une app: `heroku git:remote -a YOUR_APP`

- voir les logs: `heroku logs [-d dynoname]` 

- voir l'état des dynos: `heroku ps`

- pour créer le superuser sur heroku: `heroku run -a eroo-app-staging python manage.py createsuperuser`

- pour activer le mode maintenance : `heroku maintenance:on` (`heroku maintenance:off` pour désactiver)

# CI/CD

- définir des environnements séparés pour avoir plusieurs jeux de variables d'environnements (https://docs.gitlab.com/ee/ci/environments/index.html)

# Front-end

## materio vuejs theme

- pour désactiver toutes les erreurs de tri des imports, modifier .eslintrc.js avec:
```javascript
    // ignore import sorting
    "sort-imports": ["error", {
      "ignoreDeclarationSort": true,
      "ignoreDeclarationSort": true,
      "ignoreMemberSort": true,
      "allowSeparatedGroups": true,
    }],
```

## VueX / reactive property with arrays and objects

- vueX avec vue 2 ne gère pas bien la réactivité des objets et tableaux. Pour les objets, il faut utiliser `Vue.set(state.housings, id, housing)` et pas directement modifier l'objet.
- avec les tableaux il faut utiliser les méthodes et pas directement []

## Transfert de donnée back-end / front-end

### via Django template

* passer les données via le contexte de la vue
* utiliser la commande `json_script` de Django pour générer un bloc json dans le template (par exemple: `{{ config|json_script:'config' }}`)
* récupérer cet objet json dans le store de l'app vue via `JSON.parse(document.getElementById('config').textContent)`

=> top pour des données statiques pas trop volumineuse pour ne pas exploser le temps de chargement de la page.

### via API
