#!/usr/bin/env bash
# Cut a new release of instagram-carousel-skills (super-board style).
#
#   ./scripts/release.sh 0.2.0            # bump versions, tag, build zip, create GH release
#   ./scripts/release.sh 0.2.0 --dry-run  # show what would happen; touch nothing
#
# Before running: add a "## v<version> — <date>" section to RELEASE-NOTES.md describing the
# changes. This script reads that section verbatim as the GitHub release body.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

VERSION="${1:-}"
DRY_RUN=0
[[ "${2:-}" == "--dry-run" || "${1:-}" == "--dry-run" ]] && DRY_RUN=1
[[ "$VERSION" == "--dry-run" ]] && VERSION=""

REPO_SLUG="EricTechPro/instagram-carousel-skills"
SKILLS=(instagram-carousel-plan instagram-carousel-generate)

die() { echo "✗ $*" >&2; exit 1; }
run() { if [[ "$DRY_RUN" == "1" ]]; then echo "  [dry-run] $*"; else eval "$*"; fi; }

# --- validate --------------------------------------------------------------
[[ -n "$VERSION" ]] || die "usage: ./scripts/release.sh <version> [--dry-run]   (e.g. 0.2.0)"
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "version must be semver, e.g. 0.2.0 (got '$VERSION')"
TAG="v$VERSION"

command -v gh >/dev/null || die "gh CLI not found"
command -v zip >/dev/null || die "zip not found"
gh auth status >/dev/null 2>&1 || die "gh not authenticated → gh auth login"

git rev-parse --git-dir >/dev/null 2>&1 || die "not a git repo"
if [[ "$DRY_RUN" == "0" && -n "$(git status --porcelain)" ]]; then
  die "working tree is dirty — commit or stash first (release.sh commits the version bump itself)"
fi
git rev-parse "$TAG" >/dev/null 2>&1 && die "tag $TAG already exists"
gh release view "$TAG" --repo "$REPO_SLUG" >/dev/null 2>&1 && die "release $TAG already exists"

# --- require a RELEASE-NOTES section for this version ----------------------
NOTES_FILE="$REPO_ROOT/RELEASE-NOTES.md"
grep -q "^## $TAG " "$NOTES_FILE" 2>/dev/null \
  || die "no '## $TAG — <date>' section in RELEASE-NOTES.md — add one first, then re-run"

# extract just this version's section (## vX.Y.Z … up to the next '## v' or EOF)
SECTION="$(awk -v tag="## $TAG " '
  $0 ~ "^" tag {grab=1}
  grab && /^## v/ && $0 !~ "^" tag {exit}
  grab {print}
' "$NOTES_FILE")"
[[ -n "$SECTION" ]] || die "could not extract release notes for $TAG"

echo "Releasing $TAG"
echo "── notes ──────────────────────────────────────────"
echo "$SECTION" | head -8
echo "…"
echo "───────────────────────────────────────────────────"

# --- bump VERSION files + manifests ----------------------------------------
if [[ "$DRY_RUN" == "0" ]]; then
  echo "$VERSION" > VERSION
  for s in "${SKILLS[@]}"; do echo "$VERSION" > "skills/$s/VERSION"; done
  # sync plugin.json + marketplace.json "version"
  python3 - "$VERSION" <<'PY'
import json, sys, pathlib
v = sys.argv[1]
for p in ("./.claude-plugin/plugin.json", "./marketplace.json"):
    path = pathlib.Path(p)
    data = json.loads(path.read_text())
    if "version" in data:
        data["version"] = v
    for plug in data.get("plugins", []):
        plug["version"] = v
    path.write_text(json.dumps(data, indent=2) + "\n")
print("  ✓ synced plugin.json + marketplace.json")
PY
else
  echo "  [dry-run] would set VERSION + skills/*/VERSION + manifests to $VERSION"
fi

# --- build the release zip (unzips into .claude/) --------------------------
ZIP="/tmp/instagram-carousel-skills-$TAG.zip"
STAGE="$(mktemp -d)"
mkdir -p "$STAGE/skills" "$STAGE/instagram-carousel"
for s in "${SKILLS[@]}"; do cp -R "skills/$s" "$STAGE/skills/"; done
cp -R assets character-references "$STAGE/instagram-carousel/"
find "$STAGE" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
find "$STAGE" \( -name '*.pyc' -o -name '.DS_Store' \) -delete 2>/dev/null || true
rm -f "$ZIP"
( cd "$STAGE" && zip -qr "$ZIP" skills instagram-carousel )
echo "  ✓ built $ZIP ($(du -h "$ZIP" | cut -f1))"

# --- commit, tag, push, release --------------------------------------------
run "git add -A"
run "git commit -q -m 'release: $TAG'"
run "git tag -a '$TAG' -m '$TAG'"
run "git push origin HEAD"
run "git push origin '$TAG'"
if [[ "$DRY_RUN" == "1" ]]; then
  echo "  [dry-run] gh release create $TAG <zip> --notes '<section>'"
else
  printf '%s\n' "$SECTION" > /tmp/ig-release-notes-$TAG.md
  gh release create "$TAG" "$ZIP" --repo "$REPO_SLUG" \
    --title "$TAG — $(echo "$SECTION" | head -1 | sed "s/^## $TAG — //")" \
    --notes-file /tmp/ig-release-notes-$TAG.md
fi

echo "✓ $TAG released → https://github.com/$REPO_SLUG/releases/tag/$TAG"
