from __future__ import annotations

from enum import Enum

NEUTRAL_WHITE = "#FFFFFF"
NEUTRAL_BLACK = "#000000"


class PaletteColor(str, Enum):
    PUNCH_RED = "#E63946"
    HONEYDEW = "#F1FAEE"
    FROSTED_BLUE = "#A8DADC"
    CERULEAN = "#457B9D"
    OXFORD_NAVY = "#1D3557"


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Hex color must have 6 digits, got {value!r}.")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    red, green, blue = rgb
    return f"#{red:02X}{green:02X}{blue:02X}"


def _blend(base: str, target: str, ratio: float) -> str:
    ratio = max(0.0, min(1.0, ratio))
    base_rgb = _hex_to_rgb(base)
    target_rgb = _hex_to_rgb(target)
    mixed = (
        round(base_rgb[0] + (target_rgb[0] - base_rgb[0]) * ratio),
        round(base_rgb[1] + (target_rgb[1] - base_rgb[1]) * ratio),
        round(base_rgb[2] + (target_rgb[2] - base_rgb[2]) * ratio),
    )
    return _rgb_to_hex(mixed)


class SemanticColor(str, Enum):
    ACCENT_BG = PaletteColor.PUNCH_RED.value
    ACCENT_TEXT = NEUTRAL_WHITE
    ACCENT_BG_DISABLED = _blend(PaletteColor.PUNCH_RED.value, NEUTRAL_WHITE, 0.58)

    BOTTOM_BAR_BG = PaletteColor.CERULEAN.value
    TOP_BAR_BG = BOTTOM_BAR_BG
    TOP_BAR_TEXT = NEUTRAL_WHITE
    TOP_NAV_BUTTON_BG = ACCENT_BG
    TOP_NAV_BUTTON_DISABLED_BG = ACCENT_BG_DISABLED
    TOP_NAV_BUTTON_TEXT_DISABLED = _blend(PaletteColor.PUNCH_RED.value, PaletteColor.OXFORD_NAVY.value, 0.55)

    WEEK_TILE_BG = _blend(PaletteColor.FROSTED_BLUE.value, NEUTRAL_WHITE, 0.36)
    WEEK_TILE_CLOSED_BG = _blend(PaletteColor.OXFORD_NAVY.value, PaletteColor.FROSTED_BLUE.value, 0.70)
    WEEK_TILE_CLOSED_TEXT = _blend(PaletteColor.OXFORD_NAVY.value, NEUTRAL_WHITE, 0.50)
    WEEK_TILE_SELECTED_BG = ACCENT_BG
    WEEK_TILE_SELECTED_BORDER = _blend(PaletteColor.PUNCH_RED.value, PaletteColor.OXFORD_NAVY.value, 0.18)
    WEEK_TILE_SELECTED_TEXT = ACCENT_TEXT
    WEEK_BLOCK_SUMMER_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.45)
    WEEK_BLOCK_WINTER_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.45)
    WEEK_BLOCK_BORDER = _blend(PaletteColor.CERULEAN.value, PaletteColor.OXFORD_NAVY.value, 0.25)
    SEASON_LABEL_BG = ACCENT_BG
    SEASON_LABEL_BORDER = _blend(PaletteColor.PUNCH_RED.value, PaletteColor.OXFORD_NAVY.value, 0.18)
    SEASON_LABEL_TEXT = ACCENT_TEXT

    ENTRY_TAB_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.60)
    ENTRY_TAB_SELECTED_UNDERLINE = PaletteColor.CERULEAN.value

    CENTER_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.45)

    PANEL_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.62)
    PANEL_BORDER = _blend(PaletteColor.CERULEAN.value, PaletteColor.HONEYDEW.value, 0.50)
    PANEL_INNER_BG = PaletteColor.HONEYDEW.value
    PANEL_INNER_BORDER = _blend(PaletteColor.CERULEAN.value, PaletteColor.HONEYDEW.value, 0.62)

    STATUS_GROUP_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.45)
    STATUS_GROUP_BORDER = _blend(PaletteColor.CERULEAN.value, PaletteColor.OXFORD_NAVY.value, 0.25)
    STATUS_LABEL_BG = ACCENT_BG
    STATUS_LABEL_BORDER = SEASON_LABEL_BORDER
    STATUS_LABEL_TEXT = ACCENT_TEXT
    STATUS_TEXT_SECONDARY = _blend(NEUTRAL_WHITE, PaletteColor.FROSTED_BLUE.value, 0.28)
    STATUS_TEXT_TERTIARY = _blend(NEUTRAL_WHITE, PaletteColor.FROSTED_BLUE.value, 0.40)
    RESOURCE_TOTAL_VALUE = NEUTRAL_WHITE

    TEXT_PRIMARY = _blend(PaletteColor.OXFORD_NAVY.value, NEUTRAL_BLACK, 0.18)
    TEXT_HEADING = _blend(PaletteColor.CERULEAN.value, PaletteColor.OXFORD_NAVY.value, 0.42)
    TEXT_MUTED = _blend(PaletteColor.OXFORD_NAVY.value, PaletteColor.HONEYDEW.value, 0.40)
    TEXT_DIMMED = _blend(PaletteColor.OXFORD_NAVY.value, PaletteColor.HONEYDEW.value, 0.55)
    TEXT_INVERSE = NEUTRAL_WHITE

    ERROR_BG = _blend(PaletteColor.PUNCH_RED.value, PaletteColor.HONEYDEW.value, 0.82)
    ERROR_BORDER = _blend(PaletteColor.PUNCH_RED.value, PaletteColor.OXFORD_NAVY.value, 0.18)
    ERROR_TEXT = _blend(PaletteColor.PUNCH_RED.value, PaletteColor.OXFORD_NAVY.value, 0.20)

    WARNING_BG = _blend(PaletteColor.CERULEAN.value, PaletteColor.HONEYDEW.value, 0.78)
    WARNING_BORDER = _blend(PaletteColor.CERULEAN.value, PaletteColor.OXFORD_NAVY.value, 0.18)
    WARNING_TEXT = PaletteColor.OXFORD_NAVY.value

    INFO_BG = _blend(PaletteColor.FROSTED_BLUE.value, PaletteColor.HONEYDEW.value, 0.48)
    INFO_BORDER = _blend(PaletteColor.CERULEAN.value, PaletteColor.HONEYDEW.value, 0.35)
    INFO_TEXT = PaletteColor.OXFORD_NAVY.value

    DELTA_POSITIVE = PaletteColor.CERULEAN.value
    DELTA_NEGATIVE = PaletteColor.PUNCH_RED.value

    VICTORY_ICON = PaletteColor.CERULEAN.value
    DEFEAT_ICON = PaletteColor.PUNCH_RED.value
    DESTRUCTIVE_ICON = PaletteColor.PUNCH_RED.value


