#!/usr/bin/env python3
"""Generate uxlab scripts/capture.py (browser-harness) from Sumi's capture.mjs.

The in-page JS (consent dismissal, DNA measurement) is extracted verbatim from the
upstream script; the driver loop is rewritten for browser-harness (raw CDP).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit("usage: gen-capture.py <sumi-clone> <uxlab-root>")
SUMI = Path(sys.argv[1]).resolve()
SRC = (SUMI / "scripts" / "capture.mjs").read_text(encoding="utf-8")
OUT = Path(sys.argv[2]).resolve() / "scripts" / "capture.py"
SUMI_SHA = subprocess.check_output(["git", "-C", str(SUMI), "rev-parse", "--short", "HEAD"], text=True).strip()
SUMI_VERSION = json.loads((SUMI / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]

# Consent dismissal: the arrow function passed to page.evaluate(...) inside dismissConsent.
m = re.search(r"await page\.evaluate\((\(\) => \{.*?\n  \})\)\.catch", SRC, re.S)
dismiss = m.group(1)
# DNA measurement: function measureDNA() { ... } up to the puppeteer bootstrap.
m = re.search(r"(function measureDNA\(\) \{.*?\n\})\n\nconst puppeteer", SRC, re.S)
measure = m.group(1)

# Python raw strings keep JS backslashes (regexes) intact.
for name, body in (("dismiss", dismiss), ("measure", measure)):
    assert '"""' not in body, name

TEMPLATE = r'''# Derived from Sumi __VER__ by Phazur Labs (Apache-2.0), scripts/capture.mjs, upstream commit __SHA__.
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

DISMISS_JS = r"""(__DISMISS__)()"""

MEASURE_JS = r"""(__MEASURE__)()"""


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
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
text = TEMPLATE.replace("__DISMISS__", dismiss).replace("__MEASURE__", measure).replace("__VER__", SUMI_VERSION).replace("__SHA__", SUMI_SHA)
OUT.write_text(text, encoding="utf-8")
print("wrote", OUT, len(text), "bytes")
