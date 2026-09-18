# EduVault

Plateforme éducative moderne pour partager des ressources pédagogiques entre enseignants et apprenants.

## Fonctionnalités

- Accès public sans compte
- Recherche et filtres avancés
- Gestion des documents par l’administrateur
- Dashboard d’administration
- Upload sécurisé de fichiers
- PDF intégré dans le navigateur
- Dark mode
- Favoris et historique sauvegardés dans le navigateur
- Mode maintenance

## Stack

- Python
- Flask
- SQLite
- SQLAlchemy
- Werkzeug
- Jinja2
- Bootstrap 5
- JavaScript vanilla

## Structure du projet

```text
project/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── instance/
│   └── database.db
├── models/
│   ├── __init__.py
│   ├── admin_user.py
│   ├── subject.py
│   ├── level.py
│   ├── document_type.py
│   ├── tag.py
│   ├── document.py
│   └── site_settings.py
├── routes/
│   ├── public.py
│   ├── admin.py
│   └── auth.py
├── services/
│   ├── document_service.py
│   └── seed_service.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── documents.html
│   ├── document_detail.html
│   ├── search.html
│   └── admin/
│       ├── layout.html
│       ├── login.html
│       ├── dashboard.html
│       ├── documents.html
│       ├── upload.html
│       ├── edit_document.html
│       ├── categories.html
│       ├── levels.html
│       └── settings.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
├── uploads/
└── .env
```

## Installation

```bash
python -m venv venv
```

Windows :

```bash
venv\Scripts\activate
```

Linux/macOS :

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## Configuration

Copiez `.env.example` vers `.env` et configurez les valeurs :

```env
SECRET_KEY=change-this-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
DATABASE_URL=sqlite:///instance/database.db
MAX_CONTENT_LENGTH=15728640
```

## Démarrage

```bash
python app.py
```

Puis ouvrez :

```text
http://127.0.0.1:5000
```

## Compte administrateur

Identifiants par défaut :

- username : admin
- password : admin123

Pour changer le mot de passe d’administration, modifiez le seed initial ou créez un utilisateur manuel dans la base.

## Sécurité

- Hashage des mots de passe avec Werkzeug
- Session Flask pour l’admin
- Validation des uploads
- `secure_filename` sur les fichiers
- Blocage des extensions non autorisées
- Limite de taille configurable
- Protection des routes admin

## Notes

Le projet est prêt à évoluer vers plus de modules, templates spécifiques et statistiques avancées.
