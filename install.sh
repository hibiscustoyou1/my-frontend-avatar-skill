#!/bin/sh
# Install every skill in this repository into all supported agent harnesses.
#
# Canonical copies go to ~/.agents/skills/<name> (read natively by Codex,
# Cursor, Copilot, OpenCode's agent-compat layer, and DSH). Harness-specific
# roots get symlinks. <name> comes from each SKILL.md frontmatter.
#
# Usage:
#   sh install.sh                  # install all skills
#   ONLY=visual-assist sh install.sh    # install one skill
#   SKIP_CLAUDE=1 sh install.sh    # skip a harness
set -eu

REPO="$(cd "$(dirname "$0")" && pwd)"
CANON_DIR="${CANONICAL_DIR:-$HOME/.agents/skills}"
mkdir -p "$CANON_DIR"

frontmatter_name() {
  awk '/^---$/{n++; next} n==1 && /^name:/ {sub(/^name:[[:space:]]*/, ""); print; exit}' "$1"
}

link_into() {
  dest="$1"
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  ln -s "$2" "$dest"
  printf '    linked: %s\n' "$dest"
}

installed=0
for skill_dir in "$REPO"/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name="$(frontmatter_name "$skill_dir/SKILL.md")"
  [ -n "$name" ] || { echo "skip (no frontmatter name): $skill_dir" >&2; continue; }
  if [ -n "${ONLY:-}" ] && [ "$ONLY" != "$name" ]; then continue; fi

  target="$CANON_DIR/$name"
  rm -rf "$target"
  cp -R "$skill_dir" "$target"
  find "$target" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
  printf '  %s -> %s\n' "$name" "$target"

  [ "${SKIP_CLAUDE:-0}" = 1 ] || link_into "$HOME/.claude/skills/$name" "$target"
  [ "${SKIP_OPENCODE:-0}" = 1 ] || link_into "${OPENCODE_CONFIG:-$HOME/.config/opencode}/skills/$name" "$target"
  [ "${SKIP_COPILOT:-0}" = 1 ] || link_into "$HOME/.copilot/skills/$name" "$target"
  [ "${SKIP_CODEX:-0}" = 1 ] || link_into "$HOME/.codex/skills/$name" "$target"

  # DSH discovers ~/.agents natively; drop a stale direct copy to avoid duplicates.
  dsh_copy="${DSH_HOME:-$HOME/.dsh}/skills/$name"
  if [ -e "$dsh_copy" ] && [ ! -L "$dsh_copy" ]; then
    rm -rf "$dsh_copy"
    printf '    removed stale copy: %s\n' "$dsh_copy"
  fi
  installed=$((installed + 1))
done

[ "$installed" -gt 0 ] || { echo "no skills found" >&2; exit 1; }
printf 'done: %d skill(s) installed under %s\n' "$installed" "$CANON_DIR"
