# Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), scripts/capture.mjs, upstream commit 3a3693b.
# Modified by uxlab: driver rewritten for browser-harness (raw CDP) instead of puppeteer-core;
# the in-page JS (consent dismissal, DNA measurement) is unchanged. See NOTICE.
#
# uxlab reference capture, one browser-harness run over N live sites.
# For each URL: desktop + phone screenshots at scroll steps (real wheel events, so
# Lenis/Locomotive smooth-scroll sites actually move) and a measured design DNA
# (type, color, spacing, layout, radius, motion stack) written to dna.json.
#
# Run it through capture.sh, which turns flags into the env vars read here:
#   UXLAB_URLS   space-separated URLs
#   UXLAB_FROM   awwwards.json written by scripts/awwwards.mjs
#   UXLAB_PICK   comma-separated slugs to take from UXLAB_FROM
#   UXLAB_OUT    output root (default .uxlab/refs)
#   UXLAB_STEPS  screenshots per desktop viewport, 1-8 (default 4)
import base64
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

URLS = os.environ.get("UXLAB_URLS", "").split()
FROM = os.environ.get("UXLAB_FROM", "")
PICK = [s.strip() for s in os.environ.get("UXLAB_PICK", "").split(",") if s.strip()]
OUT_ROOT = os.path.abspath(os.environ.get("UXLAB_OUT") or ".uxlab/refs")
STEPS = max(1, min(int(os.environ.get("UXLAB_STEPS") or 4), 8))

PHONE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900, "dsf": 1, "mobile": False},
    "phone": {"width": 390, "height": 844, "dsf": 2, "mobile": True},
}

DISMISS_JS = r"""(() => {
    const re = /^(accept( all)?|allow( all)?|agree|i agree|got it|ok(ay)?|continue|enter( site)?|yes|i am (21|18)\+?|i'm (21|18)\+?|i am of (legal )?age)$/i;
    // Gates are often a clickable <div>, not a <button>: match any leaf element with a pointer cursor.
    const clickable = (e) => e.matches('button, a, [role="button"]') || getComputedStyle(e).cursor === 'pointer';
    const gate = [...document.querySelectorAll('button, a, [role="button"], div, span')]
      .find((e) => e.children.length <= 1 && re.test((e.textContent || '').trim()) && clickable(e));
    gate?.click();

    // Marketing popups ("15% off") and their scrims: fixed layers that cover the
    // viewport and either collect an email, embed an iframe, or are an empty dim.
    // A fixed <canvas> or a fixed layer holding real page content is left alone.
    const vw = innerWidth, vh = innerHeight;
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.position !== 'fixed' || cs.display === 'none' || el.tagName === 'CANVAS' || el.querySelector('canvas')) continue;
      const r = el.getBoundingClientRect();
      const cover = (Math.min(r.right, vw) - Math.max(r.left, 0)) * (Math.min(r.bottom, vh) - Math.max(r.top, 0)) / (vw * vh);
      if (cover < 0.2) continue;
      const email = el.querySelector('input[type="email"], input[name*="email" i]');
      const frame = el.tagName === 'IFRAME' || (el.querySelector('iframe') && !el.querySelector('main, section, article'));
      const scrim = !el.textContent.trim() && /rgba\(.+,\s*0?\.\d+\)/.test(cs.backgroundColor);
      const dialog = el.matches('[role="dialog"], [aria-modal="true"]') || /popup|modal|klaviyo|privy|newsletter/i.test(el.className + '' + el.id);
      if (email || frame || scrim || dialog) el.style.setProperty('display', 'none', 'important');
    }
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  })()"""

