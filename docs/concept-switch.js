/* Concept switcher shared by docs/index.html (기본), docs/concept-a/ and docs/concept-b/.
   Each page loads it with <script src="…/concept-switch.js" data-concept="base|a|b" defer>.
   The pill lives in a shadow root so no page stylesheet reaches it, and the jump keeps the reader's
   place: every concept uses the same section ids (demo, how, kit, faq, guestbook).
   Near the top of the page it shows all three choices; once the reader scrolls it folds into a small
   "컨셉 · A" button (bottom-right on phones) so it stops covering content, and opens again on
   click or keyboard. It does not open on hover: growing under the pointer would put a link where the
   reader is about to click. */
(() => {
  const me = document.currentScript;
  const current = me?.dataset.concept || "base";
  const root = current === "base" ? "./" : "../";
  const concepts = [
    { id: "base", label: "기본", href: root },
    { id: "a", label: "A", href: root + "concept-a/" },
    { id: "b", label: "B", href: root + "concept-b/" },
  ];
  const currentLabel = concepts.find(c => c.id === current).label;
  const SECTIONS = ["demo", "how", "kit", "faq", "guestbook"];

  // the section the reader is looking at: the last shared section whose top has passed 40% of the screen
  function place() {
    if (SECTIONS.includes(location.hash.slice(1))) return location.hash;
    let found = "";
    for (const id of SECTIONS) {
      const el = document.getElementById(id);
      if (el && el.getBoundingClientRect().top < innerHeight * 0.4) found = "#" + id;
    }
    return found;
  }

  const host = document.createElement("div");
  host.setAttribute("data-concept-switch", "");
  const shadow = host.attachShadow({ mode: "open" });
  shadow.innerHTML = `
    <style>
      nav { position: fixed; left: max(16px, env(safe-area-inset-left)); bottom: max(16px, env(safe-area-inset-bottom));
            z-index: 2147483000; display: flex; align-items: center; gap: 2px; padding: 4px;
            border-radius: 999px; background: rgba(20, 22, 22, .88); color: #f2f2ee;
            box-shadow: 0 6px 24px rgba(0, 0, 0, .25); backdrop-filter: blur(8px);
            font: 500 13px/1 "Pretendard Variable", Pretendard, system-ui, sans-serif; }
      @media (max-width: 639px) { nav { left: auto; right: max(16px, env(safe-area-inset-right)); } }
      span { padding: 0 8px 0 10px; color: rgba(242, 242, 238, .8); }
      a, button { all: unset; box-sizing: border-box; cursor: pointer; padding: 8px 12px; border-radius: 999px; color: inherit; }
      a[aria-current="page"] { background: #f2f2ee; color: #141616; }
      a:not([aria-current]):hover { background: rgba(255, 255, 255, .14); }
      a:focus-visible, button:focus-visible { outline: 2px solid #9fc7b8; outline-offset: 2px; }
      button { display: none; }
      nav.folded span, nav.folded a { display: none; }
      nav.folded button { display: inline-block; }
      @media (prefers-reduced-motion: no-preference) { a { transition: background-color .14s ease; } }
    </style>
    <nav aria-label="디자인 컨셉 바꾸기"><span>컨셉</span>${concepts.map(c =>
      `<a href="${c.href}" data-id="${c.id}"${c.id === current ? ' aria-current="page"' : ""}>${c.label}</a>`).join("")}
      <button type="button" aria-expanded="false" aria-label="디자인 컨셉 바꾸기, 지금 ${currentLabel}">컨셉 · ${currentLabel}</button></nav>`;

  const nav = shadow.querySelector("nav");
  const toggle = shadow.querySelector("button");
  let opened = false; // opened by the reader; stays open until they scroll on
  let openedAt = 0, openedTime = 0;
  const fold = () => {
    const shouldFold = scrollY > 160 && !opened && !nav.matches(":hover") && !shadow.activeElement;
    nav.classList.toggle("folded", shouldFold);
    toggle.setAttribute("aria-expanded", String(!shouldFold));
  };
  addEventListener("scroll", () => {
    // scrolling that is still coasting right after the open does not count as moving on
    if (opened && performance.now() - openedTime < 600) openedAt = scrollY;
    if (opened && Math.abs(scrollY - openedAt) > 240) opened = false;
    fold();
  }, { passive: true });
  nav.addEventListener("mouseleave", fold);
  nav.addEventListener("focusout", () => setTimeout(fold));
  toggle.addEventListener("click", e => {
    opened = true; openedAt = scrollY; openedTime = performance.now(); fold();
    // keyboard opens (detail 0) move focus into the choices; a mouse or touch open leaves focus alone,
    // so the pill can fold again once the reader scrolls on
    if (e.detail === 0) shadow.querySelector('a[aria-current="page"]').focus();
    else toggle.blur();
  });

  shadow.addEventListener("click", e => {
    const a = e.target.closest("a");
    if (!a) return;
    if (a.hasAttribute("aria-current")) return e.preventDefault();
    a.href = a.getAttribute("href") + place();
  });
  const add = () => { document.body.appendChild(host); fold(); };
  document.body ? add() : addEventListener("DOMContentLoaded", add);
})();
