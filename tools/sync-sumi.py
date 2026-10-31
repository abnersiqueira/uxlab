#!/usr/bin/env python3
"""Consolidate Sumi's 45 skills into uxlab domain skills.

Each source skill becomes a reference file inside a domain skill:
  skills/<src>/SKILL.md          -> skills/<domain>/references/<ref>.md
  skills/<src>/references/<f>    -> skills/<domain>/references/<ref>/<f>
Cross references are rewritten to the `domain/ref` notation (or real relative
links), Sumi branding becomes uxlab, and every derived file carries the
Apache-2.0 modification notice.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit("usage: sync-sumi.py <sumi-clone> <uxlab-root>")
SUMI = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
SUMI_SHA = subprocess.check_output(["git", "-C", str(SUMI), "rev-parse", "--short", "HEAD"], text=True).strip()
SUMI_VERSION = json.loads((SUMI / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]

DOMAINS = {
    "uxlab": ["sumi-orchestrator"],
    "ux-evaluation": [
        "nng-ux-heuristics", "cognitive-psychology-ux", "ux-ethics-content-strategy",
        "design-critique-case-studies", "ui-pattern-intelligence",
    ],
    "ux-research": ["ux-research-methods", "ux-metrics-measurement", "design-process-methods"],
    "visual-design": [
        "ui-visual-design-system", "visual-design-mastery", "typography-pairing-recipes",
        "color-palette-library", "shadow-elevation-density", "icon-illustration-systems",
        "image-media-patterns",
    ],
    "design-systems": [
        "design-systems-architecture", "design-token-presets", "component-patterns-code",
        "figma-design-tool-workflows",
    ],
    "layout-and-flows": [
        "layout-block-intelligence", "page-composition-engine", "responsive-block-patterns",
        "navigation-pattern-encyclopedia", "screen-flow-patterns",
    ],
    "forms-and-content": [
        "form-design-encyclopedia", "micro-copy-intelligence", "performance-states-patterns",
        "conversion-optimization-patterns",
    ],
    "motion": ["interaction-motion-design", "animation-recipe-library"],
    "accessibility-i18n": ["accessibility-inclusive-design", "cross-cultural-i18n-ux"],
    "data-viz": ["data-visualization-mastery", "desktop-app-design"],
    "platforms-and-ai": [
        "mobile-ux-design", "platform-visual-standards", "agentic-ai-generative-ux",
        "ai-spatial-voice-ux", "ambient-calm-zero-ui", "ai-design-generation",
    ],
    "references-and-sectors": [
        "reference-intelligence", "sector-style-intelligence", "design-memory",
        "business-design-templates",
    ],
}

# Reference names that differ from the Sumi skill name.
REF_NAME = {"sumi-orchestrator": "orchestrator"}
# File renames inside a skill's references/ folder.
FILE_RENAME = {"sumi-file-schemas.md": "uxlab-file-schemas.md"}
# Sumi commands renamed in uxlab.
COMMAND_RENAME = {"sumi": "help"}

OWNER = {s: d for d, skills in DOMAINS.items() for s in skills}
assert len(OWNER) == 45, len(OWNER)


def ref_name(src):
    return REF_NAME.get(src, src)


def notice(src_label, consolidated=True):
    mods = "consolidated into a domain skill, renamed, cross-references rewritten" if consolidated else "renamed, cross-references rewritten"
    return (
        f"<!-- Derived from Sumi {SUMI_VERSION} by Phazur Labs (Apache-2.0), {src_label}, "
        f"upstream commit {SUMI_SHA}. Modified by uxlab: {mods}. See NOTICE. -->\n"
    )


NOTATION = (
    "> Reference notation: `domain/name` is the file `references/name.md` of the "
    "`uxlab:domain` skill. Invoke that skill, then open the file.\n\n"
)


def notation_line(text):
    for src, dom in OWNER.items():
        if f"`{dom}/{ref_name(src)}`" in text:
            return NOTATION
    return ""


COMMANDS = sorted(p.stem for p in (SUMI / "commands").glob("*.md"))
NEW_CMD = {c: COMMAND_RENAME.get(c, c) for c in COMMANDS}


def rewrite(text, dest_dir, own_skill=None):
    """Rewrite one file's text. dest_dir is the directory the file will live in."""

    # 1. markdown links to sibling skills: ](../Y/SKILL.md) or ](../Y/)
    def sibling_link(m):
        target, anchor = m.group(1), m.group(2) or ""
        if target not in OWNER:
            return m.group(0)
        dest = OUT / "skills" / OWNER[target] / "references" / (ref_name(target) + ".md")
        return "](" + os.path.relpath(dest, dest_dir) + anchor + ")"

    text = re.sub(r"\]\(\.\./([a-z0-9-]+)/(?:SKILL\.md)?(#[^)]*)?\)", sibling_link, text)

    # 2. links to the skill's own references/: ](references/foo.md) -> ](<ref>/foo.md)
    if own_skill:
        text = re.sub(
            r"\]\(references/([^)]+)\)",
            lambda m: "](" + ref_name(own_skill) + "/" + FILE_RENAME.get(m.group(1), m.group(1)) + ")",
            text,
        )
        text = re.sub(
            r"`references/([A-Za-z0-9_.-]+\.md)`",
            lambda m: "`" + ref_name(own_skill) + "/" + FILE_RENAME.get(m.group(1), m.group(1)) + "`",
            text,
        )

    # 3. skill names -> domain/ref notation (backticked or bare)
    names = sorted(OWNER, key=len, reverse=True)
    alt = "|".join(re.escape(n) for n in names)
    text = re.sub(
        r"(?<![\w/.`\[(-])(`?)(" + alt + r")\1(?![\w/-]|\.md)",
        lambda m: f"`{OWNER[m.group(2)]}/{ref_name(m.group(2))}`",
        text,
    )

    # 4. commands: /audit -> /uxlab:audit
    cmd_alt = "|".join(re.escape(c) for c in sorted(COMMANDS, key=len, reverse=True))
    text = re.sub(
        r"(?<![\w/.:@<\"'=}\])-])/(" + cmd_alt + r")(?![\w/:-])",
        lambda m: "/uxlab:" + NEW_CMD[m.group(1)],
        text,
    )

    # 5. branding
    for old, new in FILE_RENAME.items():
        text = text.replace(old.replace(".md", ""), new.replace(".md", ""))
    text = text.replace(".sumi/", ".uxlab/").replace(".sumi", ".uxlab")
    text = text.replace("SUMI", "UXLAB").replace("Sumi", "uxlab").replace("sumi", "uxlab")

    # 6. capture runs through browser-harness (capture.sh), not puppeteer-core
    for a, b in (
        ('node "$UXLAB/scripts/capture.mjs"', '"$UXLAB/scripts/capture.sh"'),
        ("node scripts/capture.mjs", "scripts/capture.sh"),
        ("capture.mjs", "capture.sh"),
        ("Never drive puppeteer/Chrome MCP step by step to study a site.", "Never drive the browser step by step to study a site."),
        (
            "`capture.sh` needs `puppeteer-core` (resolved from the project, `$UXLAB_PUPPETEER_DIR`, or known\nsibling projects) and a local Chrome.",
            "`capture.sh` drives the browser through `browser-harness` (load that skill for setup). Third-party\nsites load in the browser it is attached to; set `BU_NAME` or `BU_CDP_URL` to use an isolated one.",
        ),
    ):
        text = text.replace(a, b)
    return text


