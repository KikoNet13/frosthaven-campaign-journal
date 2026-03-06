from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.resource_catalog import ResourceCatalogItem
from frosthaven_campaign_journal.ui.common.components import LabeledGroupBox
from frosthaven_campaign_journal.ui.common.resources import (
    ResourceTotalRow,
    ResourceUiGroup,
    iter_resource_ui_groups,
)
from frosthaven_campaign_journal.ui.common.theme.colors import (
    COLOR_STATUS_GROUP_BG,
    COLOR_STATUS_GROUP_BORDER,
    COLOR_STATUS_LABEL_BG,
    COLOR_STATUS_LABEL_BORDER,
    COLOR_STATUS_LABEL_TEXT,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
)
from frosthaven_campaign_journal.ui.main_shell.model import MainShellViewData
from frosthaven_campaign_journal.ui.main_shell.view.session_timing import (
    build_active_session_subtitle,
    build_session_duration_text,
)


def build_status_bar(data: MainShellViewData) -> ft.Control:
    controls: list[ft.Control] = [
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
    ]

    active_session_box = _build_active_session_box(data)
    if active_session_box is not None:
        controls.append(active_session_box)

    return ft.Row(
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=controls,
    )


def _build_resource_group_box(
    data: MainShellViewData, group: ResourceUiGroup
) -> ft.Control:
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


def _format_saved_total(
    resource_totals: dict[str, int] | None, resource_key: str
) -> str:
    if resource_totals is None:
        return "N/D"
    return str(resource_totals.get(resource_key, 0))


def _build_active_session_box(data: MainShellViewData) -> ft.Control | None:
    if data.active_session_started_at_utc is None:
        return None

    active_week_number = (
        data.active_entry_ref.week_number if data.active_entry_ref is not None else None
    )
    subtitle = build_active_session_subtitle(
        entry_label=data.active_entry_label,
        week_number=active_week_number,
    )

    return LabeledGroupBox(
        label="Sesión actual",
        width=200,
        bgcolor=COLOR_STATUS_GROUP_BG,
        border_color=COLOR_STATUS_GROUP_BORDER,
        label_bgcolor=COLOR_STATUS_LABEL_BG,
        label_border_color=COLOR_STATUS_LABEL_BORDER,
        label_text_color=COLOR_STATUS_LABEL_TEXT,
        padding=ft.Padding(left=12, top=10, right=12, bottom=10),
        content=ft.Column(
            spacing=2,
            controls=[
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            ft.Icons.TIMER_OUTLINED,
                            size=20,
                            color=COLOR_TEXT_PRIMARY,
                        ),
                        build_session_duration_text(
                            started_at_utc=data.active_session_started_at_utc,
                            size=26,
                            weight=ft.FontWeight.W_700,
                            color=COLOR_TEXT_PRIMARY,
                        ),
                    ],
                ),
                ft.Text(
                    subtitle,
                    size=11,
                    color=COLOR_TEXT_MUTED,
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ],
        ),
    )
