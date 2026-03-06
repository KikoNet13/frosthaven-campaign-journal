from __future__ import annotations

import unittest

from tests.main_shell_test_support import install_data_stub

install_data_stub()

from frosthaven_campaign_journal.ui.main_shell.state.shell_state import MainShellState


class MainShellFeedbackEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = MainShellState()
        self.state.notify = lambda: None

    def test_emit_info_toast_repeats_same_message_with_new_event_id(self) -> None:
        self.state._emit_info_toast("Cambios guardados.")
        first_message = self.state.toast_state.message
        first_event_id = self.state.toast_state.event_id

        self.state._emit_info_toast("Cambios guardados.")

        self.assertEqual(self.state.toast_state.message, first_message)
        self.assertIsNotNone(first_event_id)
        self.assertIsNotNone(self.state.toast_state.event_id)
        self.assertNotEqual(self.state.toast_state.event_id, first_event_id)

    def test_set_confirmation_repeats_same_payload_with_new_event_id(self) -> None:
        self.state._set_confirmation(
            key="week_close",
            title="Cerrar semana",
            body="¿Quieres continuar?",
            confirm_label="Cerrar",
            payload=(1, 2),
        )
        first_event_id = self.state.confirmation_state.event_id

        self.state._set_confirmation(
            key="week_close",
            title="Cerrar semana",
            body="¿Quieres continuar?",
            confirm_label="Cerrar",
            payload=(1, 2),
        )

        self.assertIsNotNone(first_event_id)
        self.assertIsNotNone(self.state.confirmation_state.event_id)
        self.assertNotEqual(self.state.confirmation_state.event_id, first_event_id)

    def test_cancel_pending_action_clears_confirmation_and_pending_action(self) -> None:
        self.state._queue_pending_context_action(lambda: None, action_label="refrescar")
        self.state._set_confirmation(
            key="week_close",
            title="Cerrar semana",
            body="¿Quieres continuar?",
            confirm_label="Cerrar",
            payload=(1, 2),
        )

        self.state.on_cancel_pending_action()

        self.assertIsNone(self.state.confirmation_state.key)
        self.assertIsNone(self.state.confirmation_state.event_id)
        self.assertIsNone(self.state._pending_context_action)
        self.assertIsNone(self.state._pending_context_action_label)

    def test_confirm_pending_action_clears_confirmation_and_runs_pending_action(self) -> None:
        ran: list[bool] = []
        self.state.entry_panel_state.resource_draft_dirty = True
        self.state._queue_pending_context_action(lambda: ran.append(True), action_label="refrescar")
        self.state._set_confirmation(
            key="discard_resource_draft_context_change",
            title="Cambios de recursos sin guardar",
            body="¿Quieres descartar y continuar?",
            confirm_label="Descartar y continuar",
            payload="refrescar",
        )

        self.state.on_confirm_pending_action()

        self.assertEqual(ran, [True])
        self.assertIsNone(self.state.confirmation_state.key)
        self.assertIsNone(self.state.confirmation_state.event_id)
        self.assertIsNone(self.state._pending_context_action)
        self.assertIsNone(self.state._pending_context_action_label)
        self.assertEqual(
            self.state.toast_state.message,
            "Cambios de recursos sin guardar descartados al cambiar de contexto.",
        )
        self.assertIsNotNone(self.state.toast_state.event_id)


if __name__ == "__main__":
    unittest.main()