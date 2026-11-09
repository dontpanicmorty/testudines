---
name: testudines-curriculum
description: Guidelines and the mandatory validator for adding or editing Testudines curriculum, in either language. Use this whenever creating, rewording, reordering or removing SQL exercises (content/sql/, the guided track and the practice families) or Python modules, lessons, exercises and review cards (content/python/).
---

# Testudines curriculum: guidelines and validator

The curriculum is plain files under `content/`, one folder per exercise. The
app reads them at launch; nothing is generated or compiled.

## SQL (`content/sql/`)

```
content/sql/
  track/NN-lesson-slug/            the guided track: 20 lessons x 5 exercises, in order
    lesson.toml                    id, number, title, difficulty
    schema.sql                     tables shared by the lesson's exercises (optional)
    exercises/NN-exercise-slug/
      exercise.toml                id, title, difficulty, concept, tables, hint
      prompt.md                    the task
      solution.sql                 one reference answer
      starter.sql                  what the editor starts with
      schema.sql                   this exercise's own tables (optional; overrides the lesson's)
  practice/NN-family-slug/         10 families x 20 exercises, for Practice Sessions and the Randomizer
    family.toml                    id, title, source_prompt
    schema.sql                     the family's shared tables
    exercises/NN-exercise-slug/    same files as above
```

- `difficulty` is `easy`, `medium` or `hard`.
- Track ids are `lesson.index` (`"20.2"`); practice ids are `"extra-N"`. Ids
  are permanent progress keys: never change or reuse one. Folder names (the
  `NN-` prefixes) control **order**, not identity.
- An exercise's tables are its own `schema.sql` if it has one, otherwise its
  lesson's or family's `schema.sql`.
- Grading compares result values only (column order, names and row order are
  ignored), so `solution.sql` is one correct answer, not the only one.
- Changing `solution.sql` drops learners' progress on that exercise (it may be
  a different exercise now). Only change it when the task changed.

## Python (`content/python/`)

```
content/python/
  NN-path-slug/                    a learning path: 01-sql-to-python, 02-python-for-everybody
    path.toml                      id, title, summary
    NN-module-slug/
      module.toml                  title, summary, stage
      NN-lesson-slug/
        lesson.md                  +++ id, title, minutes +++ front matter, then the lesson
        cards.toml                 [[card]] id, q, a: review cards
        exercises/NN-exercise-slug/
          exercise.toml            id, title, difficulty (1-3), main, hints
          prompt.md
          starter/                 the files the learner starts from
          reference/               a solution that passes
          tests/                   pytest tests that grade it
  reference/                       the Reference page's cheat sheets
```

- Lesson, exercise, card and path ids are permanent progress keys: never
  change or reuse one. A new card needs a new unique `id`; generate it with
  `secrets.token_hex(4)`.
- Ids carry their path's prefix: `everybody.` in Python for Everybody. The
  older From SQL to Python ids have no prefix; leave them as they are.
- Learner code runs with limits: 20 seconds (`timeout` in `exercise.toml`),
  a memory cap of 512 MB to 1.5 GB depending on the computer (`memory_mb`),
  1 MB of output, and at most 2 threads for numpy/polars/pyarrow. Keep
  exercises well inside them; raise `timeout` or `memory_mb` only when an
  exercise genuinely needs it. SQL queries get 256 MB, 2 threads, 20 seconds,
  100,000 rows, and no file or network access.
- Exercises run with stdin closed and no internet. Grade functions, not
  `input()`, and have network exercises talk to a local server that the test
  starts on 127.0.0.1.
- **Python for Everybody follows the chapters and topics of Charles
  Severance's book (CC BY-NC-SA 3.0), but all of its prose, examples, data and
  exercises are original.** Never copy or closely paraphrase the book's text,
  sample programs, data files (its mbox, romeo or geodata files) or exercise
  wording. Keep the credit in its `path.toml` and the README.

## The four rules (learned from real mistakes)

**1. Every field must be filled in for real. Never leave a placeholder empty
and move on.** Seven SQL exercises once shipped with an empty prompt because a
bulk-generation pass left placeholders unfilled. If you write a skeleton,
finish it in the same pass.

**2. The title and prompt must never leak the construct needed to solve the
puzzle.** Test: *does the task have a plain-English description that doesn't
name the SQL clause or Python feature?* If yes, naming it is a leak, so remove
it. `"Rebuild the same region pivot using DuckDB's pivot statement"` was the
original example: the task ("show region totals as one row of columns") never
needed the word "pivot".
  - Exception: exercises that are explicitly *about* a syntax or style choice
    (Snowflake `::type` casts, reproducing an exact md5 surrogate-key formula)
    may name it, because naming it is the lesson.
  - `concept` is exempt: it is an always-visible technique label.
  - Hints are exempt: they are opt-in, and naming the construct is often the
    whole point.

**3. Every exercise must be self-contained.** Never write "as before", "same
as [other exercise]", "rebuild the same X" or "reusing the Y from exercise Z".
Practice Sessions and the Randomizer show exercises out of order. Restate any
shared setup inline every time.

**4. Every reference must actually run and give the intended answer.** Never
hand-write a solution you haven't executed. The validator runs every one.

## Mandatory: run the validator after every change

```
./run.sh validate          # both languages (Windows: .\run.ps1 validate)
./run.sh validate sql      # or just one section
./run.sh validate python
```

It checks:

- **SQL:** every field is filled in (prompt, solution, schema, starter,
  title, concept, tables, hint); ids are present and unique; difficulty is
  valid; the tables load; the solution runs; the starter doesn't already
  pass. A solution that returns no rows is printed as a `note`, not a
  problem: some exercises expect an empty result or build tables. Review
  any new note.
- **Python:** ids are present and unique; every lesson has a body; every
  card has a question and an answer; every reference passes its tests; every
  starter fails them.

**Exit code 0 with 0 problems is required before the work is done.** Rules 2
and 3 aren't machine-checked: reread every title and prompt you touched
against them.

Then run the tests (`uv run pytest`). `tests/test_sql.py` pins the
curriculum's counts (20 lessons, 100 track exercises, 10 families, 200
practice exercises): update those numbers when you add or remove exercises on
purpose.

## After validating: see it in the app

Validation proves the data is right, not that the app shows it well. Launch
from source (`./run.sh`), open an exercise you changed, and check that its
prompt, sample tables and editor look right and that its reference passes
**Check answer**.
