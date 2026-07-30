#!/bin/sh
set -e

COMPONENT="${1:-patch}"
CHANGELOG="debian/changelog"
SETUP_PY="setup.py"

CURRENT=$(head -1 "$CHANGELOG" | sed -n 's/.*(\([0-9.]*\)-.*/\1/p')
MAJOR=$(echo "$CURRENT" | cut -d. -f1)
MINOR=$(echo "$CURRENT" | cut -d. -f2)
PATCH=$(echo "$CURRENT" | cut -d. -f3)

case "$COMPONENT" in
    major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
    minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
    patch) PATCH=$((PATCH + 1)) ;;
    *) echo "Usage: $0 [major|minor|patch]"; exit 1 ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
DEB_VERSION="${NEW_VERSION}-1"
DATE=$(date -R)

echo "Bumping version: $CURRENT -> $NEW_VERSION"

tmp=$(mktemp)
cat > "$tmp" <<EOF
anyfile-to-markdown (${DEB_VERSION}) unstable; urgency=medium

  * Automatic version bump.

 -- stas <stas@example.com>  ${DATE}

EOF
cat "$CHANGELOG" >> "$tmp"
mv "$tmp" "$CHANGELOG"

sed -i "s/version=\"${CURRENT}\"/version=\"${NEW_VERSION}\"/" "$SETUP_PY"

echo "Done. New version: $NEW_VERSION (deb: $DEB_VERSION)"
