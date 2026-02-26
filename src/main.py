from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.app_root import build_app_root


APP_TITLE = "Frosthaven Campaign Journal"


def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.padding = 0
    page.scroll = ft.ScrollMode.HIDDEN
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.add(build_app_root(page))


def run() -> None:
    ft.run(main)


if __name__ == "__main__":
    run()
