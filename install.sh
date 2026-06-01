#!/usr/bin/env bash
# Install the Instagram Carousel skills into a Claude Code project (or globally).
#
#   ./install.sh            # install into $PWD/.claude/skills  (project install)
#   ./install.sh <dir>      # install into <dir>/.claude/skills
#   ./install.sh --global   # install into ~/.claude/skills      (all projects)
#
# Skills are auto-discovered from a project's .claude/skills/ (or ~/.claude/skills/).
# A bare clone is NOT auto-discovered — this script copies the skills + shared assets
# into the right place and wires up the runtime asset path.
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGET="$PWD"
GLOBAL=0
if [[ "${1:-}" == "--global" ]]; then GLOBAL=1; fi
if [[ -n "${1:-}" && "$1" != "--global" ]]; then TARGET="$1"; fi

if [[ "$GLOBAL" == "1" ]]; then
  SKILLS_DIR="$HOME/.claude/skills"
  ASSETS_DIR="$HOME/.claude/instagram-carousel"
else
  SKILLS_DIR="$TARGET/.claude/skills"
  ASSETS_DIR="$TARGET/.claude/instagram-carousel"
fi

echo "Installing Instagram Carousel skills"
echo "  from: $SRC_DIR"
echo "  into: $SKILLS_DIR"

mkdir -p "$SKILLS_DIR" "$ASSETS_DIR"

ok=1
for skill in instagram-carousel-plan instagram-carousel-generate; do
  if [[ -f "$SRC_DIR/skills/$skill/SKILL.md" ]]; then
    rm -rf "$SKILLS_DIR/$skill"
    cp -R "$SRC_DIR/skills/$skill" "$SKILLS_DIR/$skill"
    echo "  ✓ $skill"
  else
    echo "  ✗ $skill (SKILL.md missing)"; ok=0
  fi
done

# Shared assets the generate skill needs at runtime (style refs + logos + fonts).
# rm -rf first so re-running the installer replaces assets instead of nesting them
# (cp -R into an existing dir would create assets/assets, character-references/character-references).
rm -rf "$ASSETS_DIR/assets" "$ASSETS_DIR/character-references"
cp -R "$SRC_DIR/assets" "$ASSETS_DIR/assets"
cp -R "$SRC_DIR/character-references" "$ASSETS_DIR/character-references"
chmod +x "$SKILLS_DIR/instagram-carousel-generate/scripts/"*.py 2>/dev/null || true
echo "  ✓ assets -> $ASSETS_DIR"

cat <<EOF

Done. Two skills installed:
  • instagram-carousel-plan      — research + copywriting -> carousel-spec.md
  • instagram-carousel-generate  — spec -> 1080x1350 slides (HiggsField GPT Image 2)

Set this so the generate skill always finds the bundled assets:
  export IG_CAROUSEL_ASSETS="$ASSETS_DIR"

Then in Claude Code: "plan an instagram carousel for <topic>".
See README.md for HiggsField (CLI or MCP) setup.
EOF
[[ "$ok" == "1" ]] || { echo "Some skills failed to install."; exit 1; }
