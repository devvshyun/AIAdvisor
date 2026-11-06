"""Start a showcase folder for one catalog tool from the template.

    python showcase/scripts/new.py <catalog-id>

Creates showcase/<id>/README.md with the tool's name, kind and install command filled in from the
catalog. Refuses an id the catalog does not have, and never overwrites an existing README.
"""

import glob
import os
import sys
from datetime import date

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tool_id = sys.argv[1]
    items = {it["id"]: it for p in glob.glob(os.path.join(ROOT, "references", "catalog", "*.yaml"))
             for it in yaml.safe_load(open(p, encoding="utf-8")) or []}
    if tool_id not in items:
        sys.exit(f"'{tool_id}' is not a catalog id")
    it = items[tool_id]
    out = os.path.join(ROOT, "showcase", tool_id, "README.md")
    if os.path.exists(out):
        sys.exit(f"{out} already exists")
    text = open(os.path.join(ROOT, "showcase", "TEMPLATE.md"), encoding="utf-8").read()
    text = (text.replace("{{name}}", it["name"]).replace("{{id}}", tool_id).replace("{{kind}}", it["kind"])
                .replace("{{area}}", it["area"]).replace("{{date}}", date.today().isoformat())
                .replace("{{install}}", it["install"].strip()))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write(text)
    print(out)


if __name__ == "__main__":
    main()
