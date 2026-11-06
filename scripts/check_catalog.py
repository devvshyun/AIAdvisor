"""Check the tool catalog: format and whether each repo is still maintained.

    python scripts/check_catalog.py --validate [files...]    keys, types, ids, overlaps, recipe tool ids
    python scripts/check_catalog.py --freshness [files...]   GitHub API: archived, last push, stars
    python scripts/check_catalog.py --freshness --report out.md   also write a Markdown report

With no files, every references/catalog/*.yaml is checked. Exit code 1 when a check fails, so CI
can open an issue. Set GITHUB_TOKEN to avoid the API's low anonymous rate limit.
"""
import datetime as dt
import glob
import json
import os
import re
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "references", "catalog")
REQUIRED = ["id", "name", "kind", "area", "what", "when", "not_when", "install", "verify", "docs",
            "maintained", "cost", "risks", "source_checked", "sources"]
OPTIONAL = ["repo", "license", "stars", "last_push", "needs", "overlaps", "also", "always_on_tokens"]
KINDS = {"skill", "plugin", "mcp", "cli", "built-in", "github-action", "service"}
AREAS = {"web-design", "coding", "automation"}
STALE_DAYS = 180


def load(paths):
    items = []
    for p in paths:
        data = yaml.safe_load(open(p, encoding="utf-8")) or []
        for it in data:
            it["_file"] = os.path.relpath(p, ROOT)
            items.append(it)
    return items


def validate(items):
    errors, ids = [], {}
    for it in items:
        where = f'{it.get("_file")}:{it.get("id", "?")}'
        for k in REQUIRED:
            if it.get(k) in (None, "", []):
                errors.append(f"{where}: missing {k}")
        unknown = set(it) - set(REQUIRED) - set(OPTIONAL) - {"_file"}
        if unknown:
            errors.append(f"{where}: unknown keys {sorted(unknown)}")
        if it.get("kind") not in KINDS:
            errors.append(f"{where}: kind {it.get('kind')!r} not in {sorted(KINDS)}")
        if it.get("area") not in AREAS:
            errors.append(f"{where}: area {it.get('area')!r} not in {sorted(AREAS)}")
        for a in it.get("also") or []:
            if a not in AREAS or a == it.get("area"):
                errors.append(f"{where}: also {a!r} must be another area from {sorted(AREAS)}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(it.get("id", ""))):
            errors.append(f"{where}: id must be lowercase letters, digits and hyphens")
        if it.get("id") in ids:
            errors.append(f"{where}: duplicate id (also in {ids[it['id']]})")
        ids[it.get("id")] = it.get("_file")
        for d in ("last_push", "source_checked"):
            v = it.get(d)
            if v and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v)):
                errors.append(f"{where}: {d} must be YYYY-MM-DD")
    for it in items:
        for o in it.get("overlaps") or []:
            if o not in ids:
                errors.append(f'{it["_file"]}:{it["id"]}: overlaps names unknown id {o!r}')
    errors += check_recipes(ids)
    return errors


def check_recipes(ids):
    """Every `id` on a recipe's '- 도구:' line must be a catalog id."""
    errors = []
    for p in sorted(glob.glob(os.path.join(ROOT, "references", "recipes", "*.md"))):
        for n, line in enumerate(open(p, encoding="utf-8"), 1):
            if line.lstrip().startswith("- 도구:"):
                for name in re.findall(r"`([^`]+)`", line):
                    if name not in ids:
                        errors.append(f"{os.path.relpath(p, ROOT)}:{n}: unknown tool id {name!r}")
    return errors


def repo_slug(url):
    m = re.match(r"https?://github\.com/([^/]+/[^/#?]+)", str(url or ""))
    return m.group(1).removesuffix(".git") if m else None


def freshness(items):
    token = os.environ.get("GITHUB_TOKEN")
    today = dt.date.today()
    rows, problems = [], []
    for it in items:
        slug = repo_slug(it.get("repo"))
        if not slug:
            rows.append((it["id"], "-", "-", "-", "no repo"))
            continue
        req = urllib.request.Request(f"https://api.github.com/repos/{slug}",
                                     headers={"User-Agent": "aiadvisor-catalog-check",
                                              **({"Authorization": f"Bearer {token}"} if token else {})})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=20))
        except Exception as e:  # moved, deleted or rate limited
            rows.append((it["id"], slug, "-", "-", f"lookup failed: {e}"))
            problems.append(f"{it['id']}: {slug} lookup failed ({e})")
            continue
        pushed = dt.date.fromisoformat(data["pushed_at"][:10])
        age = (today - pushed).days
        status = "archived" if data.get("archived") else ("stale" if age > STALE_DAYS else "ok")
        rows.append((it["id"], slug, data.get("stargazers_count"), str(pushed), status))
        if status != "ok":
            problems.append(f"{it['id']}: {slug} is {status} (last push {pushed}, {age} days)")
        if it.get("maintained") and status != "ok":
            problems.append(f"{it['id']}: catalog says maintained but repo is {status}")
    return rows, problems


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    report = None
    if "--report" in sys.argv:
        report = sys.argv[sys.argv.index("--report") + 1]
        args = [a for a in args if a != report]
    paths = args or sorted(glob.glob(os.path.join(CATALOG, "*.yaml")))
    items = load(paths)
    failed = False
    if "--validate" in sys.argv:
        errs = validate(items)
        print(f"validate: {len(items)} items, {len(errs)} problems")
        for e in errs:
            print("  " + e)
        failed |= bool(errs)
    if "--freshness" in sys.argv:
        rows, problems = freshness(items)
        print(f"freshness: {len(rows)} items, {len(problems)} problems")
        for p in problems:
            print("  " + p)
        if report:
            with open(report, "w", encoding="utf-8") as f:
                f.write(f"# Catalog freshness {dt.date.today()}\n\n| id | repo | stars | last push | status |\n|---|---|---:|---|---|\n")
                f.writelines(f"| {a} | {b} | {c} | {d} | {e} |\n" for a, b, c, d, e in rows)
                if problems:
                    f.write("\n## Needs attention\n\n" + "".join(f"- {p}\n" for p in problems))
        failed |= bool(problems)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
