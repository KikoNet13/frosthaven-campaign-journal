from __future__ import annotations

import flet as ft

from frosthaven_campaign_journal.ui.app_root import build_app_root
from examples.app3 import AppExample


APP_TITLE = "Frosthaven Campaign Journal"


def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.render(build_app_root, page)


def main_example(page: ft.Page):
    page.render(AppExample)


def run() -> None:
    ft.run(main)
    # ft.run(main_example)


if __name__ == "__main__":
    run()
