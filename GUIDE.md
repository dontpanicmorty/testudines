# SQL Dojo — User Guide

SQL Dojo is a self-contained SQL practice app: 300 exercises, an in-app
SQL editor, and instant grading — all running locally against a real
database engine (DuckDB), no internet connection or server required.

## Building and opening the app

SQL Dojo is built with [Tauri](https://tauri.app) — the same app (everything
under `webapp/`) runs on both macOS and Windows, each wrapped in that OS's
own native webview (no bundled browser engine).

**macOS:**
```bash
tauri/build.sh
open "tauri/src-tauri/target/release/bundle/macos/SQL Dojo.app"
```
The first launch may show a Gatekeeper warning since it isn't notarized —
right-click the app and choose **Open** to bypass that once.

**Windows:** build from a Windows machine with the
[Rust toolchain](https://rustup.rs) and the
[Tauri CLI](https://tauri.app/start/prerequisites/) installed:
```powershell
cd tauri/src-tauri
cargo tauri build
```
This produces an installer (`.msi`/`.exe`) under
`src-tauri/target/release/bundle/`. Cross-compiling a Windows build from
macOS isn't practical (Windows installer bundling needs tools that only run
on Windows), so this step has to happen on an actual Windows machine or a
Windows CI runner.

## The home screen

Every time you open SQL Dojo, you land on the home screen first.

### 1. Who's practicing?

Pick your name from the list, or type a new one and hit **Continue**. This
is just a local nickname — no password, no account. It exists so more than
one person can use the same installation without mixing up progress:
everything you complete, every session you start, and your display
preferences are saved separately under your name.

### 2. Choose what to work on

Once you've picked a name, you get five ways into the exercises:

| Option | What it is |
|---|---|
| **Track** | The original, fixed 100-module curriculum, worked in order across 20 lessons (grouped easy → medium → hard). |
| **Practice Session** | You choose which difficulties (easy/medium/hard, any combination) and how many modules; works through that filtered set from the *entire* 300-module catalog, in order, with difficulty and module numbers visible the whole time. |
| **Randomizer** | You choose only a count. Pulls that many modules from the whole 300-module catalog in random order, with difficulty, module numbers, and the side panel all hidden — a blind, unpredictable practice mode. |
| **Easy / Medium / Hard** | One-click shortcuts: instantly starts a Practice Session using *every* module of that difficulty from the full catalog. |

If you already have a Practice Session or Randomizer in progress, that tile
shows **Continue** — it reopens the *exact* same set of modules at the exact
module you were on, not a fresh one. **Start new…** discards that and lets
you configure a different session.

Click **Home** in the top bar at any time to come back here — you don't have
to re-enter your name, just pick a different path. Use **Switch user** on
this screen if a different person wants to use the app next.

## Working an exercise

Each exercise has:

- **Prompt** — what to write a query for.
- **Sample tables** — the *real* data seeded for this exercise, so you can
  see exactly what you're querying before you write anything.
- **Show hint** — a nudge toward the technique, if you want it.
- **Show solution** — one reference answer. This only unlocks after 3
  incorrect check attempts on that exercise, so it doesn't spoil things
  early.

Write your query in the editor on the right, then:

- **Run** — executes your SQL and shows the results, no grading.
- **Check answer** — runs your query *and* the reference answer, and
  compares the results. You can also just press **⌘Enter** (Mac) instead
  of clicking Check.

**Grading compares the data your query returns, not the SQL you wrote.**
Column order, column names/aliases, and row order don't matter — only
whether the actual values match. That means there's almost always more than
one correct way to solve any given exercise (a `JOIN`, a subquery, a window
function, `PIVOT` vs. `CASE WHEN`, etc. can all be equally valid). Reset
brings back the starter text if you want to start that exercise over.

## Pause

Click **Pause** (top bar) any time you need to step away with your screen
visible to others. It freezes the timer and covers the entire exercise —
prompt, data, editor, results, everything — with a blurred, blocked screen
until you click **Resume** (or press Escape). Nothing you've typed is lost.

## Timers

- **Show Timer** — tracks time spent on the *current* module.
- **Show Total Timer** (in the sidebar) — tracks total time across this
  session. Time doesn't accrue while the app is in the background, or while
  paused.

Timers reset to zero on every app relaunch — they're not meant to be a
lifetime tracker, just a per-sitting one.

## Progress: Export / Import

The sidebar has **Export** and **Import** buttons (visible in Track and
Practice Session — the sidebar is hidden during the Randomizer). Export
downloads *all* of your current user's saved progress — every module
you've completed, across Track and Practice Session alike — as a JSON file,
useful as a backup or to move your progress to another machine. Import
loads a previously exported file back in, replacing your current progress
entirely.

## Tips

- Difficulty badges (green/orange/red) tell you easy/medium/hard for Track
  and Practice Session — but not the Randomizer, on purpose.
- If you're stuck, the hint is free to check any time; the solution needs
  3 failed attempts first.
- The Randomizer and Practice Session both draw from the same 300-module
  catalog — the difference is entirely in *order* (sequential vs. shuffled)
  and *transparency* (visible vs. hidden difficulty/id/sidebar), not in
  which exercises are available.
