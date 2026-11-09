KIND_ORDER = ["Added", "Changed", "Deprecated", "Removed", "Fixed"]


def render_changelog(entries):
    versions = {}
    for version, date, kind, text in entries:
        v = versions.setdefault(version, {"date": date, "kinds": {}})
        v["kinds"].setdefault(kind, []).append(text)
    blocks = []
    for version, info in versions.items():
        lines = [f"## [{version}] - {info['date']}"]
        for kind in KIND_ORDER:
            if kind in info["kinds"]:
                lines.append("")
                lines.append(f"### {kind}")
                lines.extend(f"- {t}" for t in info["kinds"][kind])
        blocks.append("\n".join(lines))
    if not blocks:
        return ""
    return "\n\n".join(blocks) + "\n"
