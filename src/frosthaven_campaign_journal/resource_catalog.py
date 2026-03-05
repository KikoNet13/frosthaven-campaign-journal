from __future__ import annotations

from dataclasses import dataclass


RESOURCE_GROUPS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("materials", "Materiales", ("lumber", "metal", "hide")),
    ("plants_a", "Plantas A", ("arrowvine", "axenut", "corpsecap")),
    ("plants_b", "Plantas B", ("flamefruit", "rockroot", "snowthistle")),
    ("others", "Otros", ("inspiration", "morale", "soldiers")),
)

RESOURCE_KEYS: tuple[str, ...] = tuple(
    resource_key
    for _group_key, _group_label, resource_keys in RESOURCE_GROUPS
    for resource_key in resource_keys
)

RESOURCE_LABELS_ES: dict[str, str] = {
    "lumber": "Madera",
    "metal": "Metal",
    "hide": "Piel",
    "arrowvine": "Enredaflecha",
    "axenut": "Bellota filosa",
    "corpsecap": "Gorro de muerto",
    "flamefruit": "Pitallama",
    "rockroot": "Raíz de roca",
    "snowthistle": "Cardo de nieve",
    "inspiration": "Inspiración",
    "morale": "Moral",
    "soldiers": "Soldados",
}

RESOURCE_ICON_FILENAMES: dict[str, str] = {
    "lumber": "fh-lumber-bw-icon.png",
    "metal": "fh-metal-bw-icon.png",
    "hide": "fh-hide-bw-icon.png",
    "arrowvine": "fh-arrowvine-bw-icon.png",
    "axenut": "fh-axenut-bw-icon.png",
    "corpsecap": "fh-corpsecap-bw-icon.png",
    "flamefruit": "fh-flamefruit-bw-icon.png",
    "rockroot": "fh-rockroot-bw-icon.png",
    "snowthistle": "fh-snowthistle-bw-icon.png",
    "inspiration": "fh-inspiration-bw-icon.png",
    "morale": "fh-morale-bw-icon.png",
    "soldiers": "fh-soldiers-bw-icon.png",
}

RESOURCE_ICON_ASSET_PREFIX = "resource-icons"


@dataclass(frozen=True)
class ResourceCatalogItem:
    key: str
    label_es: str
    icon_src: str
    group_key: str
    group_label: str
    order_index: int


def _build_resource_items() -> dict[str, ResourceCatalogItem]:
    items: dict[str, ResourceCatalogItem] = {}
    order_index = 0
    for group_key, group_label, resource_keys in RESOURCE_GROUPS:
        for resource_key in resource_keys:
            label = RESOURCE_LABELS_ES.get(resource_key)
            if label is None:
                raise ValueError(f"Falta etiqueta en castellano para resource_key={resource_key!r}.")
            filename = RESOURCE_ICON_FILENAMES.get(resource_key)
            if filename is None:
                raise ValueError(f"Falta icono para resource_key={resource_key!r}.")
            items[resource_key] = ResourceCatalogItem(
                key=resource_key,
                label_es=label,
                icon_src=f"{RESOURCE_ICON_ASSET_PREFIX}/{filename}",
                group_key=group_key,
                group_label=group_label,
                order_index=order_index,
            )
            order_index += 1
    return items


RESOURCE_ITEMS_BY_KEY: dict[str, ResourceCatalogItem] = _build_resource_items()


def iter_resource_groups_with_items() -> tuple[tuple[str, str, tuple[ResourceCatalogItem, ...]], ...]:
    return tuple(
        (
            group_key,
            group_label,
            tuple(RESOURCE_ITEMS_BY_KEY[resource_key] for resource_key in resource_keys),
        )
        for group_key, group_label, resource_keys in RESOURCE_GROUPS
    )
