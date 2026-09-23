#!/usr/bin/env bash
# Builds SQL Dojo.app from the Swift sources here, without needing Xcode.app
# (this machine only has the Command Line Tools, whose swiftc/SDK are enough
# to compile against SwiftUI/WebKit/AppKit directly).
set -euo pipefail
cd "$(dirname "$0")"

APP_NAME="SQL Dojo"
BUILD_DIR="build"
APP_BUNDLE="${BUILD_DIR}/${APP_NAME}.app"

rm -rf "${BUILD_DIR}"
mkdir -p "${APP_BUNDLE}/Contents/MacOS" "${APP_BUNDLE}/Contents/Resources/sql-dojo"

echo "Compiling Swift sources..."
swiftc \
  Sources/SQLDojoApp.swift \
  Sources/ContentView.swift \
  Sources/LocalSchemeHandler.swift \
  Sources/DiagnosticLogger.swift \
  -o "${APP_BUNDLE}/Contents/MacOS/SQLDojo" \
  -sdk "$(xcrun --sdk macosx --show-sdk-path)" \
  -parse-as-library \
  -framework SwiftUI -framework WebKit -framework AppKit

echo "Copying Info.plist..."
cp Info.plist "${APP_BUNDLE}/Contents/Info.plist"

echo "Copying SQL Dojo web app resources (including vendored DuckDB-Wasm)..."
rsync -a --exclude='start.sh' --exclude='stop.sh' --exclude='server.py' --exclude='mac' \
  ../ "${APP_BUNDLE}/Contents/Resources/sql-dojo/"

echo "Ad-hoc code signing..."
codesign --force --deep --sign - "${APP_BUNDLE}"

echo
echo "Built: ${APP_BUNDLE}"
echo "Run with: open \"${APP_BUNDLE}\""