MEASURE_JS = r"""(function measureDNA() {
  const px = (v) => Math.round(parseFloat(v) || 0);
  const tally = (arr) => Object.entries(arr.reduce((m, k) => ((m[k] = (m[k] || 0) + 1), m), {}))
    .sort((a, b) => b[1] - a[1]);
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0.01;
  };
  const family = (f) => f.split(',')[0].replace(/["']/g, '').trim();
  const textStyle = (sel) => {
    const els = [...document.querySelectorAll(sel)].filter(visible).slice(0, 40);
    if (!els.length) return null;
    // Representative = the style that carries the most text overall, preferring
    // readable running text: a long uppercase 12px footnote is not the body face.
    const groups = new Map();
    for (const e of els) {
      const c = getComputedStyle(e);
      const key = `${c.fontFamily}|${c.fontSize}|${c.fontWeight}|${c.textTransform}`;
      const readable = c.textTransform !== 'uppercase' && parseFloat(c.fontSize) >= 14;
      const g = groups.get(key) || { el: e, chars: 0, readable };
      g.chars += (e.textContent || '').trim().length;
      groups.set(key, g);
    }
    const ranked = [...groups.values()].sort((a, b) => (b.readable - a.readable) || (b.chars - a.chars));
    const cs = getComputedStyle(ranked[0].el);
    return {
      family: family(cs.fontFamily),
      sizes: [...new Set(els.map((e) => px(getComputedStyle(e).fontSize)))].sort((a, b) => b - a).slice(0, 6),
      weight: cs.fontWeight,
      lineHeight: cs.lineHeight === 'normal' ? 'normal' : +(parseFloat(cs.lineHeight) / parseFloat(cs.fontSize)).toFixed(2),
      tracking: cs.letterSpacing === 'normal' ? '0' : `${(parseFloat(cs.letterSpacing) / parseFloat(cs.fontSize)).toFixed(3)}em`,
      transform: cs.textTransform,
      count: els.length,
    };
  };

  const all = [...document.querySelectorAll('body *')].filter(visible).slice(0, 4000);
  const area = (el) => { const r = el.getBoundingClientRect(); return r.width * r.height; };

  // Colors weighted by painted area (backgrounds) and by count (text).
  const bg = {};
  for (const el of all) {
    const c = getComputedStyle(el).backgroundColor;
    if (!c || c === 'rgba(0, 0, 0, 0)' || c === 'transparent') continue;
    bg[c] = (bg[c] || 0) + area(el);
  }
  const bodyBg = getComputedStyle(document.body).backgroundColor;
  const htmlBg = getComputedStyle(document.documentElement).backgroundColor;
  const pageBg = [bodyBg, htmlBg].find((c) => c && c !== 'rgba(0, 0, 0, 0)') || 'rgb(255, 255, 255)';
  const text = tally(all.filter((e) => e.childNodes.length && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()))
    .map((e) => getComputedStyle(e).color));

  const sections = [...document.querySelectorAll('main > *, body > section, main section, body > div > section, footer')]
    .filter(visible).slice(0, 30);
  const radii = tally(all.map((e) => getComputedStyle(e).borderTopLeftRadius).filter((r) => r !== '0px'));
  // Multi-property transitions repeat the same value per property; keep the first.
  const first = (v) => v.split(/,(?![^(]*\))/)[0].trim();
  const animated = all.filter((e) => getComputedStyle(e).transitionDuration !== '0s');
  const easings = tally(animated.map((e) => first(getComputedStyle(e).transitionTimingFunction)));
  const durations = tally(animated.map((e) => first(getComputedStyle(e).transitionDuration)));
  const widths = all.map((e) => getComputedStyle(e).maxWidth).filter((w) => w.endsWith('px'));

  const html = document.documentElement;
  const has = (cond) => { try { return !!cond(); } catch { return false; } };
  const scriptSrc = [...document.scripts].map((s) => s.src).join(' ');

  return {
    title: document.title,
    description: document.querySelector('meta[name="description"]')?.content || null,
    pageHeight: html.scrollHeight,
    sectionCount: sections.length,
    theme: (() => {
      const [r, g, b] = pageBg.match(/\d+/g).map(Number);
      return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 < 0.45 ? 'dark' : 'light';
    })(),
    type: {
      display: textStyle('h1'),
      heading: textStyle('h2, h3'),
      body: textStyle('p'),
      ui: textStyle('button, nav a, a[class*="btn"], a[class*="button"]'),
      loadedFaces: [...new Set([...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family.replace(/["']/g, '')} ${f.weight}`))].slice(0, 16),
    },
    color: {
      pageBackground: pageBg,
      backgrounds: Object.entries(bg).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([c, a]) => ({ color: c, share: +(a / (innerWidth * html.scrollHeight)).toFixed(3) })),
      text: text.slice(0, 6).map(([c, n]) => ({ color: c, count: n })),
    },
    spacing: {
      sectionPaddingY: [...new Set(sections.map((s) => px(getComputedStyle(s).paddingTop)).filter(Boolean))].sort((a, b) => a - b),
      sectionHeights: sections.map((s) => Math.round(s.getBoundingClientRect().height)),
      gaps: tally(all.map((e) => getComputedStyle(e).rowGap).filter((g) => g !== 'normal' && g !== '0px')).slice(0, 6),
    },
    layout: {
      viewport: innerWidth,
      containerMaxWidths: tally(widths).slice(0, 4),
      gridCount: all.filter((e) => getComputedStyle(e).display.includes('grid')).length,
      flexCount: all.filter((e) => getComputedStyle(e).display.includes('flex')).length,
      gridTemplates: tally(all.filter((e) => getComputedStyle(e).display.includes('grid'))
        .map((e) => getComputedStyle(e).gridTemplateColumns.split(' ').length + ' cols')).slice(0, 4),
    },
    shape: { radii: radii.slice(0, 5) },
    motion: {
      // Best-effort: libraries bundled as ES modules leave no global, so a false
      // here means "not detected", not "not used". Read the shots too.
      stack: {
        gsap: has(() => window.gsap) || /gsap/.test(scriptSrc),
        scrollTrigger: has(() => window.ScrollTrigger || window.gsap?.plugins?.scrollTrigger),
        lenis: has(() => window.lenis || window.Lenis) || html.classList.contains('lenis'),
        locomotive: html.classList.contains('has-scroll-smooth') || !!document.querySelector('[data-scroll-container]'),
        three: has(() => window.THREE || window.__THREE__),
        webgl: [...document.querySelectorAll('canvas')].some((c) => has(() => c.getContext('webgl2') || c.getContext('webgl'))),
        framer: !!document.querySelector('[data-framer-name], [data-framer-component-type]'),
        webflow: !!html.dataset.wfPage,
        barba: !!document.querySelector('[data-barba]'),
        swiper: !!document.querySelector('.swiper'),
        lottie: !!document.querySelector('lottie-player, dotlottie-player') || has(() => window.lottie),
      },
      canvases: document.querySelectorAll('canvas').length,
      videos: document.querySelectorAll('video').length,
      easings: easings.slice(0, 4),
      durations: durations.slice(0, 4),
    },
    counts: {
      images: document.images.length,
      links: document.links.length,
      buttons: document.querySelectorAll('button').length,
      forms: document.forms.length,
    },
  };
})()"""


