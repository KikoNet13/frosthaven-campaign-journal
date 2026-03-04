from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.resource_catalog import ResourceCatalogItem
from frosthaven_campaign_journal.ui.common.components import LabeledGroupBox
from frosthaven_campaign_journal.ui.common.resources import ResourceTotalRow, ResourceUiGroup, iter_resource_ui_groups
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_RESOURCE_TOTAL_VALUE,
    COLOR_STATUS_GROUP_BG,
    COLOR_STATUS_GROUP_BORDER,
    COLOR_STATUS_LABEL_BG,
    COLOR_STATUS_LABEL_BORDER,
    COLOR_STATUS_LABEL_TEXT,
    COLOR_STATUS_TEXT_SECONDARY,
    COLOR_STATUS_TEXT_TERTIARY,
    COLOR_WHITE,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData


def build_status_bar(data: MainShellViewData) -> ft.Control:
    active_text, active_detail_text = _active_status_texts(data)
    viewer_text = (
        f"Viendo: {data.viewer_entry.label} (S{data.viewer_entry.ref.week_number})"
        if data.viewer_entry is not None
        else "Sin entrada en visor"
    )

    return ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                content=ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10,
                    controls=[
                        _build_resource_group_box(data, group)
                        for group in iter_resource_ui_groups()
                    ],
                ),
            ),
            ft.Container(
                width=360,
                content=ft.Column(
                    spacing=1,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Text(
                            active_text,
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_WHITE,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text(
                            active_detail_text or viewer_text,
                            size=12,
                            color=COLOR_STATUS_TEXT_SECONDARY,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                        ft.Text(
                            f"{viewer_text} · env={data.env_name}",
                            size=11,
                            color=COLOR_STATUS_TEXT_TERTIARY,
                            text_align=ft.TextAlign.RIGHT,
                        ),
                    ],
                ),
            ),
        ],
    )


def _build_resource_group_box(data: MainShellViewData, group: ResourceUiGroup) -> ft.Control:
    column_controls: list[ft.Control] = []
    for group_column in group.columns:
        column_controls.append(
            ft.Container(
                expand=1,
                content=ft.Column(
                    spacing=4,
                    controls=[
                        _build_resource_total_row(
                            item=item,
                            resource_totals=data.campaign_resource_totals,
                        )
                        for item in group_column
                    ],
                ),
            )
        )

    columns_control: ft.Control
    if len(column_controls) == 1:
        columns_control = column_controls[0]
    else:
        columns_control = ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=column_controls,
        )

    return LabeledGroupBox(
        label=group.label_es,
        width=(462 if len(group.columns) > 1 else 235),
        content=columns_control,
        bgcolor=COLOR_STATUS_GROUP_BG,
        border_color=COLOR_STATUS_GROUP_BORDER,
        label_bgcolor=COLOR_STATUS_LABEL_BG,
        label_border_color=COLOR_STATUS_LABEL_BORDER,
        label_text_color=COLOR_STATUS_LABEL_TEXT,
        padding=ft.Padding(left=8, top=10, right=8, bottom=6),
    )


def _build_resource_total_row(
    *,
    item: ResourceCatalogItem,
    resource_totals: dict[str, int] | None,
) -> ft.Control:
    return ResourceTotalRow(
        icon_src=item.icon_src,
        label_es=item.label_es,
        total_text=_format_saved_total(resource_totals, item.key),
        text_color=COLOR_WHITE,
        value_color=COLOR_RESOURCE_TOTAL_VALUE,
        label_width=136,
        value_width=44,
    )


def _format_saved_total(resource_totals: dict[str, int] | None, resource_key: str) -> str:
    if resource_totals is None:
        return "N/D"
    return str(resource_totals.get(resource_key, 0))


def _active_status_texts(data: MainShellViewData) -> tuple[str, str]:
    if data.active_status_error_message:
        return ("Estado activo no disponible", data.active_status_error_message)
    if data.active_entry_ref is None:
        return ("Sin sesión activa", "")
    label = data.active_entry_label or f"Entrada {data.active_entry_ref.entry_id}"
    if data.viewer_entry is not None and data.viewer_entry.ref == data.active_entry_ref:
        return (f"Con sesión activa: {label} · aquí", "")
    return (f"Con sesión activa: {label} · en otra entrada", "")
