from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from google.api_core.exceptions import Aborted
from google.cloud import firestore

from frosthaven_campaign_journal.data.write_errors import (
    FirestoreConflictError,
    FirestoreTransitionInvalidError,
    FirestoreValidationError,
    FirestoreWriteError,
)
from frosthaven_campaign_journal.models import EntryRef
from frosthaven_campaign_journal.resource_catalog import RESOURCE_KEYS


CAMPAIGN_ID = "01"
WEEKS_PER_YEAR = 20


@dataclass(frozen=True)
class ResourceWriteResult:
    entry_ref: EntryRef
    resource_key: str
    adjustment_delta: int
    entry_delta_after: int
    campaign_total_after: int
    no_op: bool = False


@dataclass(frozen=True)
class ResourceBulkWriteResult:
    entry_ref: EntryRef
    changed_keys: tuple[str, ...]
    entry_resource_deltas_after: dict[str, int]
    campaign_totals_after_for_changed_keys: dict[str, int]
    no_op: bool = False


def adjust_resource_delta(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    resource_key: str,
    adjustment_delta: int,
) -> ResourceWriteResult:
    if resource_key not in RESOURCE_KEYS:
        raise FirestoreValidationError(f"`resource_key` no soportada: {resource_key!r}.")
    if isinstance(adjustment_delta, bool) or not isinstance(adjustment_delta, int):
        raise FirestoreValidationError("`adjustment_delta` debe ser entero.")
    if adjustment_delta == 0:
        entry_snapshot = _entry_doc_ref(client, entry_ref).get()
        if not entry_snapshot.exists:
            raise FirestoreTransitionInvalidError("La entry ya no existe.")
        entry_data = entry_snapshot.to_dict() or {}
        resource_deltas = _parse_resource_map(entry_data.get("resource_deltas") or {}, field_label="resource_deltas")
        current_entry_delta = resource_deltas.get(resource_key, 0)
        campaign_snapshot = _campaign_doc_ref(client).get()
        if not campaign_snapshot.exists:
            raise FirestoreConflictError("La campaña ya no existe. Pulsa Refresh y reintenta.")
        campaign_data = campaign_snapshot.to_dict() or {}
        resource_totals = _parse_resource_map(
            campaign_data.get("resource_totals") or {},
            field_label="campaign.resource_totals",
        )
        current_total = resource_totals.get(resource_key, 0)
        return ResourceWriteResult(
            entry_ref=entry_ref,
            resource_key=resource_key,
            adjustment_delta=adjustment_delta,
            entry_delta_after=current_entry_delta,
            campaign_total_after=current_total,
            no_op=True,
        )

    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    campaign_doc_ref = _campaign_doc_ref(client)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> ResourceWriteResult:
        entry_snapshot = _get_doc_snapshot(txn, entry_doc_ref)
        if not entry_snapshot.exists:
            raise FirestoreTransitionInvalidError("La entry ya no existe.")
        campaign_snapshot = _get_doc_snapshot(txn, campaign_doc_ref)
        if not campaign_snapshot.exists:
            raise FirestoreConflictError("La campaña ya no existe. Pulsa Refresh y reintenta.")

        entry_data = entry_snapshot.to_dict() or {}
        campaign_data = campaign_snapshot.to_dict() or {}

        entry_deltas = _parse_resource_map(entry_data.get("resource_deltas") or {}, field_label="resource_deltas")
        campaign_totals = _parse_resource_map(
            campaign_data.get("resource_totals") or {},
            field_label="campaign.resource_totals",
        )

        current_entry_delta = entry_deltas.get(resource_key, 0)
        current_campaign_total = campaign_totals.get(resource_key, 0)

        next_entry_delta = current_entry_delta + adjustment_delta
        next_campaign_total = current_campaign_total + adjustment_delta

        if next_campaign_total < 0:
            raise FirestoreValidationError(
                f"La operación dejaría `campaign.resource_totals[{resource_key}]` en negativo."
            )

        if next_entry_delta == 0:
            entry_deltas.pop(resource_key, None)
        else:
            entry_deltas[resource_key] = next_entry_delta

        # Regla de #15: conservar 0 en campaign.resource_totals para claves materializadas
        campaign_totals[resource_key] = next_campaign_total

        txn.update(
            entry_doc_ref,
            {
                "resource_deltas": entry_deltas,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )
        txn.update(
            campaign_doc_ref,
            {
                "resource_totals": campaign_totals,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

        return ResourceWriteResult(
            entry_ref=entry_ref,
            resource_key=resource_key,
            adjustment_delta=adjustment_delta,
            entry_delta_after=next_entry_delta,
            campaign_total_after=next_campaign_total,
        )

    try:
        return _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover
        _map_firestore_write_exception(exc)


def replace_entry_resource_deltas(
    client: firestore.Client,
    *,
    entry_ref: EntryRef,
    target_resource_deltas: dict[str, int],
) -> ResourceBulkWriteResult:
    if not isinstance(target_resource_deltas, dict):
        raise FirestoreValidationError("`target_resource_deltas` debe ser un mapa.")

    parsed_target = _parse_resource_map(
        target_resource_deltas,
        field_label="target_resource_deltas",
    )
    for key in parsed_target:
        if key not in RESOURCE_KEYS:
            raise FirestoreValidationError(f"`target_resource_deltas` contiene `resource_key` no soportada: {key!r}.")

    # Regla de representación del entry: no persistir claves con delta 0.
    normalized_target = {
        key: value
        for key, value in parsed_target.items()
        if value != 0
    }

    entry_doc_ref = _entry_doc_ref(client, entry_ref)
    campaign_doc_ref = _campaign_doc_ref(client)
    transaction = client.transaction()

    @firestore.transactional
    def _run(txn: firestore.Transaction) -> ResourceBulkWriteResult:
        entry_snapshot = _get_doc_snapshot(txn, entry_doc_ref)
        if not entry_snapshot.exists:
            raise FirestoreTransitionInvalidError("La entry ya no existe.")
        campaign_snapshot = _get_doc_snapshot(txn, campaign_doc_ref)
        if not campaign_snapshot.exists:
            raise FirestoreConflictError("La campaña ya no existe. Pulsa Refresh y reintenta.")

        entry_data = entry_snapshot.to_dict() or {}
        campaign_data = campaign_snapshot.to_dict() or {}

        current_entry_deltas = _parse_resource_map(
            entry_data.get("resource_deltas") or {},
            field_label="resource_deltas",
        )
        campaign_totals = _parse_resource_map(
            campaign_data.get("resource_totals") or {},
            field_label="campaign.resource_totals",
        )

        # Preservar cualquier clave fuera del catálogo MVP para no borrar datos inesperados.
        current_entry_supported = {
            key: value for key, value in current_entry_deltas.items() if key in RESOURCE_KEYS
        }
        current_entry_unsupported = {
            key: value for key, value in current_entry_deltas.items() if key not in RESOURCE_KEYS
        }

        changed_keys = sorted(set(current_entry_supported) | set(normalized_target))
        if not changed_keys:
            return ResourceBulkWriteResult(
                entry_ref=entry_ref,
                changed_keys=(),
                entry_resource_deltas_after=dict(current_entry_deltas),
                campaign_totals_after_for_changed_keys={},
                no_op=True,
            )

        next_campaign_totals = dict(campaign_totals)
        changed_totals_after: dict[str, int] = {}

        for resource_key in changed_keys:
            current_entry_delta = current_entry_supported.get(resource_key, 0)
            target_entry_delta = normalized_target.get(resource_key, 0)
            delta_to_apply = target_entry_delta - current_entry_delta

            current_campaign_total = next_campaign_totals.get(resource_key, 0)
            next_campaign_total = current_campaign_total + delta_to_apply
            if next_campaign_total < 0:
                raise FirestoreValidationError(
                    f"La operación dejaría `campaign.resource_totals[{resource_key}]` en negativo."
                )

            changed_totals_after[resource_key] = next_campaign_total
            # Regla de #15: conservar 0 materializado si la clave fue tocada.
            next_campaign_totals[resource_key] = next_campaign_total

        next_entry_deltas = dict(current_entry_unsupported)
        for key, value in normalized_target.items():
            next_entry_deltas[key] = value

        if current_entry_deltas == next_entry_deltas:
            no_op = True
            no_op_totals = {
                key: next_campaign_totals.get(key, 0)
                for key in changed_keys
            }
            return ResourceBulkWriteResult(
                entry_ref=entry_ref,
                changed_keys=tuple(changed_keys),
                entry_resource_deltas_after=next_entry_deltas,
                campaign_totals_after_for_changed_keys=no_op_totals,
                no_op=no_op,
            )

        txn.update(
            entry_doc_ref,
            {
                "resource_deltas": next_entry_deltas,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )
        txn.update(
            campaign_doc_ref,
            {
                "resource_totals": next_campaign_totals,
                "updated_at_utc": firestore.SERVER_TIMESTAMP,
            },
        )

        return ResourceBulkWriteResult(
            entry_ref=entry_ref,
            changed_keys=tuple(changed_keys),
            entry_resource_deltas_after=next_entry_deltas,
            campaign_totals_after_for_changed_keys=changed_totals_after,
            no_op=False,
        )

    try:
        return _run(transaction)
    except (FirestoreWriteError, FirestoreConflictError, FirestoreTransitionInvalidError, FirestoreValidationError):
        raise
    except Exception as exc:  # pragma: no cover
        _map_firestore_write_exception(exc)


def _campaign_doc_ref(client: firestore.Client) -> Any:
    return client.collection("campaigns").document(CAMPAIGN_ID)


def _entry_doc_ref(client: firestore.Client, entry_ref: EntryRef) -> Any:
    season_type = _resolve_season_type_for_week(
        year_number=entry_ref.year_number,
        week_number=entry_ref.week_number,
    )
    return (
        _campaign_doc_ref(client)
        .collection("years")
        .document(str(entry_ref.year_number))
        .collection("seasons")
        .document(season_type)
        .collection("weeks")
        .document(str(entry_ref.week_number))
        .collection("entries")
        .document(entry_ref.entry_id)
    )


def _resolve_season_type_for_week(*, year_number: int, week_number: int) -> str:
    local_week = week_number - ((year_number - 1) * WEEKS_PER_YEAR)
    if not 1 <= local_week <= WEEKS_PER_YEAR:
        raise FirestoreValidationError(
            f"Week {week_number} no pertenece al año {year_number} según el template temporal MVP."
        )
    return "summer" if local_week <= 10 else "winter"


def _parse_resource_map(raw_map: Any, *, field_label: str) -> dict[str, int]:
    if not isinstance(raw_map, dict):
        raise FirestoreValidationError(f"`{field_label}` debe ser un mapa.")
    parsed: dict[str, int] = {}
    for key, value in raw_map.items():
        if not isinstance(key, str):
            raise FirestoreValidationError(f"`{field_label}` contiene una clave no string.")
        if isinstance(value, bool) or not isinstance(value, int):
            raise FirestoreValidationError(f"`{field_label}[{key}]` debe ser entero.")
        parsed[key] = value
    return parsed


def _get_doc_snapshot(txn: firestore.Transaction, doc_ref: Any) -> Any:
    snapshot_or_iter = txn.get(doc_ref)
    if hasattr(snapshot_or_iter, "exists"):
        return snapshot_or_iter
    snapshots = list(snapshot_or_iter)
    if not snapshots:
        raise FirestoreTransitionInvalidError("El documento ya no existe.")
    return snapshots[0]


def _map_firestore_write_exception(exc: Exception) -> None:
    if isinstance(exc, FirestoreWriteError):
        raise exc
    if isinstance(exc, Aborted):
        raise FirestoreConflictError(
            "La operación de escritura entró en conflicto. Pulsa Refresh y reintenta."
        ) from exc
    raise FirestoreWriteError(f"Error de escritura en Firestore: {exc}") from exc


