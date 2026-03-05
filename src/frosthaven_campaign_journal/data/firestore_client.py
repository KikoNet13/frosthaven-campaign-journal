from __future__ import annotations

import os
from pathlib import Path

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import firestore

from frosthaven_campaign_journal.config import Settings


class FirestoreConfigError(Exception):
    """Raised when local Firestore configuration is missing or invalid."""


class FirestoreReadError(Exception):
    """Raised when Firestore client initialization or reads fail."""


def validate_firestore_settings(settings: Settings) -> None:
    if not settings.firestore_project_id:
        raise FirestoreConfigError(
            "Falta FIRESTORE_PROJECT_ID. Configúralo en .env, en el entorno o en secretos móviles embebidos."
        )

    credentials_path = settings.google_application_credentials
    if not credentials_path:
        raise FirestoreConfigError(
            "Falta GOOGLE_APPLICATION_CREDENTIALS. Configura la ruta del JSON en .env, en el entorno o en secretos móviles embebidos."
        )

    path_obj = Path(credentials_path)
    if not path_obj.exists():
        raise FirestoreConfigError(
            f"No existe el archivo de credenciales: {path_obj}"
        )


def build_firestore_client(settings: Settings) -> firestore.Client:
    validate_firestore_settings(settings)
    assert settings.google_application_credentials is not None  # narrow typing
    assert settings.firestore_project_id is not None

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

    try:
        return firestore.Client(project=settings.firestore_project_id)
    except DefaultCredentialsError as exc:
        raise FirestoreReadError(
            "No se pudieron cargar las credenciales de Google para Firestore."
        ) from exc
    except Exception as exc:  # pragma: no cover - protective branch
        raise FirestoreReadError(
            f"Error al inicializar el cliente de Firestore: {exc}"
        ) from exc
