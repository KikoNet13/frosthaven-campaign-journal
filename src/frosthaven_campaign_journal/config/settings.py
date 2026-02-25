from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    env: str = "dev"
    firestore_project_id: str | None = None
    google_application_credentials: str | None = None


def load_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or None
    if credentials_path:
        path_obj = Path(credentials_path)
        if not path_obj.is_absolute():
            credentials_path = str((PROJECT_ROOT / path_obj).resolve())

    return Settings(
        env=os.getenv("FHCJ_ENV", "dev"),
        firestore_project_id=os.getenv("FIRESTORE_PROJECT_ID") or None,
        google_application_credentials=credentials_path,
    )
