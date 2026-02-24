from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BootstrapSelectionState:
    selected_year: int | None = None
    selected_week: int | None = None
    selected_entry: str | None = None
    current_week_marker: int | None = None
    active_entry_id: str | None = None
