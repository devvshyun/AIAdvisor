"""Run one fixed prompt through headless Claude Code and keep what it cost.

    python showcase/scripts/measure.py --id graphify --label before --prompt code-tour --cwd . --runs 3
    python showcase/scripts/measure.py --id graphify --label after  --prompt code-tour --cwd . --runs 3 -- --settings x.json

--prompt is a section name in showcase/fixtures/prompts.md (the text of its first code block) or a
path to a text file. Anything after `--` goes to `claude` as is (--settings, --mcp-config, ...).
Each run is saved as showcase/<id>/runs/<label>-<n>.json; the summary is appended to
showcase/<id>/runs/summary.md and printed. Every run uses your Claude Code usage.
"""

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROMPTS = os.path.join(ROOT, "showcase", "fixtures", "prompts.md")


def load_prompt(name):
    if os.path.exists(name):
        return open(name, encoding="utf-8").read().strip()
    text = open(PROMPTS, encoding="utf-8").read()
    m = re.search(rf"^## {re.escape(name)}\b.*?```\n(.*?)\n```", text, re.S | re.M)
    if not m:
        sys.exit(f"no prompt section '{name}' in {PROMPTS}")
    return m.group(1).strip()


def tokens(usage):
    total_in = sum(usage.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return total_in, usage.get("output_tokens", 0)


def main():
    argv = sys.argv[1:]
    extra = argv[argv.index("--") + 1:] if "--" in argv else []
    argv = argv[:argv.index("--")] if "--" in argv else argv
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--cwd", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--prefix", default="", help="text put before the prompt, e.g. '/caveman '")
    a = ap.parse_args(argv)

    claude = shutil.which("claude")
    if not claude:
        sys.exit("claude CLI not found on PATH")
    prompt = a.prefix + load_prompt(a.prompt)
    out_dir = os.path.join(ROOT, "showcase", a.id, "runs")
    os.makedirs(out_dir, exist_ok=True)

    rows = []
    for n in range(1, a.runs + 1):
        cmd = [claude, "-p", prompt, "--output-format", "json", "--no-session-persistence", *extra]
        start = time.time()
        done = subprocess.run(cmd, cwd=a.cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        wall = time.time() - start
        try:
            data = json.loads(done.stdout)
        except json.JSONDecodeError:
            sys.exit(f"run {n}: no JSON from claude (exit {done.returncode}): {done.stderr[:400]}")
        json.dump({"cmd": cmd[3:], "cwd": a.cwd, "wall_seconds": round(wall, 1), **data},
                  open(os.path.join(out_dir, f"{a.label}-{n}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        tin, tout = tokens(data.get("usage", {}))
        rows.append((tin, tout, data.get("num_turns", 0), data.get("total_cost_usd", 0.0), wall, data.get("is_error")))
        print(f"{a.label} #{n}: in {tin:,} / out {tout:,} tokens, {data.get('num_turns')} turns, {wall:.0f}s, error={data.get('is_error')}")

    med = lambda i: statistics.median(r[i] for r in rows)
    line = (f"| {a.label} | {a.prompt} | {len(rows)} | {med(0):,.0f} | {med(1):,.0f} | {med(2):.0f} | "
            f"{med(4):.0f}s | ${med(3):.3f} | {' '.join(extra) or '-'} |")
    summary = os.path.join(out_dir, "summary.md")
    if not os.path.exists(summary):
        open(summary, "w", encoding="utf-8").write(
            "| 라벨 | 프롬프트 | 횟수 | 입력 토큰(중앙값) | 출력 토큰 | 턴 | 시간 | 비용 | claude 추가 인자 |\n|---|---|---:|---:|---:|---:|---:|---:|---|\n")
    open(summary, "a", encoding="utf-8").write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
