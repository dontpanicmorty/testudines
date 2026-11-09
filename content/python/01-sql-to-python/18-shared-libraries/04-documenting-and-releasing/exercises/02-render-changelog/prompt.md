Write `render_changelog(entries)`. `entries` is a list of `(version, date, kind, text)` tuples, listed newest version first (entries of one version are not necessarily adjacent).

Output Markdown:

- one heading per version in order of first appearance: `## [1.5.0] - 2026-02-01`
- under it, one `### Kind` section per kind present, in the order **Added, Changed, Deprecated, Removed, Fixed** (not input order)
- each entry as `- text`, in input order
- blank line between blocks as shown; the output ends with exactly one newline; empty input gives `""`

```python
render_changelog([
    ("1.5.0", "2026-02-01", "Fixed", "Trim spaces."),
    ("1.5.0", "2026-02-01", "Added", "top_n option."),
    ("1.4.0", "2026-01-10", "Added", "First release."),
])
```

```
## [1.5.0] - 2026-02-01

### Added
- top_n option.

### Fixed
- Trim spaces.

## [1.4.0] - 2026-01-10

### Added
- First release.
```
