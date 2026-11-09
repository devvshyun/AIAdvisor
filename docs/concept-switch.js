/* Concept switcher shared by docs/index.html (기본), docs/concept-a/ and docs/concept-b/.
   Each page loads it with <script src="…/concept-switch.js" data-concept="base|a|b" defer>.
   The pill lives in a shadow root so no page stylesheet reaches it, and the jump keeps the reader's
   place: every concept uses the same section ids (demo, how, kit, faq, guestbook). */
(() => {
  const me = document.currentScript;
  const current = me?.dataset.concept || "base";
  const root = current === "base" ? "./" : "../";
  const concepts = [
    { id: "base", label: "기본", href: root },
    { id: "a", label: "A", href: root + "concept-a/" },
    { id: "b", label: "B", href: root + "concept-b/" },
  ];
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
            border-radius: 999px; background: rgba(20, 22, 22, .86); color: #f2f2ee;
            box-shadow: 0 6px 24px rgba(0, 0, 0, .25); backdrop-filter: blur(8px);
            font: 500 13px/1 system-ui, "Pretendard Variable", "Apple SD Gothic Neo", sans-serif; }
      span { padding: 0 8px 0 10px; opacity: .7; }
      a { color: inherit; text-decoration: none; padding: 7px 11px; border-radius: 999px; }
      a[aria-current="page"] { background: #f2f2ee; color: #141616; }
      a:not([aria-current]):hover { background: rgba(255, 255, 255, .12); }
      a:focus-visible { outline: 2px solid #9fc7b8; outline-offset: 2px; }
      @media (prefers-reduced-motion: no-preference) { a { transition: background-color .14s ease; } }
    </style>
    <nav aria-label="디자인 컨셉 바꾸기"><span>컨셉</span>${concepts.map(c =>
      `<a href="${c.href}" data-id="${c.id}"${c.id === current ? ' aria-current="page"' : ""}>${c.label}</a>`).join("")}</nav>`;
  shadow.addEventListener("click", e => {
    const a = e.target.closest("a");
    if (!a || a.hasAttribute("aria-current")) return e.preventDefault();
    a.href = a.getAttribute("href") + place();
  });
  const add = () => document.body.appendChild(host);
  document.body ? add() : addEventListener("DOMContentLoaded", add);
})();
