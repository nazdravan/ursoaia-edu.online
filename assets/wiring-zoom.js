// Zoom pe schemele de conectare Wokwi (<figure class="wiring">, generate de hooks/wokwi.py).
// Click / Enter pe schemă → ecran complet; zoom cu rotița, pinch, +/−, dublu-click;
// deplasare prin tragere sau săgeți; Esc / ✕ închide. Fără dependențe.
(function () {
  const figures = document.querySelectorAll("figure.wiring");
  if (!figures.length) return;

  const en = (document.documentElement.lang || "").toLowerCase().startsWith("en");
  const T = en
    ? { open: "Enlarge the wiring diagram", close: "Close", zoomIn: "Zoom in", zoomOut: "Zoom out",
        fit: "Fit to screen", hint: "Scroll or pinch to zoom · drag to move · Esc to close", dialog: "Wiring diagram" }
    : { open: "Mărește schema de conectare", close: "Închide", zoomIn: "Mărește", zoomOut: "Micșorează",
        fit: "Potrivește pe ecran", hint: "Rotiță sau două degete pentru zoom · trage pentru a muta · Esc pentru închidere",
        dialog: "Schema de conectare" };

  const MIN = 0.2, MAX = 8, STEP = 1.25;
  const icon = (d) =>
    `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" ` +
    `stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
  const ICONS = {
    expand: icon('<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>'),
    plus: icon('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M11 8v6M8 11h6"/>'),
    minus: icon('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M8 11h6"/>'),
    fit: icon('<path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/>'),
    close: icon('<path d="M18 6L6 18M6 6l12 12"/>'),
  };

  // ---- overlay (unul singur, refolosit) ----
  const overlay = document.createElement("div");
  overlay.className = "wiring-zoom";
  overlay.hidden = true;
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", T.dialog);
  overlay.innerHTML =
    '<div class="wiring-zoom__stage"><img class="wiring-zoom__img" alt="" draggable="false"></div>' +
    '<div class="wiring-zoom__bar">' +
    `<button type="button" data-act="out" aria-label="${T.zoomOut}" title="${T.zoomOut}">${ICONS.minus}</button>` +
    '<span class="wiring-zoom__pct" aria-live="polite">100%</span>' +
    `<button type="button" data-act="in" aria-label="${T.zoomIn}" title="${T.zoomIn}">${ICONS.plus}</button>` +
    `<button type="button" data-act="fit" aria-label="${T.fit}" title="${T.fit}">${ICONS.fit}</button>` +
    `<button type="button" data-act="close" aria-label="${T.close}" title="${T.close}">${ICONS.close}</button>` +
    "</div>" +
    `<p class="wiring-zoom__hint">${T.hint}</p>`;
  document.body.appendChild(overlay);

  const stage = overlay.querySelector(".wiring-zoom__stage");
  const img = overlay.querySelector(".wiring-zoom__img");
  const pct = overlay.querySelector(".wiring-zoom__pct");

  let scale = 1, tx = 0, ty = 0, fitScale = 1, natW = 1, natH = 1;
  let opener = null;

  function apply() {
    img.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
    pct.textContent = Math.round((scale / fitScale) * 100) + "%";
  }

  function fit() {
    const r = stage.getBoundingClientRect();
    fitScale = Math.min((r.width - 32) / natW, (r.height - 32) / natH);
    scale = fitScale;
    tx = (r.width - natW * scale) / 2;
    ty = (r.height - natH * scale) / 2;
    apply();
  }

  // zoom păstrând punctul (cx, cy) din stage sub cursor
  function zoomAt(factor, cx, cy) {
    const next = Math.min(Math.max(scale * factor, fitScale * MIN), fitScale * MAX);
    const k = next / scale;
    tx = cx - (cx - tx) * k;
    ty = cy - (cy - ty) * k;
    scale = next;
    apply();
  }

  function center() {
    const r = stage.getBoundingClientRect();
    return [r.width / 2, r.height / 2];
  }

  function open(fig) {
    const src = fig.querySelector("img");
    if (!src) return;
    opener = fig;
    natW = parseFloat(src.getAttribute("width")) || src.naturalWidth || 600;
    natH = parseFloat(src.getAttribute("height")) || src.naturalHeight || 400;
    img.src = src.currentSrc || src.src;
    img.alt = src.alt;
    img.style.width = natW + "px";
    img.style.height = natH + "px";
    overlay.hidden = false;
    document.documentElement.classList.add("wiring-zoom-open");
    fit();
    overlay.querySelector('[data-act="close"]').focus();
  }

  function close() {
    overlay.hidden = true;
    document.documentElement.classList.remove("wiring-zoom-open");
    img.removeAttribute("src");
    if (opener) opener.focus();
  }

  // ---- figurile de pe pagină devin butoane ----
  figures.forEach((fig) => {
    fig.tabIndex = 0;
    fig.setAttribute("role", "button");
    fig.setAttribute("aria-label", T.open);
    const badge = document.createElement("span");
    badge.className = "wiring__zoom-badge";
    badge.setAttribute("aria-hidden", "true");
    badge.innerHTML = ICONS.expand;
    fig.appendChild(badge);
    fig.addEventListener("click", (e) => {
      if (e.target.closest("a")) return; // linkul „Simulează în Wokwi” rămâne link
      open(fig);
    });
    fig.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(fig); }
    });
  });

  // ---- butoane ----
  overlay.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-act]");
    if (btn) {
      const [cx, cy] = center();
      const act = btn.dataset.act;
      if (act === "in") zoomAt(STEP, cx, cy);
      else if (act === "out") zoomAt(1 / STEP, cx, cy);
      else if (act === "fit") fit();
      else close();
      return;
    }
    if (dragged) { dragged = false; return; } // sfârșitul unei trageri nu e click
    if (e.target === stage || e.target === overlay) close(); // click pe fundal
  });

  // ---- tastatură ----
  overlay.addEventListener("keydown", (e) => {
    const [cx, cy] = center();
    const move = 60;
    switch (e.key) {
      case "Escape": close(); break;
      case "+": case "=": zoomAt(STEP, cx, cy); break;
      case "-": case "_": zoomAt(1 / STEP, cx, cy); break;
      case "0": fit(); break;
      case "ArrowLeft": tx += move; apply(); break;
      case "ArrowRight": tx -= move; apply(); break;
      case "ArrowUp": ty += move; apply(); break;
      case "ArrowDown": ty -= move; apply(); break;
      case "Tab": { // focusul rămâne în dialog
        const btns = [...overlay.querySelectorAll("button")];
        const i = btns.indexOf(document.activeElement);
        const next = e.shiftKey ? (i <= 0 ? btns.length - 1 : i - 1) : (i + 1) % btns.length;
        btns[next].focus();
        break;
      }
      default: return;
    }
    e.preventDefault();
  });

  // ---- rotiță / trackpad ----
  stage.addEventListener("wheel", (e) => {
    e.preventDefault();
    const r = stage.getBoundingClientRect();
    const factor = Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.002));
    zoomAt(factor, e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });

  stage.addEventListener("dblclick", (e) => {
    const r = stage.getBoundingClientRect();
    if (scale > fitScale * 1.5) fit();
    else zoomAt(2.5, e.clientX - r.left, e.clientY - r.top);
  });

  // ---- tragere și pinch (pointer events: mouse, touch, pen) ----
  const pts = new Map();
  let last = null; // {x, y, dist}
  let dragged = false, travel = 0;
  const snapshot = () => {
    const p = [...pts.values()];
    if (p.length === 1) return { x: p[0].x, y: p[0].y, dist: 0 };
    return { x: (p[0].x + p[1].x) / 2, y: (p[0].y + p[1].y) / 2,
             dist: Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y) };
  };
  stage.addEventListener("pointerdown", (e) => {
    try { stage.setPointerCapture(e.pointerId); } catch (_) { /* pointer deja eliberat */ }
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    last = snapshot();
    travel = 0;
    dragged = false;
    stage.classList.add("is-dragging");
  });
  stage.addEventListener("pointermove", (e) => {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const now = snapshot();
    travel += Math.abs(now.x - last.x) + Math.abs(now.y - last.y);
    if (travel > 4) dragged = true;
    tx += now.x - last.x;
    ty += now.y - last.y;
    if (pts.size > 1 && last.dist && now.dist) {
      const r = stage.getBoundingClientRect();
      zoomAt(now.dist / last.dist, now.x - r.left, now.y - r.top);
    } else {
      apply();
    }
    last = now;
  });
  const up = (e) => {
    pts.delete(e.pointerId);
    last = pts.size ? snapshot() : null;
    if (!pts.size) stage.classList.remove("is-dragging");
  };
  stage.addEventListener("pointerup", up);
  stage.addEventListener("pointercancel", up);

  window.addEventListener("resize", () => { if (!overlay.hidden) fit(); });
})();
