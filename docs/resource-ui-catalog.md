# Catálogo UI de Recursos (MVP)

## Metadatos

- `doc_id`: DOC-RESOURCE-UI-CATALOG
- `purpose`: Definir catálogo UI único de recursos (claves internas, etiquetas, grupos, orden e iconos) para edición de deltas y visualización de totales.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-19

## Objetivo

Establecer una referencia única para:

- orden canónico de recursos del MVP;
- mapeo `resource_key` (EN) -> etiqueta visible en castellano;
- agrupación visual en la app;
- ubicación oficial y convención de nombres de iconos.

Este documento alinea implementación UI con el glosario de dominio vigente (`docs/domain-glossary.md`), que define 12 `resource_key`.

## Orden canónico y agrupación

1. Otros:
   - `inspiration`
   - `morale`
   - `soldiers`
1. Materiales:
   - `lumber`
   - `metal`
   - `hide`
1. Plantas A:
   - `arrowvine`
   - `axenut`
   - `corpsecap`
1. Plantas B:
   - `flamefruit`
   - `rockroot`
   - `snowthistle`

## Mapeo UI (EN -> ES) y assets

Nota de orden visual activo en runtime: `Otros -> Materiales -> Plantas` (las
dos columnas de plantas se renderizan como un único bloque `Plantas`).

| resource_key | etiqueta_ui_es | grupo_ui | icon_filename_png |
| --- | --- | --- | --- |
| `lumber` | Madera | Materiales | `fh-lumber-bw-icon.png` |
| `metal` | Metal | Materiales | `fh-metal-bw-icon.png` |
| `hide` | Piel | Materiales | `fh-hide-bw-icon.png` |
| `arrowvine` | Enredaflecha | Plantas A | `fh-arrowvine-bw-icon.png` |
| `axenut` | Bellota filosa | Plantas A | `fh-axenut-bw-icon.png` |
| `corpsecap` | Gorro de muerto | Plantas A | `fh-corpsecap-bw-icon.png` |
| `flamefruit` | Pitallama | Plantas B | `fh-flamefruit-bw-icon.png` |
| `rockroot` | Raíz de roca | Plantas B | `fh-rockroot-bw-icon.png` |
| `snowthistle` | Cardo de nieve | Plantas B | `fh-snowthistle-bw-icon.png` |
| `inspiration` | Inspiración | Otros | `fh-inspiration-bw-icon.png` |
| `morale` | Moral | Otros | `fh-morale-bw-icon.png` |
| `soldiers` | Soldados | Otros | `fh-soldiers-bw-icon.png` |

## Ubicación oficial de assets

- PNG operativos para UI:
  - `assets/resource-icons/`
- Fuentes SVG base (custom):
  - `assets/resource-icons/svg/`

### Convención de nombres

- Patrón: `fh-<resource_key>-bw-icon.<ext>`
- Extensiones usadas:
  - `.png` para runtime UI;
  - `.svg` para fuente editable de iconos custom.

## Origen de iconos

- Reubicados desde referencias temporales (`tmp/loot`) a carpeta oficial:
  - `lumber`, `metal`, `hide`, `arrowvine`, `axenut`, `corpsecap`, `flamefruit`, `rockroot`, `snowthistle`.
- Generados en esta unidad (SVG + PNG) con estilo monocromo compatible:
  - `inspiration`, `morale`, `soldiers`.

## Referencias

- `docs/domain-glossary.md`
- `src/frosthaven_campaign_journal/resource_catalog.py`
- `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`
- `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`
