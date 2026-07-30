#!/bin/sh
set -e

APP_NAME="AnyFileToMarkdown"
DMG_NAME="${APP_NAME}-macOS.dmg"
VOLUME_NAME="${APP_NAME}"

# 1. PyInstaller bundle
pyinstaller --windowed --onefile \
    --name "$APP_NAME" \
    --icon icon.icns \
    --add-data "icons:icons" \
    --hidden-import markitdown \
    anyfile_to_markdown/app.py

# 2. Create .app bundle structure
APP_BUNDLE="dist/$APP_NAME.app"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

cat > "$APP_BUNDLE/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>com.bettal.anyfile-to-markdown</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.0</string>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIconFile</key>
    <string>icon</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>
EOF

cp icon.icns "$APP_BUNDLE/Contents/Resources/"

# 3. Create .dmg
if command -v create-dmg >/dev/null 2>&1; then
    create-dmg \
        --volname "$VOLUME_NAME" \
        --volicon icon.icns \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "$APP_NAME.app" 175 190 \
        --app-drop-link 425 190 \
        "$DMG_NAME" \
        "dist/$APP_NAME.app"
else
    echo "create-dmg not found, using hdiutil..."
    hdiutil create -volname "$VOLUME_NAME" -srcfolder "dist/$APP_NAME.app" -ov -format UDZO "$DMG_NAME"
fi

echo "Done: $DMG_NAME"
