from __future__ import annotations

from collections.abc import Callable

import flet as ft


def build_confirm_dialog(
    *,
    title: str,
    body: str,
    confirm_label: str,
    on_confirm: Callable[[ft.ControlEvent], None],
    on_cancel: Callable[[ft.ControlEvent], None],
) -> ft.AlertDialog:
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(body),
        actions=[
            ft.TextButton("Cancelar", on_click=on_cancel),
            ft.FilledButton(confirm_label, on_click=on_confirm),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


def build_resource_draft_leave_confirm_dialog(
    *,
    action_label: str,
    on_cancel: Callable[[ft.ControlEvent], None],
    on_discard: Callable[[ft.ControlEvent], None],
    on_save: Callable[[ft.ControlEvent], None],
    save_disabled: bool,
) -> ft.AlertDialog:
    body = (
        f"Hay cambios locales de recursos sin guardar.\n\n"
        f"¿Qué quieres hacer antes de {action_label}?"
    )
    return ft.AlertDialog(
        modal=True,
        title=ft.Text("Cambios locales sin guardar"),
        content=ft.Text(body),
        actions=[
            ft.TextButton("Cancelar", on_click=on_cancel),
            ft.OutlinedButton("Descartar cambios", on_click=on_discard, disabled=save_disabled),
            ft.FilledButton("Guardar y continuar", on_click=on_save, disabled=save_disabled),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

