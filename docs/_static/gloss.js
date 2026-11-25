// Glossary terms ({gloss}, _ext/link_titles.py): hovering or focusing one shows its summary at once, in a
// popup that links to the glossary entry. The summary is the term's title, removed here so the browser's
// slower tooltip doesn't show as well. On a touch screen the first tap shows the popup and a second follows
// the term's link.
(() => {
  const TERM = ".yue a.gloss";
  const terms = document.querySelectorAll(`${TERM}[title]`);
  if (!terms.length) return;
  for (const term of terms) {
    term.dataset.gloss = term.title;
    term.removeAttribute("title");
  }

  const tip = document.createElement("div");
  tip.className = "gloss-tip";
  tip.id = "gloss-tip";
  tip.hidden = true;
  const summary = document.createElement("span");
  const link = document.createElement("a");
  link.textContent = "glossary";
  tip.append(summary, " (", link, ")");
  document.body.append(tip);

  const GAP = 6; // between the term and the popup
  const MARGIN = 16; // between the popup and the window's edges
  let current = null;
  let hideTimer;

  const hide = () => {
    clearTimeout(hideTimer);
    if (!current) return;
    current.removeAttribute("aria-describedby");
    current = null;
    tip.hidden = true;
  };
  // long enough to move the pointer from the term into the popup
  const hideSoon = () => {
    hideTimer = setTimeout(hide, 200);
  };

  const show = (term) => {
    clearTimeout(hideTimer);
    if (current === term) return;
    hide();
    current = term;
    summary.textContent = term.dataset.gloss;
    link.href = term.href;
    term.setAttribute("aria-describedby", tip.id);
    tip.hidden = false;
    // under the term's first line, or above it when there's no room below, and inside the window
    const line = term.getClientRects()[0];
    const view = document.documentElement;
    const { offsetWidth: width, offsetHeight: height } = tip;
    const left = Math.max(MARGIN, Math.min(line.left, view.clientWidth - MARGIN - width));
    const below = line.bottom + GAP + height <= view.clientHeight - MARGIN || line.top - GAP - height < MARGIN;
    tip.style.left = `${left + scrollX}px`;
    tip.style.top = `${(below ? line.bottom + GAP : line.top - GAP - height) + scrollY}px`;
  };

  document.addEventListener("pointerover", (e) => {
    if (e.pointerType !== "mouse") return;
    const term = e.target.closest(TERM);
    if (term) show(term);
    else if (tip.contains(e.target)) clearTimeout(hideTimer);
  });
  document.addEventListener("pointerout", (e) => {
    if (e.pointerType !== "mouse" || !current) return;
    const from = current.contains(e.target) ? current : tip.contains(e.target) ? tip : null;
    if (from && !from.contains(e.relatedTarget)) hideSoon();
  });

  document.addEventListener("focusin", (e) => {
    const term = e.target.closest?.(TERM);
    if (term) show(term);
  });
  document.addEventListener("focusout", (e) => {
    if (e.target === current && !tip.contains(e.relatedTarget)) hide();
  });

  let touch = false;
  let openAtTouch = null;
  document.addEventListener("pointerdown", (e) => {
    touch = e.pointerType !== "mouse";
    openAtTouch = current;
  });
  document.addEventListener("click", (e) => {
    const term = e.target.closest?.(TERM);
    if (term && touch && openAtTouch !== term) {
      e.preventDefault();
      show(term);
    } else if (!term && !tip.contains(e.target)) {
      hide();
    }
    touch = false;
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") hide();
  });
  window.addEventListener("resize", hide);
})();
