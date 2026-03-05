from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.resource_catalog import ResourceCatalogItem
from frosthaven_campaign_journal.ui.common.components import LabeledGroupBox
from frosthaven_campaign_journal.ui.common.resources import ResourceTotalRow, ResourceUiGroup, iter_resource_ui_groups
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_STATUS_GROUP_BG,
    COLOR_STATUS_GROUP_BORDER,
    COLOR_STATUS_LABEL_BG,
    COLOR_STATUS_LABEL_BORDER,
    COLOR_STATUS_LABEL_TEXT,
    COLOR_TEXT_PRIMARY,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData


def build_status_bar(data: MainShellViewData) -> ft.Control:
    return ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                content=ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=8,
                    controls=[
                        _build_resource_group_box(data, group)
                        for group in iter_resource_ui_groups()
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
                    spacing=3,
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
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=column_controls,
        )

    return LabeledGroupBox(
        label=group.label_es,
        width=(430 if len(group.columns) > 1 else 228),
        content=columns_control,
        bgcolor=COLOR_STATUS_GROUP_BG,
        border_color=COLOR_STATUS_GROUP_BORDER,
        label_bgcolor=COLOR_STATUS_LABEL_BG,
        label_border_color=COLOR_STATUS_LABEL_BORDER,
        label_text_color=COLOR_STATUS_LABEL_TEXT,
        padding=ft.Padding(left=8, top=9, right=8, bottom=4),
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
        text_color=COLOR_TEXT_PRIMARY,
        value_color=COLOR_TEXT_PRIMARY,
        icon_color=COLOR_TEXT_PRIMARY,
        label_size=13,
        value_size=14,
        label_width=116,
        value_width=32,
    )


def _format_saved_total(resource_totals: dict[str, int] | None, resource_key: str) -> str:
    if resource_totals is None:
        return "N/D"
    return str(resource_totals.get(resource_key, 0))