def strip_frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    n_main = n_refs = n_other = 0
    for domain, skills in DOMAINS.items():
        base = OUT / "skills" / domain / "references"
        for src in skills:
            sdir = SUMI / "skills" / src
            body = strip_frontmatter((sdir / "SKILL.md").read_text(encoding="utf-8"))
            body = rewrite(body, base, own_skill=src).lstrip("\n")
            write(base / (ref_name(src) + ".md"), notice(f"skills/{src}/SKILL.md") + body)
            n_main += 1
            for f in sorted((sdir / "references").glob("*")) if (sdir / "references").exists() else []:
                dest = base / ref_name(src) / FILE_RENAME.get(f.name, f.name)
                if f.suffix == ".md":
                    text = rewrite(f.read_text(encoding="utf-8"), dest.parent)
                    write(dest, notice(f"skills/{src}/references/{f.name}") + text)
                    n_refs += 1
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest)
                    n_other += 1
            for extra in sdir.iterdir():
                if extra.name not in ("SKILL.md", "references"):
                    print("UNHANDLED extra in", src, extra.name)

    # commands
    for c in COMMANDS:
        text = rewrite((SUMI / "commands" / f"{c}.md").read_text(encoding="utf-8"), OUT / "commands")
        fm = re.match(r"^---\n.*?\n---\n", text, re.S)
        head, rest = (text[:fm.end()], text[fm.end():]) if fm else ("", text)
        head = re.sub(r"(?m)^name: .*$", f"name: {NEW_CMD[c]}", head)
        write(OUT / "commands" / f"{NEW_CMD[c]}.md", head + notice(f"commands/{c}.md", False) + notation_line(rest) + rest)

    # agents
    for f in sorted((SUMI / "agents").glob("*.md")):
        text = rewrite(f.read_text(encoding="utf-8"), OUT / "agents")
        fm = re.match(r"^---\n.*?\n---\n", text, re.S)
        head, rest = (text[:fm.end()], text[fm.end():]) if fm else ("", text)
        write(OUT / "agents" / f.name, head + notice(f"agents/{f.name}", False) + notation_line(rest) + rest)

    # node-only Awwwards scraper (no puppeteer)
    aw = rewrite((SUMI / "scripts" / "awwwards.mjs").read_text(encoding="utf-8"), OUT / "scripts")
    write(OUT / "scripts" / "awwwards.mjs", aw.replace("\n", "\n// Derived from Sumi " + SUMI_VERSION + " by Phazur Labs (Apache-2.0), scripts/awwwards.mjs, upstream commit " + SUMI_SHA + ". Modified by uxlab: renamed. See NOTICE.\n", 1))

    print(f"main refs: {n_main}, reference files: {n_refs}, other files: {n_other}, commands: {len(COMMANDS)}")


if __name__ == "__main__":
    sys.exit(main())
