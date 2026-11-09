# Testudines

A native desktop app for practicing **SQL** and **Python**, for macOS and
Windows. Everything runs on your machine: 300 SQL exercises graded by a real
database engine (DuckDB), and two Python learning paths with lessons, review
cards and exercises graded by real tests (pytest). No account, no server, and no
internet once it's installed.

## Install and open

**macOS:** open the disk image for your Mac and drag **Testudines** into
Applications: `Testudines-<version>-arm64.dmg` for Apple silicon (M-series)
Macs, `Testudines-<version>-x86_64.dmg` for Intel Macs. (Not sure which? Apple
menu → About This Mac: "Chip: Apple M…" is Apple silicon, "Processor: Intel"
is Intel.) The first time, right-click the app and choose **Open** (it isn't
notarized, so macOS asks once).

**Windows:** unzip `Testudines-<version>-windows-x64.zip` anywhere and
double-click **Testudines.cmd** inside the folder. If SmartScreen warns about
it, choose **More info → Run anyway** once.

Both carry their own Python and every library, so nothing else needs to be
installed. To build them yourself, see [Building](#building).

### System requirements

| | macOS | Windows |
|---|---|---|
| System | macOS 14 (Sonoma) or later, on an Apple silicon or Intel Mac | Windows 10 or 11, 64-bit (also runs on Windows on Arm, emulated) |
| Memory | 4 GB or more | 4 GB or more |
| Disk | about 800 MB | about 800 MB |

### Light on your computer

Testudines uses about 160 MB of memory and almost no CPU while you work. The
code you write runs with limits, so a mistake can't slow down or freeze your
computer:

- **Python** you run or check gets at most 20 seconds, and at most a share of
  your computer's memory (a sixth of it, between 512 MB and 1.5 GB). It runs
  at a lower priority than the app, and stops if it prints more than 1 MB.
  Anything it starts is stopped with it, and at most two programs run at once.
  When one is stopped, the output says why ("Infinite loop?", "Is a list
  growing without end?").
- **SQL** runs with 2 threads and up to 256 MB of memory (less on a computer
  with under 4 GB), for at most 20 seconds. A result keeps its first 100,000
  rows, and the results table shows the first 1,000. Queries can't read files
  or reach the network: they only see the exercise's tables.
- Pressing Run or Check again while one is running does nothing until it
  finishes.

An exercise that genuinely needs more can say so in its `exercise.toml`
(`timeout = 40`, `memory_mb = 2048`).

**Run from source** instead: `./run.sh` on macOS (or double-click
`Testudines.command`), `.\run.ps1` on Windows. The first launch needs internet
once to set up its own Python in this folder (`.tools/`, `.venv/`); it never
touches a Python already on the machine.

## Who's practicing?

The first time Testudines opens, it asks for a name. Type one and press
**Add**. It's just a local nickname, with no password, so more than one person
can share an installation: everything each person completes, their sessions,
streak and scratch pad are kept separately. Use **Switch user** at the top of
the sidebar to change person.

Pick **SQL** or **Python** at the top of the sidebar to switch sections. The
app reopens on the last person and section you used.

## The SQL section

### Home: choose how to practice

| Option | What it is |
|---|---|
| **Guided Track** | The fixed 100-exercise curriculum: 20 lessons, worked in order, easy to hard. **Continue the track** picks up where you left off. |
| **Practice Session** | Tick the difficulties you want and choose how many exercises. It works through that set from the whole 300-exercise catalog, in order, with difficulty showing. |
| **Easy / Medium / Hard** | One-click Practice Sessions with every exercise of that difficulty. |
| **Randomizer** | Choose only a count. It picks that many from all 300 at random and hides their difficulty and the exercise list. |

A Practice Session or Randomizer in progress shows **Resume session** or
**Resume randomizer**, which reopens the same set at the exercise you were on.
Starting a new one replaces it. **End session** on the exercise screen
finishes it.

### Working an exercise

Each exercise shows:

- the **prompt**: what your query should return;
- **sample tables**: the real rows seeded for this exercise, so you can see
  what you're querying;
- **Show hint**: a nudge toward the technique;
- **Show solution**: one reference answer, available after 3 incorrect
  checks (or once you've solved it).

Write your query in the editor, then:

- **▶ Run** (⌘↵ on macOS, Ctrl+Enter on Windows) runs it and shows the
  results, without grading.
- **✓ Check answer** (⇧⌘↵, Ctrl+Shift+Enter) runs your query and the
  reference, and compares the results.

**Grading compares the data your query returns, not the SQL you wrote.**
Column order, column names and row order don't matter, only the values. So
there's almost always more than one right answer: a join, a subquery or a
window function can all be correct. Every run starts from fresh tables, so a
query that changes data can't break the next one.

Your query is saved as you type. **Reset** brings back the starter.
**← Previous** and **Next →** move through the session, and the list on the
left jumps to any exercise in it (it's hidden in the Randomizer, on purpose).

### Pause and timers

**Pause** covers the whole exercise (prompt, tables, editor, results) and
stops the timers, for when you step away with your screen visible. **Resume**
or Escape brings it back; nothing you typed is lost.

The **timer** buttons show time on the current exercise (it stops when you
solve it) and total time this sitting. Both reset each time the app opens:
they're per sitting, not a lifetime tracker.

### Export and Import

**Export…** on the SQL home screen saves your SQL progress (completed
exercises, your queries, failed checks) to a JSON file, as a backup or to
move to another machine. **Import…** loads one back, replacing your current
SQL progress. It also accepts progress exported from SQL Dojo, this app's
earlier version, so that progress carries over. Exercises that have changed
since the export keep your query but not their completion.

## The Python section

The Python section has two learning paths. Choose one at the top of the
**Curriculum** page; you can switch at any time, and progress in each is kept.

| Path | For |
|---|---|
| **From SQL to Python** | Data and analytics engineers who already think in SQL. 20 modules from zero Python to production-grade work: lessons bridge from SQL ideas, and the exercises are the data work you'd actually do (files and formats, wrangling, testing, DataFrames, APIs, pipelines, services). |
| **Python for Everybody** | Anyone, with no programming experience needed: the foundations of the language, step by step. 16 modules follow the chapters of Charles Severance's open textbook [*Python for Everybody*](https://www.py4e.com) (CC BY-NC-SA 3.0): your first program, variables, conditionals, functions, loops, strings, files, lists, dictionaries, tuples, regular expressions, networked programs, web services, objects, databases and SQL, and visualizing data. The lessons and exercises are written for Testudines, so you can read the book alongside them or not. The web chapters run against small local servers, so everything still works offline. |

- **Today**: your session, in three parts. **Recall** the review cards that
  are due, **rebuild** an exercise you solved days ago from a blank starter,
  then **new material**: the next lesson and its exercises, from the path
  you're following. Review cards and rebuilds come from every path.
- **Curriculum**: the path picker, then that path's modules and lessons, with
  your progress. Open any lesson; **Mark as read and add cards to review** adds its cards to your
  reviews.
- **Exercises**: the prompt, an editor with the starter code, and **▶ Run**
  (⌘↵, Ctrl+Enter) and **✓ Check** (⇧⌘↵, Ctrl+Shift+Enter). Check runs the
  exercise's pytest tests in a throwaway folder and shows which pass. Hints
  open one at a time; **Show solution** asks you to try once more first.
  Solved exercises come back later to redo from scratch.
- **Review**: spaced-repetition cards. Answer in your head, press
  **Show answer** (space), then grade yourself **Again / Hard / Good / Easy**
  (1-4). Cards you know come back less often. The sidebar shows how many are
  due.
- **Scratchpad**: free Python, run with ▶ Run, saved automatically, never
  graded. The bundled datasets (CSV, JSON, JSONL) are in the folder named by
  `os.environ["DOJO_DATA"]`.
- **Reference**: cheat sheets for the Python you use most.

The scratchpad's bundled datasets and the libraries installed with the app
(DuckDB, pandas, polars, pydantic, httpx, BeautifulSoup and more) work the
same in both paths.

The sidebar shows your streak: the days in a row you've practiced, in either
section.

## Where progress is kept

| Running | Folder |
|---|---|
| The macOS app | `~/Library/Application Support/Testudines` |
| The Windows app | `%APPDATA%\Testudines` |
| From source | `user_data/` in this folder |

Inside, each person has a folder under `users/` with their `progress.db`
(both sections) and `scratch.py`. Replacing the app with a newer build never
touches it. Copy the folder to back up or move everything; set
`TESTUDINES_HOME` to keep it somewhere else.

The first person added also takes over any Py Dojo progress found on the
machine (this app's earlier Python version).

## Editing the curriculum

The curriculum is plain files under `content/`, one folder per exercise. The
app reads them when it opens, so a change shows up on the next launch.

Every lesson, exercise and review card has a permanent `id`, and progress is
stored against it. **Never change or reuse an id.** Folder names (the `NN-`
prefixes) set the **order**, not the identity, so you can rename, reorder and
insert freely.

### SQL (`content/sql/`)

```
content/sql/
  track/NN-lesson/                 the guided track, in order
    lesson.toml                    id, number, title, difficulty
    schema.sql                     tables shared by the lesson (optional)
    exercises/NN-exercise/
      exercise.toml                id, title, difficulty, concept, tables, hint
      prompt.md                    the task
      solution.sql                 one reference answer
      starter.sql                  what the editor starts with
      schema.sql                   this exercise's own tables (optional)
  practice/NN-family/              exercises for Practice Sessions and the Randomizer
    family.toml                    id, title
    schema.sql                     the family's shared tables
    exercises/NN-exercise/         same files as above
```

To **add an exercise**, copy an exercise folder next to it, give it a new
`id` (`"lesson.index"` in the track, `"extra-N"` in a practice family), and
rewrite its files. `difficulty` is `easy`, `medium` or `hard`. An exercise uses
its own `schema.sql` if it has one, otherwise its lesson's or family's.

To **add a lesson or family**, add a folder with a `lesson.toml` (or
`family.toml`), a `schema.sql` and an `exercises/` folder.

Changing an exercise's `solution.sql` resets everyone's progress on that
exercise (it may be a different task now), so only change it when the task
changed.

### Python (`content/python/`)

```
content/python/
  NN-path/                         a learning path, e.g. 01-sql-to-python, 02-python-for-everybody
    path.toml                      id, title, summary
    NN-module/
      module.toml                  title, summary, stage (the heading it's grouped under)
      NN-lesson/
        lesson.md                  +++ id, title, minutes +++, then the lesson in Markdown
        cards.toml                 [[card]] blocks: id, q, a
        exercises/NN-exercise/
          exercise.toml            id, title, difficulty (1-3), main, hints
          prompt.md
          starter/                 the files the learner starts from
          reference/               a solution that passes
          tests/                   the pytest tests that grade it
  reference/                       the Reference page's cheat sheets (Markdown)
```

To **add a path**, add a folder with a `path.toml` and module folders. Its
`id` is where each person's choice of path is saved, so never change it.

To **add an exercise**, copy an exercise folder, give it a new `id`, and write
the prompt, starter, reference and tests. A new review card needs a new unique
`id` (any short string).

### Check your changes

```
./run.sh validate          # both sections (Windows: .\run.ps1 validate)
./run.sh validate sql      # or one section
./run.sh validate python
./run.sh validate python 05-iteration   # just the modules (or paths) whose id contains this
```

The validator must report **0 problems**. It checks:

- **SQL:** every field is filled in, ids are unique, the tables load, the
  solution runs, and the starter doesn't already pass. A solution that returns
  no rows is listed as a `note` (some exercises expect an empty result), not a
  problem.
- **Python:** ids are unique, every lesson and card is filled in, every
  reference passes its tests, and every starter fails them.

Two rules it can't check, so read your titles and prompts for them:

1. **Don't give the answer away.** If the task can be described in plain
   English, the title and prompt shouldn't name the SQL clause or Python
   feature that solves it. (The `concept` label and the hints may.)
2. **Every exercise stands alone.** No "as before" or "same as the last
   exercise": Practice Sessions and the Randomizer show them out of order.

Then run the tests: `uv run pytest`.

## Building

**macOS** (on a Mac; needs internet once):

```
scripts/build_macos.sh                          # for this Mac's kind (Apple silicon or Intel)
TESTUDINES_ARCH=x86_64 scripts/build_macos.sh   # an Intel build, on an Apple silicon Mac with Rosetta
```

It builds `dist/Testudines.app` (an Intel build on an Apple silicon Mac goes
to `dist/x86_64/Testudines.app`) and `dist/Testudines-<version>-<arch>.dmg`,
with an embedded Python, every library, the curriculum and the datasets. It
removes the parts of Qt the app never uses (`scripts/prune_bundle.py`, about
250 MB), then self-tests, signs (ad hoc) and self-tests the app again.

**Windows** (on Windows, in PowerShell; needs internet once):

```
.\scripts\build_windows.ps1
```

It builds the `dist\Testudines` folder and
`dist\Testudines-<version>-windows-x64.zip`, trims Qt the same way, then
self-tests them.

**GitHub Actions** (`.github/workflows/build.yml`) runs the tests, validates
the curriculum, and builds and self-tests the app on an Apple silicon Mac, an
Intel Mac and Windows on every push, uploading the three builds as artifacts.

`testudines selftest` (`./run.sh selftest`) checks an installation end to end:
the content, SQL and Python grading, users, and every page.

The icon is drawn in code by `scripts/make_icon.py`
(`uv run python scripts/make_icon.py` writes `src/testudines/assets/icon.png`).

## Known gaps

- **Import trusts completion.** An exported progress file is plain JSON, so
  someone could edit it to mark exercises complete and import it. The
  curriculum and its solutions ship with the app, so no purely local check
  can prove an exercise was solved without seeing the answer. A sensible
  future step: re-check each imported query against its exercise on import,
  and record whether the solution was shown.
- **The apps aren't notarized or code-signed** with a developer certificate,
  so macOS and Windows each warn once on first open.
