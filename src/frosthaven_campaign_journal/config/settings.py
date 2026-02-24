from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    env: str = "dev"
    firestore_project_id: str | None = None
    google_application_credentials: str | None = None


def load_settings() -> Settings:
    return Settings(
        env=os.getenv("FHCJ_ENV", "dev"),
        firestore_project_id=os.getenv("FIRESTORE_PROJECT_ID") or None,
        google_application_credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        or None,
    )
