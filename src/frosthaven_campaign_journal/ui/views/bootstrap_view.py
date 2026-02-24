from __future__ import annotations

import flet as ft


def build_bootstrap_view(env_name: str) -> ft.Control:
    return ft.Container(
        expand=True,
        padding=ft.padding.all(24),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Frosthaven Campaign Journal",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text("Bootstrap de app Flet listo"),
                ft.Text(f"Entorno: {env_name}"),
                ft.Text(
                    "El layout de pantalla principal se implementa en la issue #52.",
                    italic=True,
                    color=ft.Colors.GREY_700,
                ),
            ],
        ),
    )