def log(msg):
    print(msg, file=sys.stderr)


def slug_of(t):
    if t.get("slug"):
        return t["slug"]
    u = urlparse(t["url"])
    host = re.sub(r"^www\.", "", u.hostname or "")
    raw = f"{host}{'-' + str(u.port) if u.port else ''}{u.path}"
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", raw, flags=re.I)).lower()


def targets():
    out = [{"url": u} for u in URLS]
    if FROM:
        sites = json.load(open(FROM, encoding="utf-8")).get("sites", [])
        out += [s for s in sites if s.get("url") and (not PICK or s.get("slug") in PICK)]
    return out


def dismiss_consent():
    try:
        js(DISMISS_JS)
    except Exception:
        pass


def wheel_to(fraction):
    # Real wheel input: programmatic scrollTo is ignored by Lenis and Locomotive,
    # which is how a capture ends up with N copies of the hero.
    s = js("({height: document.documentElement.scrollHeight, vh: innerHeight, y: scrollY})")
    delta = max(0, (s["height"] - s["vh"]) * fraction) - s["y"]
    while abs(delta) > 40:
        step = (1 if delta > 0 else -1) * min(abs(delta), 400)
        scroll(200, 300, dy=step)
        time.sleep(0.09)
        delta -= step
    time.sleep(0.9)


