# Py Dojo

A native desktop application (Qt, no browser, no server) that takes a SQL/dbt/Snowflake practitioner from zero Python to production-grade work: libraries, services, pipelines and data wrangling.

Everything the app needs ships inside this folder: lessons, exercises, tests, datasets and reference sheets. Nothing is fetched or linked at runtime.

## Install (packaged app, macOS)

Open `dist/PyDojo-<version>-<arch>.dmg` and drag **Py Dojo** into Applications. The app carries its own Python and every library, so it needs no internet, no `uv` and no system Python. Progress is stored in `~/Library/Application Support/PyDojo`, so replacing the app with a newer build never loses it.

Build it yourself with `./scripts/build_macos.sh` (needs internet once; produces `dist/Py Dojo.app` and the `.dmg`, then self-tests the result).

## Run from source

macOS / Linux: `./run.sh` (macOS: double-click `Py Dojo.command`)
Windows: `./run.ps1`

The first launch needs internet once, to install its own Python and packages into this folder (`.tools/`, `.venv/`). After that it runs fully offline. It does not use or modify any Python already installed on the machine.

Your progress is stored in `user_data/progress.db`. Copy the folder to move everything to another machine; set `PYDOJO_HOME` to keep progress elsewhere.

## How a session works

1. **Recall**: spaced-repetition cards from lessons you've read.
2. **Rebuild**: exercises you solved days ago, redone from a blank starter.
3. **New material**: one lesson, then its exercises.

Each exercise is graded by real pytest tests in a throwaway directory.

## Editing the curriculum

Every lesson (`id` in the `lesson.md` front matter), exercise (`id` in `exercise.toml`) and review card (`id` on each `[[card]]`) has a permanent ID. Progress is stored against that ID only.

- Folder names and card positions control **order**, not identity: rename, reorder and insert freely.
- Never change an existing `id`. A new card needs a new unique `id` (any short unique string).
- `pydojo validate` reports missing or duplicate IDs, and checks every exercise.

## Maintainers

`pydojo selftest` verifies an installation end to end: content, grading, every page, and the learner libraries.

`./run.sh validate` checks that every exercise's starter fails and its reference solution passes.
