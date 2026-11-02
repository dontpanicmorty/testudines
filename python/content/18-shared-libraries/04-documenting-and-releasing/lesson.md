+++
id = "shared-libraries.documenting-and-releasing"
title = "Documenting and releasing"
minutes = 30
+++

# Documenting and releasing

A library nobody can figure out how to use is a library nobody uses. A library nobody dares upgrade is just as dead. This lesson covers the two habits that keep a shared package healthy: documentation that lives next to the code, and a repeatable release.

> **dbt bridge.** `description:` fields in YAML become the docs site, and a good README is the difference between a package people adopt and one they fork. A release is like cutting a new package version in your dbt hub listing: a tag, a version, a changelog entry, and a promise.

## Docstrings are documentation

A docstring is a string literal as the first statement of a function, class or module. Python stores it in `__doc__`, and `help()` and editors show it. Write it for someone who has not read your code.

```python
def parse_amount(text: str) -> float:
    """Convert an amount string such as ``"$1,234.50"`` to a float.

    Args:
        text: Raw text from an export. Surrounding whitespace, a leading
            ``$`` and thousands separators are ignored.

    Returns:
        The amount as a float.

    Raises:
        ValueError: If the text is not a number after cleaning.
    """
    return float(text.strip().replace("$", "").replace(",", ""))

print(parse_amount.__doc__.splitlines()[0])
print(parse_amount("$1,234.50"))
```

A good docstring answers: what does it do (one line), what do the arguments mean, what does it return, what can it raise. Don't restate the code: "increments i" is noise; "rows with a null key are dropped" is information.

## Examples that cannot go stale: doctest

Put runnable examples **in** the docstring. The standard library's `doctest` runs them and fails if the output differs, so the docs cannot silently rot.

```python
import doctest

def slugify(text):
    """Lowercase text and join words with hyphens.

    >>> slugify("Daily Orders Report")
    'daily-orders-report'
    >>> slugify("  Extra   spaces ")
    'extra-spaces'
    """
    return "-".join(text.lower().split())

print(doctest.testmod())
```

`TestResults(failed=0, attempted=2)` means both examples passed. Lines starting with `>>>` are the code; the next line is the exact expected output.

## README anatomy

The README is the front door. In order:

1. **What it is**: one sentence and who it is for.
2. **Install**: the one command to run.
3. **Quick start**: a minimal, working example, copy-pasteable.
4. **API overview**: the public functions, one line each (not everything).
5. **Configuration**: environment variables and options.
6. **Compatibility**: supported Python versions and the versioning policy.
7. **Contributing and releasing**: how to run tests, how to cut a release.

Test the quick start. A README example that raises on the first copy-paste costs you more trust than any bug.

## The release checklist

A release should be boring: the same steps every time, ideally as a script or CI job. A manual checklist at minimum:

1. Tests, linting and type checks pass on the main branch.
2. Decide the bump from the changelog (patch, minor, major).
3. Update the version in one place (`pyproject.toml`; read it elsewhere if needed).
4. Move "Unreleased" changelog entries under the new version with today's date.
5. Build the artifacts (sdist and wheel) and inspect their contents.
6. Tag the commit with the version and publish.
7. Announce breaking changes and deprecations to consumers.

Checks like "version in pyproject matches `__version__`" and "changelog mentions this version" are easy to automate, and mismatches are a classic release bug:

```python
import re

def version_in_changelog(changelog_text, version):
    return re.search(rf"^## \[{re.escape(version)}\]", changelog_text, re.M) is not None

log = "## [Unreleased]\n\n## [1.5.0] - 2026-02-01\n### Added\n- top_n\n"
print(version_in_changelog(log, "1.5.0"), version_in_changelog(log, "1.6.0"))
```

## How teams consume an internal package

Internal libraries usually are not on the public index. Two common routes, shown as commands only (they need a network and credentials, so they do not run here):

```python
# no-run
# 1. A private package index (artifact repository): the team publishes wheels,
#    consumers install by name and version range.
#      pip install --index-url https://pypi.internal.example/simple "acme-datakit>=1.4,<2"
#
# 2. Straight from a git tag: no index needed, the tag is the version.
#      pip install "acme-datakit @ git+https://git.internal.example/data/datakit.git@v1.4.2"
#
# In the consumer's pyproject.toml either one becomes a dependency line:
#      dependencies = ["acme-datakit>=1.4,<2"]
```

The `>=1.4,<2` range is where semantic versioning pays off: consumers automatically take compatible releases and are protected from major breaks. Git tags (`v1.4.2`) should be immutable: never move a tag after it is published.

Consumers should also **pin exactly** in their deployed environments through a lock file, and upgrade deliberately, running their tests when they do.

## Common mistakes

- Docs and code diverge because examples are not executed.
- Moving or deleting a published tag or version. Published versions are forever; fix forward with a patch.
- `__version__` in the code and the version in `pyproject.toml` drift apart.
- Releasing from a dirty working tree or an unmerged branch.
- A README with no install line.

## What to take away

1. Docstrings document purpose, arguments, returns and raises; doctests keep examples honest.
2. The README is the front door: what, install, quick start, API, compatibility.
3. A release is a repeatable checklist: tests, bump, changelog, build, tag, announce.
4. Automate consistency checks between version, changelog and tag.
5. Consumers depend on version ranges for libraries and exact pins for deployments.
