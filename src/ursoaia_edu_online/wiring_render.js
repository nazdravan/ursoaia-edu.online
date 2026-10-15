// Rulat de Playwright cu page.evaluate(src, parts). Pagina are deja bundle-ul
// @wokwi/elements încărcat. Întoarce, pentru fiecare piesă, markup-ul SVG din
// shadow root, CSS-ul ei, dimensiunea randată și coordonatele pinilor.
async (parts) => {
  const out = [];
  for (const part of parts) {
    if (!customElements.get(part.type)) {
      throw new Error(`tip de piesă necunoscut: ${part.type} (${part.id})`);
    }
    const el = document.createElement(part.type);
    for (const [key, value] of Object.entries(part.attrs || {})) {
      el.setAttribute(key, String(value));
    }
    el.style.position = "absolute";
    document.body.appendChild(el);
    await el.updateComplete;
    // cel mai mare <svg> exterior din shadow root (wokwi-buzzer are întâi o notă muzicală ascunsă)
    const area = (s) => { const r = s.getBoundingClientRect(); return r.width * r.height; };
    const svg = el.shadowRoot && [...el.shadowRoot.querySelectorAll("svg")]
      .filter((s) => !s.parentElement || !s.parentElement.closest("svg"))
      .sort((a, b) => area(b) - area(a))[0];
    if (!svg) throw new Error(`piesa ${part.id} nu are <svg>`);
    let css = "";
    for (const sheet of el.shadowRoot.adoptedStyleSheets || []) {
      for (const rule of sheet.cssRules) css += rule.cssText + "\n";
    }
    for (const style of el.shadowRoot.querySelectorAll("style")) css += style.textContent + "\n";
    const rect = svg.getBoundingClientRect();
    out.push({
      id: part.id,
      width: rect.width,
      height: rect.height,
      // XMLSerializer, nu outerHTML: SVG-ul final e XML, iar outerHTML scrie entități HTML (&nbsp;)
      svg: new XMLSerializer().serializeToString(svg),
      css,
      pins: Object.fromEntries((el.pinInfo || []).map((p) => [p.name, [p.x, p.y]])),
    });
    el.remove();
  }
  return out;
}
