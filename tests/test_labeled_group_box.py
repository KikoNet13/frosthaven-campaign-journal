from __future__ import annotations

import unittest

import flet as ft

from frosthaven_campaign_journal.ui.common.components import LabeledGroupBox


class LabeledGroupBoxTests(unittest.TestCase):
    def test_labeled_group_box_is_isolated_and_preserves_content_on_update(self) -> None:
        content = ft.Text("contenido")
        box = LabeledGroupBox(
            label="Caja",
            content=content,
            bgcolor="#efefef",
            border_color="#999999",
            label_bgcolor="#ffffff",
            label_border_color="#999999",
            label_text_color="#111111",
        )

        self.assertTrue(box.is_isolated())
        self.assertIs(content, box.controls[0].content)

        box.label = "Caja actualizada"
        box.before_update()

        self.assertIs(content, box.controls[0].content)


if __name__ == "__main__":
    unittest.main()
