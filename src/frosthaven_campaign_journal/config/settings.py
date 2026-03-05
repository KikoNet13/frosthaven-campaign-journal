from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass
import importlib
import json
import os
from pathlib import Path
import tempfile

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]
_MOBILE_RUNTIME_SECRETS_MODULE = "frosthaven_campaign_journal.config._mobile_runtime_secrets"
_MOBILE_FIRESTORE_CREDENTIALS_FILENAME = "frosthaven_campaign_journal_mobile_firestore_credentials.json"


@dataclass(frozen=True)
class Settings:
    env: str = "dev"
    firestore_project_id: str | None = None
    google_application_credentials: str | None = None


def _load_mobile_runtime_secrets() -> tuple[str | None, str | None]:
    try:
        secrets_module = importlib.import_module(_MOBILE_RUNTIME_SECRETS_MODULE)
    except ModuleNotFoundError:
        return None, None

    firestore_project_id = getattr(secrets_module, "FIRESTORE_PROJECT_ID", None)
    credentials_json_b64 = getattr(
        secrets_module,
        "GOOGLE_APPLICATION_CREDENTIALS_JSON_B64",
        None,
    )

    if isinstance(firestore_project_id, str):
        firestore_project_id = firestore_project_id.strip() or None
    else:
        firestore_project_id = None

    if isinstance(credentials_json_b64, str):
        credentials_json_b64 = credentials_json_b64.strip() or None
    else:
        credentials_json_b64 = None

    return firestore_project_id, credentials_json_b64


def _materialize_mobile_credentials_file(credentials_json_b64: str) -> str | None:
    try:
        credentials_payload = base64.b64decode(credentials_json_b64.encode("utf-8"))
        credentials_json = credentials_payload.decode("utf-8")
        # Validate decoded value is valid JSON credentials before persisting it.
        json.loads(credentials_json)
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError):
        return None

    target_path = Path(tempfile.gettempdir()) / _MOBILE_FIRESTORE_CREDENTIALS_FILENAME
    target_path.write_text(credentials_json, encoding="utf-8")
    return str(target_path.resolve())


def load_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    firestore_project_id = os.getenv("FIRESTORE_PROJECT_ID") or None
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or None
    if credentials_path:
        path_obj = Path(credentials_path)
        if not path_obj.is_absolute():
            credentials_path = str((PROJECT_ROOT / path_obj).resolve())

    if not firestore_project_id or not credentials_path:
        mobile_project_id, mobile_credentials_json_b64 = _load_mobile_runtime_secrets()

        if not firestore_project_id and mobile_project_id:
            firestore_project_id = mobile_project_id

        if not credentials_path and mobile_credentials_json_b64:
            mobile_credentials_path = _materialize_mobile_credentials_file(mobile_credentials_json_b64)
            if mobile_credentials_path:
                credentials_path = mobile_credentials_path

    return Settings(
        env=os.getenv("FHCJ_ENV", "dev"),
        firestore_project_id=firestore_project_id,
        google_application_credentials=credentials_path,
    )
