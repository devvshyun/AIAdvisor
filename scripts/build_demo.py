"""Rebuild the data-driven parts of the demo page from references/.

What it rewrites in docs/index.html:
  - the guide browser (#library): one tab per topic folder, every guide's title and one-line summary
  - every "가이드 N편" count on the page
It also writes references/INDEX.md: recipes, catalog ids, and the guide index the skill reads first.

Everything else in the page is hand-written and left alone. Run it after adding, removing or
editing a guide; the Pages workflow runs it too, so the deployed page always matches references/.

    python scripts/build_demo.py           rewrite docs/index.html
    python scripts/build_demo.py --check   exit 1 if the page is out of date (no write)
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "docs", "index.html")
REPO = "https://github.com/devvshyun/AIAdvisor/blob/main/references/"
INDEX = "https://github.com/devvshyun/AIAdvisor/blob/main/references/README.md"

# folder -> label, in page order; a new folder needs a line here
TOPICS = [
    ("01-skills-mcp", "스킬·MCP"), ("02-video-image", "영상·이미지"), ("03-automation", "자동화"),
    ("04-prompts", "프롬프트"), ("05-coding", "코딩"), ("06-cost-saving", "비용 절약"),
    ("07-study-research", "공부·리서치"), ("08-business", "비즈니스"), ("09-web-design", "웹 디자인"),
    ("10-writing", "글쓰기"), ("99-etc", "기타"),
]
e = html.escape


def guides(folder):
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "references", folder, "*.md"))):
        lines = open(path, encoding="utf-8").read().split("\n")
        title = lines[0].lstrip("# ").strip()
        summary = next((l.split(":", 1)[1].strip() for l in lines[:8] if "한 줄 요약" in l), "")
        summary = re.sub(r"`([^`]*)`", r"\1", summary)
        # a literal "[ ]" reads as a leftover placeholder to the kit's guard (system.js); full-width brackets say the same
        summary = re.sub(r"\[(\s*)\]", r"［\1］", summary)
        summary = re.sub(r"\s*\((?:\d{4}-\d{2}-\d{2}|갱신|읽는 데)[^)]*\)\s*$", "", summary)
        out.append((title, summary, f"{folder}/{os.path.basename(path)}"))
    return out


def library(data, total):
    tabs, panes = [], []
    for i, (folder, label) in enumerate(TOPICS):
        items = data[folder]
        first = i == 0
        selected = "true" if first else "false"
        tabindex = "" if first else ' tabindex="-1"'
        tabs.append(
            f'            <button class="topic" role="tab" type="button" id="tp-{folder}" aria-controls="gp-{folder}" '
            f'aria-selected="{selected}"{tabindex}>{e(label)}<span>{len(items)}편</span></button>')
        rows = "\n".join(
            f'              <li><a class="guide" href="{REPO}{e(p)}"><b>{e(t)}</b><span>{e(s)}</span></a></li>'
            for t, s, p in items)
        panes.append(
            f'          <div class="guides" role="tabpanel" id="gp-{folder}" aria-labelledby="tp-{folder}"{"" if first else " hidden"}>\n'
            f'            <ul>\n{rows}\n            </ul>\n          </div>')
    nl = "\n"
    return f'''  <section class="section" id="library" style="--hm: 2" aria-labelledby="library-h">
    <div class="wrap">
      <div class="grid">
        <h2 class="span-5" id="library-h">스킬에 들어 있는 가이드 {total}편</h2>
        <p class="span-6 start-7 muted">주제를 누르면 가이드마다 한 줄 요약이 나옵니다. 가이드를 누르면 GitHub에서 전문이 열립니다. <a class="link" href="{INDEX}">상황별 색인 열기</a></p>
      </div>
      <div class="grid fill lib">
        <div class="span-4 topics" role="tablist" aria-label="가이드 주제" aria-orientation="vertical">
{nl.join(tabs)}
        </div>
        <div class="span-8 start-5 lib__panes">
{nl.join(panes)}
        </div>
      </div>
    </div>
  </section>
'''


AREAS = [("web-design", "웹 디자인"), ("coding", "코딩"), ("automation", "자동화")]
NOTAB = ' tabindex="-1"'
KIND = {"skill": "스킬", "plugin": "플러그인", "mcp": "MCP", "cli": "CLI", "built-in": "내장",
        "github-action": "Actions", "service": "서비스"}


def catalog_items(area):
    """name, kind, what, maintained per entry, read with regexes (the Pages build has no PyYAML)."""
    text = open(os.path.join(ROOT, "references", "catalog", f"{area}.yaml"), encoding="utf-8").read()
    out = []
    for chunk in re.split(r"^- id: ", text, flags=re.M)[1:]:
        field = lambda k: (re.search(rf"^  {k}: (.*)$", chunk, re.M) or [None, ""])[1].strip().strip("'\"")
        out.append((field("name"), KIND.get(field("kind"), field("kind")), field("what"), field("maintained") != "false",
                    bool(re.search(r"^  hands_on: ", chunk, re.M))))
    return out


def recipe_steps(area):
    """Title and step headings; '## 레시피 N.' lines start a group (the automation file has two)."""
    lines = open(os.path.join(ROOT, "references", "recipes", f"{area}.md"), encoding="utf-8").read().split("\n")
    title = lines[0].lstrip("# ").removeprefix("레시피:").strip()
    groups, current = [], None
    for l in lines:
        if l.startswith("## 레시피"):
            current = (re.sub(r"^## 레시피 \d+\.\s*", "", l).strip(), []); groups.append(current)
        elif l.startswith("### "):
            if current is None:
                current = ("", []); groups.append(current)
            current[1].append(re.sub(r"^### \d+\.\s*", "", l).strip())
    return title, groups


def kit(total_tools):
    tabs, panes = [], []
    for i, (area, label) in enumerate(AREAS):
        items = catalog_items(area)
        title, groups = recipe_steps(area)
        first = i == 0
        tabs.append(
            f'            <button class="topic" role="tab" type="button" id="kt-{area}" aria-controls="kp-{area}" '
            f'aria-selected="{"true" if first else "false"}"{"" if first else NOTAB}>{e(label)}<span>{len(items)}개</span></button>')
        recipe = []
        for name, steps in groups:
            head = f'<p class="recipe__group">{e(name)}</p>' if name else ""
            # div lists, not ul/ol: the kit's layout check treats a page-level list as a column that must
            # start on a grid line, and these sit inside the pane
            recipe.append(head + '<div class="recipe__steps" role="list">'
                          + "".join(f'<div role="listitem">{e(s)}</div>' for s in steps) + "</div>")
        tools = "\n".join(
            f'              <div role="listitem" class="tool{"" if ok else " tool--off"}{" tool--tried" if tried else ""}"><b>{e(n)}</b><i>{e(k)}{"" if ok else " · 관리 중단"}{" · 써 봄" if tried else ""}</i><span>{e(w)}</span></div>'
            for n, k, w, ok, tried in items)
        panes.append(
            f'          <div class="kitp" role="tabpanel" id="kp-{area}" aria-labelledby="kt-{area}"{"" if first else " hidden"}>\n'
            f'            <div class="recipe"><a class="recipe__title" href="{REPO}recipes/{area}.md">{e(title)}</a>{"".join(recipe)}</div>\n'
            f'            <div class="tools" role="list">\n{tools}\n            </div>\n          </div>')
    nl = "\n"
    return f'''  <section class="section" id="kit" style="--hm: 2" aria-labelledby="kit-h">
    <div class="wrap">
      <div class="grid">
        <h2 class="span-5" id="kit-h">직접 확인한 도구 {total_tools}개와 레시피</h2>
        <p class="span-6 start-7 muted">자동화·코딩·웹 디자인은 공식 문서와 GitHub로 확인한 카탈로그로 추천하고, 도구를 엮는 순서는 레시피로 정해 둡니다. 번호를 고르면 레시피를 한 단계씩, 확인 기준을 보여 주며 진행합니다. <a class="link" href="{REPO}catalog/CHANGELOG.md">변경 기록 보기</a></p>
      </div>
      <div class="grid fill lib">
        <div class="span-4 topics" role="tablist" aria-label="분야" aria-orientation="vertical">
{nl.join(tabs)}
        </div>
        <div class="span-8 start-5 lib__panes">
{nl.join(panes)}
        </div>
      </div>
    </div>
  </section>
'''


def build(page):
    folders = sorted(d for d in os.listdir(os.path.join(ROOT, "references"))
                     if os.path.isdir(os.path.join(ROOT, "references", d)) and d not in ("catalog", "recipes"))
    missing = [d for d in folders if d not in dict(TOPICS)]
    if missing:
        sys.exit(f"topic folders without a label in TOPICS: {missing}")
    data = {f: guides(f) for f, _ in TOPICS}
    total = sum(len(v) for v in data.values())
    start = page.index('  <section class="section" id="library"')
    end = page.index("</section>\n", start) + len("</section>\n")
    page = page[:start] + library(data, total) + page[end:]
    page = re.sub(r"가이드 \d+편", f"가이드 {total}편", page)
    tools = sum(len(catalog_items(a)) for a, _ in AREAS)
    section = kit(tools)
    if 'id="kit"' in page:
        start = page.index('  <section class="section" id="kit"')
        end = page.index("</section>\n", start) + len("</section>\n")
        page = page[:start] + section + page[end:]
    else:  # first run: the catalog goes right before the guide library
        at = page.index('  <section class="section" id="library"')
        page = page[:at] + section + "\n" + page[at:]
    page = re.sub(r"검증한 도구 \d+개", f"검증한 도구 {tools}개", page)  # hero pill and nav only
    return page, total


INDEX_PATH = os.path.join(ROOT, "references", "INDEX.md")


def build_index():
    """references/INDEX.md: the small file SKILL.md reads first. The situational table and the
    overlapping-tools list are copied from references/README.md, then every guide's file name by
    folder, so the skill sees the whole library without loading every summary."""
    readme = open(os.path.join(ROOT, "references", "README.md"), encoding="utf-8").read()
    start = readme.index("## 상황별 빠른 찾기")
    end = readme.index("\n---", readme.index("## 여러 가이드에 반복해서 나오는 도구"))
    parts = ["# 색인 (스킬용)", "",
             "스킬이 먼저 읽는 작은 색인입니다. 자동화·코딩·웹 디자인은 레시피와 카탈로그부터 보고, 그 밖의 주제는 가이드 상황별 표로 후보를 고른 뒤 필요한 파일만 엽니다. "
             "가이드별 한 줄 요약이 필요하면 `README.md`의 주제별 목차를 봅니다. 이 파일은 `python scripts/build_demo.py`가 만듭니다.", ""]
    parts += catalog_section()
    parts += [readme[start:end].strip(), "", "## 가이드 전체 파일 목록", ""]
    for folder, label in TOPICS:
        names = [os.path.basename(p)[:-3] for p in sorted(glob.glob(os.path.join(ROOT, "references", folder, "*.md")))]
        parts.append(f"- **{label}** `{folder}/`: " + ", ".join(names))
    return "\n".join(parts) + "\n"


def catalog_section():
    """Recipes (title line) and catalog ids per area, read with regexes so the Pages build needs no PyYAML."""
    out = ["## 레시피", ""]
    for p in sorted(glob.glob(os.path.join(ROOT, "references", "recipes", "*.md"))):
        title = open(p, encoding="utf-8").readline().lstrip("# ").strip()
        out.append(f"- `recipes/{os.path.basename(p)}`: {title}")
    out += ["", "## 도구 카탈로그", "", "id 뒤 괄호는 종류, `+`는 함께 쓰이는 다른 분야(`also`), \"써 봄\"은 이 저장소 작업에서 직접 써 본 도구(`hands_on`)입니다. 자세한 내용은 해당 yaml에서 id로 찾습니다.", ""]
    for p in sorted(glob.glob(os.path.join(ROOT, "references", "catalog", "*.yaml"))):
        entries = re.split(r"^- id: ", open(p, encoding="utf-8").read(), flags=re.M)[1:]
        names = []
        for e in entries:
            id_ = e.splitlines()[0].strip()
            kind = re.search(r"^  kind: (\S+)", e, re.M).group(1)
            also = re.search(r"^  also: \[(.*)\]", e, re.M)
            stale = ", 관리 중단" if re.search(r"^  maintained: false", e, re.M) else ""
            tried = ", 써 봄" if re.search(r"^  hands_on: ", e, re.M) else ""
            names.append(f"`{id_}` ({kind}{', +' + also.group(1) if also else ''}{stale}{tried})")
        out.append(f"- `catalog/{os.path.basename(p)}` {len(names)}개: " + ", ".join(names))
    return out + [""]


def sync(path, text, check):
    before = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if before == text:
        return False
    if not check:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return True


if __name__ == "__main__":
    check = "--check" in sys.argv
    page, total = build(open(PAGE, encoding="utf-8").read())
    stale = [name for name, changed in (("docs/index.html", sync(PAGE, page, check)),
                                        ("references/INDEX.md", sync(INDEX_PATH, build_index(), check))) if changed]
    if check:
        if stale:
            sys.exit(f"out of date: {', '.join(stale)}. Run python scripts/build_demo.py")
        print(f"up to date ({total} guides)")
    else:
        print(f"{total} guides; rewrote: {', '.join(stale) if stale else 'nothing'}")
