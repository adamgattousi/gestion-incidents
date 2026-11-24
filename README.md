# Gestion des incidents informatiques

Application web qui permet aux étudiants et aux enseignants de signaler les incidents informatiques (PC en panne, wifi, projecteur...) et de suivre leur traitement.

Le projet met en place une chaîne DevOps complète : Git/GitHub, Docker, Docker Compose, GitHub Actions (CI/CD) et publication de l'image dans GHCR.

## Fonctionnalités

- Ajouter un incident
- Afficher la liste des incidents
- Consulter les détails d'un incident
- Modifier le statut (Nouveau, En cours, Résolu)
- Supprimer un incident

Chaque incident contient : identifiant, titre, description, lieu, priorité (Faible, Moyenne, Élevée) et statut.

## Technologies

- Python 3.12 + Flask
- SQLite (base de données dans un fichier)
- pytest pour les tests
- Docker / Docker Compose
- GitHub Actions + GitHub Container Registry (GHCR)

## Structure du projet

```
gestion-incidents/
├── app/
│   ├── main.py            # routes Flask
│   ├── database.py        # accès à la base SQLite
│   ├── templates/         # pages HTML
│   └── static/style.css
├── tests/
│   ├── conftest.py
│   ├── test_home.py
│   └── test_incidents.py
├── Dockerfile
├── compose.yaml
├── compose.deploy.yaml
├── requirements.txt
├── pytest.ini
└── .github/workflows/
    ├── ci.yml
    └── cd.yml
```

## Lancer l'application en local (sans Docker)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / Mac
pip install -r requirements.txt
python -m app.main
```

Puis ouvrir http://localhost:5000

## Lancer les tests

```bash
pytest -v
```

## Docker

```bash
docker build -t gestion-incidents .                       # construire l'image
docker run -d -p 5000:5000 --name incidents gestion-incidents   # lancer un conteneur
docker ps                                                 # vérifier le conteneur
```

Ouvrir http://localhost:5000 puis arrêter avec `docker stop incidents && docker rm incidents`.

## Docker Compose

```bash
docker compose up -d --build    # démarrer
docker compose ps               # vérifier les services
docker compose logs             # consulter les journaux
docker compose down             # arrêter
```

Les données sont gardées dans le volume `incidents-data`, elles ne sont pas perdues quand on arrête les conteneurs.

## Intégration continue (CI)

Le fichier `.github/workflows/ci.yml` se lance à chaque **push** et à chaque **Pull Request** sur `main`. Il :

1. récupère le code
2. installe Python et les dépendances
3. lance les tests avec pytest
4. vérifie `compose.yaml` avec `docker compose config`
5. construit l'image Docker

## Publication dans GHCR (CD)

Le fichier `.github/workflows/cd.yml` se lance à chaque push sur `main` :

1. le job `tests` exécute les tests
2. le job `publication` (qui dépend de `tests` avec `needs`) construit l'image, se connecte à GHCR avec le `GITHUB_TOKEN` et publie l'image avec deux tags : `latest` et le SHA du commit.

L'image est visible dans l'onglet **Packages** du profil GitHub.

```bash
docker pull ghcr.io/adamgattousi/gestion-incidents:latest
docker images
```

## Déploiement

Le fichier `compose.deploy.yaml` utilise directement l'image de GHCR, il ne reconstruit rien.

```bash
docker compose -f compose.deploy.yaml pull     # récupérer l'image
docker compose -f compose.deploy.yaml up -d    # démarrer
docker compose -f compose.deploy.yaml ps       # vérifier
docker compose -f compose.deploy.yaml logs     # journaux
```

### Mettre à jour l'application

1. Modifier le code, faire un commit et un push sur `main`
2. Attendre que les workflows CI et CD soient verts dans l'onglet **Actions**
3. Récupérer la nouvelle image et relancer :

```bash
docker compose -f compose.deploy.yaml pull
docker compose -f compose.deploy.yaml up -d
```

> Si le package est privé, il faut d'abord se connecter : `docker login ghcr.io` (avec un token personnel, à ne jamais partager).

## Captures d'écran

Les captures sont dans le dossier `captures/` :

- `01-pipeline-cd-reussi.jpg` : workflow CD réussi (tests puis publication)
- `02-ci-echec.jpg` : test volontairement cassé, échec à l'étape « Exécuter les tests »
- `03-ci-corrige.jpg` : historique des workflows, rouge puis vert après la correction
- `04-image-ghcr.jpg` : image publiée dans GHCR avec les tags `latest` et SHA
- `05-application-deployee.jpg` : application lancée avec `compose.deploy.yaml`
- `06-mise-a-jour.jpg` : nouvelle version après `docker compose pull` et `up -d` (nombre d'incidents affiché)

## Auteur

- Adam Gattousi
