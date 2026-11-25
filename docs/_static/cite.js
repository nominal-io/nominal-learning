// Citations are MyST footnotes: [^name] in the text, and [^name]: the source, collected at the bottom of the
// page. Hovering or focusing a citation's number shows its source at once, in a popup whose links work, as on
// Wikipedia. On a touch screen the first tap shows the popup and a second follows the number to the source list.
(() => {
  const REF = ".yue a.footnote-reference";
  if (!document.querySelector(REF)) return;

  const tip = document.createElement("div");
  tip.className = "cite-tip";
  tip.id = "cite-tip";
  tip.hidden = true;
  document.body.append(tip);

  const GAP = 6; // between the number and the popup
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
  // long enough to move the pointer from the number into the popup
  const hideSoon = () => {
    hideTimer = setTimeout(hide, 200);
  };

  // the footnote's text, without its label and backlinks
  const sourceOf = (ref) => {
    const note = document.getElementById(decodeURIComponent(ref.hash.slice(1)));
    if (!note) return null;
    const parts = [...note.children].filter((el) => !el.matches(".label, .backrefs"));
    return parts.map((el) => el.cloneNode(true));
  };

  const show = (ref) => {
    clearTimeout(hideTimer);
    if (current === ref) return;
    const source = sourceOf(ref);
    if (!source) return;
    hide();
    current = ref;
    tip.replaceChildren(...source);
    ref.setAttribute("aria-describedby", tip.id);
    tip.hidden = false;
    // under the number, or above it when there's no room below, and inside the window
    const box = ref.getBoundingClientRect();
    const view = document.documentElement;
    const { offsetWidth: width, offsetHeight: height } = tip;
    const left = Math.max(MARGIN, Math.min(box.left, view.clientWidth - MARGIN - width));
    const below = box.bottom + GAP + height <= view.clientHeight - MARGIN || box.top - GAP - height < MARGIN;
    tip.style.left = `${left + scrollX}px`;
    tip.style.top = `${(below ? box.bottom + GAP : box.top - GAP - height) + scrollY}px`;
  };

  document.addEventListener("pointerover", (e) => {
    if (e.pointerType !== "mouse") return;
    const ref = e.target.closest(REF);
    if (ref) show(ref);
    else if (tip.contains(e.target)) clearTimeout(hideTimer);
  });
  document.addEventListener("pointerout", (e) => {
    if (e.pointerType !== "mouse" || !current) return;
    const from = current.contains(e.target) ? current : tip.contains(e.target) ? tip : null;
    if (from && !from.contains(e.relatedTarget)) hideSoon();
  });

  document.addEventListener("focusin", (e) => {
    const ref = e.target.closest?.(REF);
    if (ref) show(ref);
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
    const ref = e.target.closest?.(REF);
    if (ref && touch && openAtTouch !== ref) {
      e.preventDefault();
      show(ref);
    } else if (!ref && !tip.contains(e.target)) {
      hide();
    }
    touch = false;
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") hide();
  });
  window.addEventListener("resize", hide);
})();
