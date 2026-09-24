---
name: sql-dojo-curriculum
description: Guidelines and a mandatory validator for adding or editing SQL Dojo modules in webapp/curriculum.js (the 100-module track and the 200-module extra pool). Use this whenever creating new modules, editing existing prompts/titles/hints, or touching LESSONS/MODULES/SCHEMAS/EXTRA_MODULES/EXTRA_SCHEMAS in that file.
---

# SQL Dojo curriculum: guidelines and validator

`webapp/curriculum.js` holds two pools:

- `LESSONS` + `MODULES` — the fixed, sequential 100-module track (20 lessons
  x 5 modules), grouped by difficulty (easy, then medium, then hard).
- `EXTRA_SCHEMAS` + `EXTRA_MODULES` — 200 modules outside the track (10
  families x 20 modules, one shared schema fixture per family), used by
  Practice Session and the Randomizer.

Both pools share the same per-module shape:

```js
{
  "id": "...",              // MODULES: "20.2" (lesson.index). EXTRA_MODULES: "extra-N", globally unique.
  "lesson": 20,              // MODULES only — omit entirely for EXTRA_MODULES.
  "family": "sales",         // EXTRA_MODULES only — the source prompts/*.txt this family came from.
  "difficulty": "easy" | "medium" | "hard",
  "title": "...",
  "concept": "...",          // the technique label shown under the title — see rule 2, this one CAN name syntax.
  "tables": "table(col, col, ...)",  // short fallback description; the Sample Tables panel shows the real seeded data automatically.
  "prompt": "...",
  "schemaSql": SCHEMAS.someKey | EXTRA_SCHEMAS.someKey,  // a `const SCHEMAS = { someKey: \`CREATE TABLE...\` }` reference, not a literal string
  "solutionSql": "...",      // must be one reference solution that actually runs and matches the intended answer
  "hint": "...",
  "starter": "-- table(col, col, ...)\n",
}
```

## The four rules (learned from real mistakes made in this file)

**1. Every field must be filled in for real. Never leave a placeholder empty
string and move on.** Seven modules once shipped with `"prompt": ""` because
a bulk-generation pass left a placeholder unfilled and nothing caught it
before the fact. There is no such thing as a field that's "fine to leave
blank" — if you write a module skeleton before its content is ready, finish
it in the same pass, or don't write the skeleton yet.

**2. The title and prompt must never leak the SQL construct needed to solve
the puzzle.** Apply this test: *does the task have a generic English
description that doesn't require naming a SQL clause?* If yes, any
naming of that clause in the title/prompt is an unnecessary leak — remove
it. `"Rebuild the same region pivot using DuckDB's pivot statement"` was the
original example of this bug: the underlying task ("show region totals as
one row of columns") never needed the word "pivot" at all, and naming it
handed over the answer.
  - Exception: modules that are explicitly *about* a syntax/style choice
    (e.g. this curriculum's Snowflake `::type`-cast convention, or an
    md5-surrogate-key module whose whole point is reproducing an exact
    hash formula) may name it, because naming it *is* the lesson, not a
    leak of an otherwise-generic puzzle's answer.
  - The `concept` field is exempt from this rule — it's an always-visible
    technique label (like a chapter heading, e.g. `"RANK() OVER (...)"`,
    `"self-join"`), and every module in this curriculum already uses it
    that way. Only `title` and `prompt` are the leak surface.
  - The `hint` field is also exempt — hints are opt-in (hidden behind
    "Show hint"), so naming the construct there is fine and often the
    entire point of a hint.

**3. Every module must be fully self-contained — no module may depend on
another.** Never write "as before," "same as [other module]," "rebuild the
same X," "reusing the Y from module Z," etc. This breaks immediately in
Randomizer/Practice Session order, and even in the fixed track it's a bad
habit. If a module needs the same constraint/setup as an earlier one,
restate it inline every time.

**4. `solutionSql` must actually run against `schemaSql` and produce the
intended answer.** Never hand-write a solution you haven't executed. See
the validator below — it runs every module's `schemaSql` then `solutionSql`
through a real DuckDB connection and reports anything that errors.

## Mandatory: run the validator after every change

```
python3 .claude/skills/sql-dojo-curriculum/scripts/validate_curriculum.py
```

(Requires `duckdb` — `pip install duckdb` — already installed in this repo's
environment as of this writing.)

This is not optional or "nice to check later" — run it after *any* edit to
`curriculum.js`, whether adding modules, rewording a prompt, or touching
`SCHEMAS`/`EXTRA_SCHEMAS`. It checks, across every module in both pools:

- No empty/missing required fields (this is exactly the class of bug that
  motivated writing this tool — rule 1 above).
- No duplicate `id`s.
- `difficulty` is one of `easy`/`medium`/`hard`.
- `schemaSql` resolves to a real schema and `solutionSql` actually executes
  against it in DuckDB, back to back, with no errors.
- (Soft warnings, not auto-failures — use judgment against rules 2/3 above)
  title/prompt text matching common syntax-naming or cross-reference
  patterns, for you to manually review.

**Exit code 0 with zero hard failures is required before considering
curriculum work done.** Warnings are printed for manual review — judge each
one against rule 2's exception (style/syntax-is-the-lesson modules are fine
to leave as-is) rather than mechanically rewriting every hit.

If you add a new module family or change the file's structure (e.g. rename
`MODULES`/`EXTRA_MODULES`, change how `schemaSql` references work), update
`scripts/validate_curriculum.py`'s parsing to match — it uses regex over the
raw file rather than a JS parser (because `schemaSql` values are JS
identifier references like `SCHEMAS.foo`, not JSON strings, so the module
arrays aren't valid JSON), so keep the two in sync.

## After validating: rebuild and check the diagnostic log

Validation proves the data is correct; it doesn't prove the app renders it.
Rebuild and relaunch (`tauri/build.sh`, then `open`
the built `.app` under `tauri/src-tauri/target/release/bundle/macos/`), and
check the diagnostic log (macOS: `~/Library/Logs/com.mauriceallen.sqldojo/sqldojo.log`)
for a clean load with
no `window.onerror`/capture-phase entries before considering the change
done.
