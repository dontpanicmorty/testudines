# SQL Dojo

A self-contained SQL practice app: 300 exercises, an in-app SQL editor, and
instant grading — all running locally against a real database engine
(DuckDB), no internet connection or server required.

For how to build and use the app, see [GUIDE.md](GUIDE.md). For open
verification/integrity gaps, see [KNOWN_GAPS.md](KNOWN_GAPS.md).

## Repository history

This repository was extracted from the `apps_and_builds/sql-dojo/`
subdirectory of a larger personal monorepo, with full git history for those
files preserved. The steps below document exactly how that extraction was
done, kept here for reference (e.g. if a similar split is ever needed again
for another app in that monorepo).

Replace `<NEW_REMOTE_URL>` below with the actual URL of the empty remote
repo created for this purpose.

### Recommended approach: preserve git history

This uses `git-filter-repo` to rewrite a *disposable clone* of the monorepo
so it looks like `sql-dojo/` was always its own repo root, with full commit
history intact for those files.

#### 1. Install git-filter-repo (no Homebrew needed)

`git-filter-repo` is just a Python script — install it with `pip3`
(already on your machine via Xcode's Python) instead of Homebrew:

```bash
pip3 install --user git-filter-repo
```

If `git filter-repo` isn't found on your `PATH` afterward, run it directly
with `python3 -m git_filter_repo` in place of `git filter-repo` in step 3
below, or add `~/Library/Python/3.9/bin` (whatever `pip3` reports as the
user base `bin` dir) to your `PATH`.

#### 2. Make a disposable clone (never run filter-repo on your real working copy)

```bash
cd ~/Documents/repositories/personal
git clone --no-local code sql-dojo-extraction
cd sql-dojo-extraction
```

`--no-local` is required — a plain local clone uses hardlinks that
`git-filter-repo` refuses to run against.

#### 3. Rewrite history to isolate just the sql-dojo subtree

```bash
git filter-repo --path apps_and_builds/sql-dojo/ --path-rename apps_and_builds/sql-dojo/:
```

After this, `apps_and_builds/sql-dojo/tauri/...` becomes just `tauri/...`
at the new repo's root, and history is rewritten to only include commits
that touched those files.

#### 4. Bring the two related Claude Code skills along

These currently live at the monorepo's `.claude/skills/` (outside the
subtree that got extracted), so copy them in manually:

```bash
mkdir -p .claude/skills
cp -R ~/Documents/repositories/personal/code/.claude/skills/sql-dojo-curriculum .claude/skills/
cp -R ~/Documents/repositories/personal/code/.claude/skills/sql-dojo-icon .claude/skills/
git add .claude
git commit -m "Bring sql-dojo Claude Code skills along from the monorepo"
```

#### 5. Fix paths that assumed the monorepo layout

- **`.claude/skills/sql-dojo-curriculum/scripts/validate_curriculum.py`** —
  find this line:
  ```python
  DEFAULT_PATH = Path(__file__).resolve().parents[4] / "apps_and_builds" / "sql-dojo" / "webapp" / "curriculum.js"
  ```
  and change it to (same `parents[4]` depth — the script's own nesting under
  `.claude/skills/...` didn't change — just drop the `apps_and_builds/sql-dojo`
  prefix since this repo's root now *is* that directory):
  ```python
  DEFAULT_PATH = Path(__file__).resolve().parents[4] / "webapp" / "curriculum.js"
  ```
- **`GUIDE.md`** and **`KNOWN_GAPS.md`** — search for
  `apps_and_builds/sql-dojo/` and remove that prefix from any paths/commands
  (e.g. `apps_and_builds/sql-dojo/tauri/build.sh` becomes `tauri/build.sh`).
- **`.claude/skills/sql-dojo-icon/SKILL.md`** — same find/replace for any
  `apps_and_builds/sql-dojo/` path references.

Commit these fixes:

```bash
git add -A
git commit -m "Fix paths for standalone repo layout"
```

#### 6. Point at the new remote and push

```bash
git remote add origin <NEW_REMOTE_URL>
git branch -M main
git push -u origin main
```

#### 7. Verify the new repo works standalone

```bash
python3 .claude/skills/sql-dojo-curriculum/scripts/validate_curriculum.py
./tauri/build.sh
open "tauri/src-tauri/target/release/bundle/macos/SQL Dojo.app"
```

Check `~/Library/Logs/com.mauriceallen.sqldojo/sqldojo.log` for a clean
launch.

#### 8. Decide what happens to the monorepo's copy

Once the new repo is confirmed working, decide in the original `code` repo:

- **Remove it** (recommended — avoids the two copies drifting apart):
  ```bash
  cd ~/Documents/repositories/personal/code
  git rm -r apps_and_builds/sql-dojo
  git commit -m "Remove sql-dojo: now maintained in its own repository"
  git push
  ```
- **Leave it as a frozen snapshot** — only do this if you're fine with
  future SQL Dojo work happening exclusively in the new repo and the
  monorepo copy going stale.

#### 9. Clean up the disposable clone

```bash
rm -rf ~/Documents/repositories/personal/sql-dojo-extraction
```

#### 10. Double-check Git LFS on the new remote

The monorepo had Git LFS disabled server-side at one point, which blocked
pushes until worked around locally. This is a separate, per-repository
GitHub setting — check the new repo's LFS status independently rather than
assuming it's already configured correctly.

---

### Alternative: preserve history with zero installs, using `git subtree`

`git subtree split` ships built into git itself, so this needs no
pip/Homebrew install at all. It's slower than `git-filter-repo` on large
histories, but a subtree this size makes that difference immaterial.

```bash
cd ~/Documents/repositories/personal
git clone code sql-dojo-extraction
cd sql-dojo-extraction

# Create a branch containing only the history that touched apps_and_builds/sql-dojo/
git subtree split --prefix=apps_and_builds/sql-dojo -b sql-dojo-only

# Move into its own clone rooted at that branch
cd ..
git clone sql-dojo-extraction sql-dojo-standalone --branch sql-dojo-only
cd sql-dojo-standalone
git checkout -b main
git branch -D sql-dojo-only
```

From here, continue with steps 4-10 above (bring the two skills along, fix
paths, add the new remote, push, verify, clean up, decide on the monorepo
copy).

---

### Alternative: fresh start, no history

If commit history didn't need to carry over, this simpler path was
available instead:

```bash
mkdir ~/Documents/repositories/personal/sql-dojo
cp -R ~/Documents/repositories/personal/code/apps_and_builds/sql-dojo/. ~/Documents/repositories/personal/sql-dojo/
cp -R ~/Documents/repositories/personal/code/.claude/skills/sql-dojo-curriculum ~/Documents/repositories/personal/sql-dojo/.claude/skills/
cp -R ~/Documents/repositories/personal/code/.claude/skills/sql-dojo-icon ~/Documents/repositories/personal/sql-dojo/.claude/skills/
cd ~/Documents/repositories/personal/sql-dojo
git init
git add -A
git commit -m "Initial commit: SQL Dojo, extracted from personal/code monorepo"
git branch -M main
git remote add origin <NEW_REMOTE_URL>
git push -u origin main
```

Then the same path fixes from step 5 above, and the same decision about the
monorepo copy from step 8, would still apply.
