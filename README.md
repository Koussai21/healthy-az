# Healthy-AZ

Encyclopédie santé (maladies, symptômes, diagnostics) avec **FastAPI**, **PostgreSQL**, **Vue 3** et assistant **Phi‑3** via **Ollama**.

## Prérequis

- Python 3.11+
- Node.js 20+
- PostgreSQL
- Ollama (pour l’assistant : `ollama pull phi3`)

## Base de données

Créez une base et adaptez l’URL dans `backend/.env` (voir `backend/.env.example`) :

```sql
CREATE DATABASE healthy_az;
```

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Éditez .env (DATABASE_URL, SECRET_KEY)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Données de démonstration (optionnel) :

```bash
python scripts/seed_demo.py
```

Compte démo si créé : `demo` / `demohealthy1`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

L’interface utilise le proxy Vite vers `http://127.0.0.1:8000`. Pour une autre URL API, créez `frontend/.env` avec `VITE_API_URL=https://votre-api`.

## Fonctionnalités

- Inscription / connexion (JWT)
- Encyclopédie avec recherche plein texte simple (ILIKE)
- Fiches par slug, ajout de fiche (utilisateur connecté)
- Forum (sujets + réponses)
- Messagerie privée
- Assistant IA : `POST /api/chat/assistant` (Ollama, modèle configurable)

Les contenus sont à visée éducative et ne remplacent pas un avis médical.
