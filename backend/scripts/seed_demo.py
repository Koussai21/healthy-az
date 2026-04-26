"""Exemple: python -m scripts.seed_demo (depuis le dossier backend, avec DATABASE_URL configurée)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base  # noqa: E402
from app.models import EncyclopediaEntry, User  # noqa: E402
from app.models.encyclopedia import EntryKind  # noqa: E402
from app.auth import hash_password  # noqa: E402
from app.utils.slug import slugify  # noqa: E402


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "demo").first():
            db.add(
                User(
                    first_name="Démo",
                    last_name="Healthy",
                    email="demo@healthy-az.local",
                    username="demo",
                    hashed_password=hash_password("demohealthy1"),
                )
            )
            db.commit()
        samples = [
            (
                EntryKind.symptome.value,
                "Fièvre",
                "Élévation temporaire de la température corporelle.",
                "La fièvre est souvent un signe d'infection ou d'inflammation. Mesurer la température et surveiller l'hydratation. Consulter un médecin si la fièvre est très élevée ou persistante.",
            ),
            (
                EntryKind.diagnostic.value,
                "Hypertension artérielle",
                "Pression artérielle durablement élevée.",
                "Diagnostic posé par mesures répétées de la tension. Prise en charge: hygiène de vie, suivi médical, traitement si indiqué. Ce contenu est éducatif et ne remplace pas une consultation.",
            ),
            (
                EntryKind.maladie.value,
                "Grippe",
                "Infection virale respiratoire saisonnière.",
                "Symptômes: fièvre, courbatures, fatigue, toux. Repos, hydratation et avis médical en cas de signes de gravité ou de facteurs de risque.",
            ),
        ]
        for kind_str, title, summary, content in samples:
            slug = slugify(title)
            if db.query(EncyclopediaEntry).filter(EncyclopediaEntry.slug == slug).first():
                continue
            db.add(
                EncyclopediaEntry(
                    kind=kind_str,
                    title=title,
                    slug=slug,
                    summary=summary,
                    content=content,
                    author_id=None,
                )
            )
        db.commit()
        print("Seed OK (utilisateur demo / demohealthy1 si créé).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