COLOR_BOTTOM_BAR_BG = SemanticColor.BOTTOM_BAR_BG.value
COLOR_ACCENT_BG = SemanticColor.ACCENT_BG.value
COLOR_ACCENT_BG_DISABLED = SemanticColor.ACCENT_BG_DISABLED.value
COLOR_ACCENT_TEXT = SemanticColor.ACCENT_TEXT.value
COLOR_TOP_BAR_BG = COLOR_BOTTOM_BAR_BG
COLOR_TOP_BAR_TEXT = SemanticColor.TOP_BAR_TEXT.value
COLOR_TOP_NAV_BUTTON_BG = SemanticColor.TOP_NAV_BUTTON_BG.value
COLOR_TOP_NAV_BUTTON_DISABLED_BG = SemanticColor.TOP_NAV_BUTTON_DISABLED_BG.value
COLOR_TOP_NAV_BUTTON_TEXT_DISABLED = SemanticColor.TOP_NAV_BUTTON_TEXT_DISABLED.value
COLOR_WEEK_TILE_BG = SemanticColor.WEEK_TILE_BG.value
COLOR_WEEK_TILE_CLOSED_BG = SemanticColor.WEEK_TILE_CLOSED_BG.value
COLOR_WEEK_TILE_CLOSED_TEXT = SemanticColor.WEEK_TILE_CLOSED_TEXT.value
COLOR_WEEK_TILE_SELECTED_BG = SemanticColor.WEEK_TILE_SELECTED_BG.value
COLOR_WEEK_TILE_SELECTED_BORDER = SemanticColor.WEEK_TILE_SELECTED_BORDER.value
COLOR_WEEK_TILE_SELECTED_TEXT = SemanticColor.WEEK_TILE_SELECTED_TEXT.value
COLOR_WEEK_BLOCK_SUMMER_BG = SemanticColor.WEEK_BLOCK_SUMMER_BG.value
COLOR_WEEK_BLOCK_WINTER_BG = SemanticColor.WEEK_BLOCK_WINTER_BG.value
COLOR_WEEK_BLOCK_BORDER = SemanticColor.WEEK_BLOCK_BORDER.value
COLOR_SEASON_LABEL_BG = SemanticColor.SEASON_LABEL_BG.value
COLOR_SEASON_LABEL_BORDER = SemanticColor.SEASON_LABEL_BORDER.value
COLOR_SEASON_LABEL_TEXT = SemanticColor.SEASON_LABEL_TEXT.value
COLOR_ENTRY_TABS_BG = SemanticColor.ENTRY_TAB_BG.value
COLOR_ENTRY_TAB_SELECTED_UNDERLINE = SemanticColor.ENTRY_TAB_SELECTED_UNDERLINE.value
COLOR_CENTER_BG = SemanticColor.CENTER_BG.value
COLOR_PANEL_BG = SemanticColor.PANEL_BG.value
COLOR_PANEL_BORDER = SemanticColor.PANEL_BORDER.value
COLOR_PANEL_INNER_BG = SemanticColor.PANEL_INNER_BG.value
COLOR_PANEL_INNER_BORDER = SemanticColor.PANEL_INNER_BORDER.value
COLOR_STATUS_GROUP_BG = SemanticColor.STATUS_GROUP_BG.value
COLOR_STATUS_GROUP_BORDER = SemanticColor.STATUS_GROUP_BORDER.value
COLOR_STATUS_LABEL_BG = SemanticColor.STATUS_LABEL_BG.value
COLOR_STATUS_LABEL_BORDER = SemanticColor.STATUS_LABEL_BORDER.value
COLOR_STATUS_LABEL_TEXT = SemanticColor.STATUS_LABEL_TEXT.value
COLOR_STATUS_TEXT_SECONDARY = SemanticColor.STATUS_TEXT_SECONDARY.value
COLOR_STATUS_TEXT_TERTIARY = SemanticColor.STATUS_TEXT_TERTIARY.value
COLOR_RESOURCE_TOTAL_VALUE = SemanticColor.RESOURCE_TOTAL_VALUE.value
COLOR_TEXT_PRIMARY = SemanticColor.TEXT_PRIMARY.value
COLOR_TEXT_HEADING = SemanticColor.TEXT_HEADING.value
COLOR_TEXT_MUTED = SemanticColor.TEXT_MUTED.value
COLOR_TEXT_DIMMED = SemanticColor.TEXT_DIMMED.value
COLOR_WHITE = SemanticColor.TEXT_INVERSE.value
COLOR_ERROR_TEXT = SemanticColor.ERROR_TEXT.value
COLOR_BANNER_ERROR_BG = SemanticColor.ERROR_BG.value
COLOR_BANNER_ERROR_BORDER = SemanticColor.ERROR_BORDER.value
COLOR_BANNER_ERROR_TEXT = SemanticColor.ERROR_TEXT.value
COLOR_BANNER_WARNING_BG = SemanticColor.WARNING_BG.value
COLOR_BANNER_WARNING_BORDER = SemanticColor.WARNING_BORDER.value
COLOR_BANNER_WARNING_TEXT = SemanticColor.WARNING_TEXT.value
COLOR_BANNER_INFO_BG = SemanticColor.INFO_BG.value
COLOR_BANNER_INFO_BORDER = SemanticColor.INFO_BORDER.value
COLOR_BANNER_INFO_TEXT = SemanticColor.INFO_TEXT.value
COLOR_DELTA_POSITIVE = SemanticColor.DELTA_POSITIVE.value
COLOR_DELTA_NEGATIVE = SemanticColor.DELTA_NEGATIVE.value
COLOR_VICTORY_ICON = SemanticColor.VICTORY_ICON.value
COLOR_DEFEAT_ICON = SemanticColor.DEFEAT_ICON.value
COLOR_DESTRUCTIVE_ICON = SemanticColor.DESTRUCTIVE_ICON.value
