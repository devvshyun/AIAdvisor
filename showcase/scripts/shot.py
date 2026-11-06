"""Screenshot a page at fixed sizes, for before/after pictures.

    python showcase/scripts/shot.py <url-or-html-file> <out-prefix> [--widths 1440,375]

Writes <out-prefix>-1440.png, <out-prefix>-375.png ... Uses the installed Chrome through Playwright for
Python (pip install playwright; no browser download needed with channel="chrome").
"""

import argparse
import os
import pathlib

from playwright.sync_api import sync_playwright

HEIGHT = {1440: 900, 1024: 768, 768: 1024, 375: 812}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("out")
    ap.add_argument("--widths", default="1440,375")
    ap.add_argument("--full", action="store_true", help="capture the whole page, not one screen")
    a = ap.parse_args()
    url = a.target if "://" in a.target else pathlib.Path(a.target).resolve().as_uri()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        for w in (int(x) for x in a.widths.split(",")):
            page = browser.new_page(viewport={"width": w, "height": HEIGHT.get(w, 900)})
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1500)
            path = f"{a.out}-{w}.png"
            page.screenshot(path=path, full_page=a.full)
            print(path)
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