def emulate(vp):
    cdp("Emulation.setDeviceMetricsOverride", width=vp["width"], height=vp["height"],
        deviceScaleFactor=vp["dsf"], mobile=vp["mobile"])
    cdp("Emulation.setTouchEmulationEnabled", enabled=vp["mobile"])
    cdp("Emulation.setUserAgentOverride", userAgent=PHONE_UA if vp["mobile"] else "")


def reset_emulation():
    for method, params in (("Emulation.clearDeviceMetricsOverride", {}),
                           ("Emulation.setTouchEmulationEnabled", {"enabled": False}),
                           ("Emulation.setUserAgentOverride", {"userAgent": ""})):
        try:
            cdp(method, **params)
        except Exception:
            pass


def shoot(path):
    r = cdp("Page.captureScreenshot", format="jpeg", quality=72, _response_timeout=60)
    with open(path, "wb") as f:
        f.write(base64.b64decode(r["data"]))


def capture(t):
    slug = slug_of(t)
    d = os.path.join(OUT_ROOT, slug)
    os.makedirs(d, exist_ok=True)
    rec = {"slug": slug, "url": t["url"], "source": t.get("source") or "url", "award": t.get("award"),
           "score": t.get("score"), "awwwards": t.get("awwwards"), "tags": t.get("tags") or [],
           "capturedAt": datetime.now(timezone.utc).isoformat(), "shots": [], "dna": {}}
    try:
        for name, vp in VIEWPORTS.items():
            emulate(vp)
            goto_url(t["url"])
            try:
                wait_for_load(45)
            except Exception:
                pass
            time.sleep(2.5)  # preloaders and intro animations on award sites run 1-3s
            dismiss_consent()
            time.sleep(0.4)
            n = STEPS if name == "desktop" else min(STEPS, 3)
            for i in range(n):
                frac = 0 if n == 1 else i / (n - 1)
                if i > 0:
                    wheel_to(frac)
                dismiss_consent()  # gates can appear late, after a preloader finishes
                fname = f"{name}-{i}.jpg"
                shoot(os.path.join(d, fname))
                rec["shots"].append(fname)
            wheel_to(0)  # measure at the end: every scroll-reveal has fired once
            rec["dna"][name] = js(MEASURE_JS)
        rec["ok"] = True
    except Exception as e:  # noqa: BLE001 - one bad site must not stop the run
        rec["ok"] = False
        rec["error"] = str(e)
    with open(os.path.join(d, "dna.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)
    log(f"{'ok ' if rec['ok'] else 'ERR'} {slug} ({len(rec['shots'])} shots)" + (f" - {rec['error']}" if rec.get("error") else ""))
    return {"slug": slug, "url": t["url"], "ok": rec["ok"], "shots": len(rec["shots"]), "error": rec.get("error")}


todo = targets()
if not todo:
    sys.exit("no targets: set UXLAB_URLS or UXLAB_FROM (use scripts/capture.sh)")

# A tab of our own, so a tab the user has open is never navigated or resized.
tab = cdp("Target.createTarget", url="about:blank", background=True)["targetId"]
switch_tab(tab)
summary = []
try:
    summary = [capture(t) for t in todo]
finally:
    reset_emulation()
    try:
        close_tab(tab)
    except Exception:
        pass
print(json.dumps({"outRoot": OUT_ROOT, "summary": summary}, indent=2))
