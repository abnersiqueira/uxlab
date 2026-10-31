#!/usr/bin/env bash
# Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), scripts/capture.mjs, upstream commit 3a3693b.
# Modified by uxlab: CLI wrapper around the browser-harness driver capture.py. See NOTICE.
#
# Usage:
#   capture.sh <url> [url…] [--out .uxlab/refs] [--steps 4]
#   capture.sh --from .uxlab/refs/awwwards.json [--pick slug1,slug2]
#
# Captures each site on desktop and phone (screenshots plus measured design DNA)
# through browser-harness. Third-party sites load in the browser browser-harness
# is attached to; point BU_NAME / BU_CDP_URL at an isolated browser to keep them
# out of a signed-in profile.
set -euo pipefail

usage() {
  echo "usage: capture.sh <url> [url…] [--out .uxlab/refs] [--steps 4] | --from awwwards.json [--pick a,b]" >&2
  exit 1
}

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
urls=()
while [ $# -gt 0 ]; do
  case "$1" in
    --out)   [ $# -ge 2 ] || usage; export UXLAB_OUT="$2";   shift 2 ;;
    --steps) [ $# -ge 2 ] || usage; export UXLAB_STEPS="$2"; shift 2 ;;
    --from)  [ $# -ge 2 ] || usage; export UXLAB_FROM="$2";  shift 2 ;;
    --pick)  [ $# -ge 2 ] || usage; export UXLAB_PICK="$2";  shift 2 ;;
    -*) usage ;;
    *)  urls+=("$1"); shift ;;
  esac
done
[ "${#urls[@]}" -gt 0 ] || [ -n "${UXLAB_FROM:-}" ] || usage

if ! command -v browser-harness >/dev/null 2>&1; then
  echo "browser-harness not found. Install: https://github.com/browser-use/browser-harness/blob/main/install.md" >&2
  exit 2
fi

export UXLAB_URLS="${urls[*]:-}"
exec browser-harness < "$here/capture.py"
