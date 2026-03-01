# Frosthaven Campaign Journal

Aplicación de apoyo para campaña de Frosthaven con foco en:

1. Registro fiable de recursos, weeks, entries y sesiones.
1. Flujo de trabajo profesional con trazabilidad técnica.

## Estado del proyecto

- Estado: implementación activa del MVP.
- UI: arquitectura declarativa MVS (`model/state/view`) con Flet.
- Datos: Firestore real (sin fallback automático a mocks).

## Estructura del repositorio

- `AGENTS.md`: contrato operativo de trabajo.
- `docs/`: documentación oficial operativa.
- `learning/`: guías reutilizables de aprendizaje.
- `src/`: código de aplicación.

## Flujo de trabajo GitHub (resumen)

- Modelo: GitHub Flow minimalista.
- Tareas: GitHub Issues como fuente principal.
- Commits: Conventional Commits en castellano.
- Ramas: `tipo/<issue-id>-slug`.
- PR: obligatoria en cambios relevantes.
- Cambios triviales: se permite `main` directo.

## Versionado y cambios

- Versionado: SemVer temprano (`v0.x.y`).
- Cambios acumulados: `CHANGELOG.md`.
- Cierre de hitos: tag + release notes.

## Documentación clave

- [Mapa del sistema](docs/system-map.md)
- [Gobierno de contexto](docs/context-governance.md)
- [Flujo de repositorio](docs/repo-workflow.md)
- [Guía de contribución](CONTRIBUTING.md)

## Arranque local

Requisitos:

- Python `3.12`
- `pipenv`

Comandos:

```powershell
pipenv --python 3.12
pipenv install
pipenv run flet run src/main.py --web -d -r --port 8550 --host 127.0.0.1
```

## Licencia

Este proyecto se publica bajo licencia MIT.
