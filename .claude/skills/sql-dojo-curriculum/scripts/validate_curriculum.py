#!/usr/bin/env python3
"""
Validates webapp/curriculum.js.

Run this after ANY edit to curriculum.js -- adding modules, editing prompts,
reordering, anything. It is the mandatory gate before considering curriculum
work done; see ../SKILL.md.

Requires: pip install duckdb (or `python3 -m pip install duckdb`)

Exit code 0 = no hard failures (warnings may still be present, review them).
Exit code 1 = at least one hard failure.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parents[4] / "webapp" / "curriculum.js"

REQUIRED_FIELDS = ["id", "difficulty", "title", "concept", "tables", "prompt", "solutionSql", "hint", "starter"]
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

# Heuristic only -- flags candidates for a human/model review pass, not automatic
# failures. Some are legitimate (e.g. this curriculum's dbt/Snowflake style-guide
# modules, like teaching `::type` casts, intentionally name the syntax because
# naming it IS the lesson). Judge each hit against SKILL.md's "the leak test".
SYNTAX_LEAK_TERMS = [
    r"\bpivot\b", r"\bqualify\b", r"\bwindow function\b", r"\brank\(\)", r"\bdense_rank\(\)",
    r"\brow_number\(\)", r"\bpercent_rank\(\)", r"\blag\(", r"\blead\(", r"\bpartition by\b",
    r"\bover\s*\(", r"\brecursive\b", r"\bunion all\b", r"\bself[- ]join\b",
    r"\bfull outer join\b", r"\bleft join\b", r"\bright join\b", r"\binner join\b",
]
DEPENDENCY_TERMS = [
    r"\bsame as\b", r"\bas before\b", r"\bprevious (exercise|module|question|lesson)\b",
    r"\brebuild the same\b", r"\bearlier (exercise|module|question)\b",
    r"\bfrom (the )?last (module|exercise|question)\b", r"\bas in module\b", r"\bas in lesson\b",
    r"\brepeat the\b", r"\bonce more\b", r"\breusing the\b", r"\bthis time\b",
]


def extract_between(content, start_marker, end_marker):
    start = content.index(start_marker)
    end = content.index(end_marker, start)
    return content[start:end]


def parse_blocks(text):
    """Regex-based module parsing (schemaSql is a JS identifier ref like
    SCHEMAS.foo, not a JSON string, so this can't be a plain json.loads)."""
    blocks = re.split(r"\n  \{\n", text)
    out = []
    for b in blocks[1:]:
        fields = {}
        for key in ["id", "family", "difficulty", "title", "concept", "tables", "prompt", "hint", "starter"]:
            m = re.search(r'"' + key + r'":\s*"((?:[^"\\]|\\.)*)"', b)
            if m:
                fields[key] = m.group(1).encode().decode("unicode_escape")
        # schemaSql: either a template-literal string or a SCHEMAS.xxx / EXTRA_SCHEMAS.xxx reference
        m = re.search(r'"schemaSql":\s*`([\s\S]*?)`,\n', b)
        if m:
            fields["schemaSql_literal"] = m.group(1)
        else:
            m = re.search(r'"schemaSql":\s*((?:EXTRA_)?SCHEMAS\.\w+)', b)
            if m:
                fields["schemaSql_ref"] = m.group(1)
        # solutionSql: template literal or plain JSON string
        m = re.search(r'"solutionSql":\s*`([\s\S]*?)`,\n', b)
        if m:
            fields["solutionSql"] = m.group(1)
        else:
            m = re.search(r'"solutionSql":\s*"((?:[^"\\]|\\.)*)"', b)
            if m:
                fields["solutionSql"] = m.group(1).encode().decode("unicode_escape")
        out.append(fields)
    return out


def resolve_schema_map(content, block_name):
    """Parse a `const NAME = { key: \`sql\`, ... };` block into {key: sql}."""
    start = content.index(f"const {block_name} = {{")
    end = content.index("\n};", start)
    block = content[start:end]
    out = {}
    for m in re.finditer(r"(\w+):\s*`([\s\S]*?)`,", block):
        out[m.group(1)] = m.group(2)
    return out


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1

    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("ERROR: the `duckdb` python package is required (pip install duckdb)", file=sys.stderr)
        return 1
    import duckdb

    content = path.read_text()

    schemas = resolve_schema_map(content, "SCHEMAS")
    extra_schemas = resolve_schema_map(content, "EXTRA_SCHEMAS")

    modules_text = extract_between(content, "const MODULES = [", "const EXTRA_SCHEMAS")
    extra_text = extract_between(content, "const EXTRA_MODULES = [", "\nexport {")
    modules = parse_blocks(modules_text)
    extra_modules = parse_blocks(extra_text)
    all_modules = modules + extra_modules

    hard_failures = []
    warnings = []
    seen_ids = set()

    for mod in all_modules:
        mid = mod.get("id", "<no id>")

        # Duplicate id
        if mid in seen_ids:
            hard_failures.append(f"[{mid}] duplicate module id")
        seen_ids.add(mid)

        # Required fields present and non-empty
        for field in REQUIRED_FIELDS:
            if field == "solutionSql":
                if not mod.get("solutionSql", "").strip():
                    hard_failures.append(f"[{mid}] empty or missing solutionSql")
                continue
            if not mod.get(field, "").strip():
                hard_failures.append(f"[{mid}] empty or missing '{field}'")

        # Difficulty is one of the three valid values
        if mod.get("difficulty") not in VALID_DIFFICULTIES:
            hard_failures.append(f"[{mid}] invalid difficulty: {mod.get('difficulty')!r}")

        # schemaSql resolves to real SQL
        schema_sql = mod.get("schemaSql_literal")
        if schema_sql is None:
            ref = mod.get("schemaSql_ref")
            if ref is None:
                hard_failures.append(f"[{mid}] schemaSql field missing entirely")
                continue
            table, key = ref.split(".")
            table_map = extra_schemas if table == "EXTRA_SCHEMAS" else schemas
            schema_sql = table_map.get(key)
            if schema_sql is None:
                hard_failures.append(f"[{mid}] schemaSql reference {ref} does not resolve to any known schema")
                continue

        # DuckDB execution: schemaSql then solutionSql must both run without error
        solution_sql = mod.get("solutionSql", "")
        if schema_sql and solution_sql:
            con = duckdb.connect()
            try:
                con.execute(schema_sql)
                con.execute(solution_sql)
            except Exception as e:
                hard_failures.append(f"[{mid}] DuckDB execution failed: {e}")

        # Syntax-leak / cross-dependency heuristics (soft warnings, human judgment required)
        text_lower = (mod.get("title", "") + " " + mod.get("prompt", "")).lower()
        leak_hits = [p for p in SYNTAX_LEAK_TERMS if re.search(p, text_lower)]
        dep_hits = [p for p in DEPENDENCY_TERMS if re.search(p, text_lower)]
        if leak_hits:
            warnings.append(f"[{mid}] possible syntax leak in title/prompt: {leak_hits}")
        if dep_hits:
            warnings.append(f"[{mid}] possible cross-module dependency in title/prompt: {dep_hits}")

    print(f"Checked {len(all_modules)} modules ({len(modules)} track + {len(extra_modules)} extra).")
    print()

    if warnings:
        print(f"=== {len(warnings)} WARNING(S) (review manually, not auto-failed) ===")
        for w in warnings:
            print("  " + w)
        print()

    if hard_failures:
        print(f"=== {len(hard_failures)} HARD FAILURE(S) ===")
        for f in hard_failures:
            print("  " + f)
        print()
        print("FAILED.")
        return 1

    print("PASSED — no hard failures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
