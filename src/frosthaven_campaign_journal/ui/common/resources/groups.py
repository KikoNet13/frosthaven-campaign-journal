from __future__ import annotations

from dataclasses import dataclass

from frosthaven_campaign_journal.resource_catalog import RESOURCE_ITEMS_BY_KEY, ResourceCatalogItem


@dataclass(frozen=True)
class ResourceUiGroup:
    key: str
    label_es: str
    columns: tuple[tuple[ResourceCatalogItem, ...], ...]


_RESOURCE_UI_GROUP_DEFS: tuple[tuple[str, str, tuple[tuple[str, ...], ...]], ...] = (
    ("materials", "Materiales", (("lumber", "metal", "hide"),)),
    (
        "plants",
        "Plantas",
        (
            ("arrowvine", "axenut", "corpsecap"),
            ("flamefruit", "rockroot", "snowthistle"),
        ),
    ),
    ("others", "Otros", (("inspiration", "morale", "soldiers"),)),
)


def iter_resource_ui_groups() -> tuple[ResourceUiGroup, ...]:
    groups: list[ResourceUiGroup] = []
    for group_key, group_label, group_columns in _RESOURCE_UI_GROUP_DEFS:
        columns = tuple(
            tuple(RESOURCE_ITEMS_BY_KEY[resource_key] for resource_key in column_keys)
            for column_keys in group_columns
        )
        groups.append(
            ResourceUiGroup(
                key=group_key,
                label_es=group_label,
                columns=columns,
            )
        )
    return tuple(groups)
