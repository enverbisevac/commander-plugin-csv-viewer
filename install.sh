#!/bin/sh
set -eu

case "$(uname -s)" in
  Darwin) destination="$HOME/Library/Application Support/Commander/plugins/csv-viewer" ;;
  Linux) destination="${XDG_DATA_HOME:-$HOME/.local/share}/commander/plugins/csv-viewer" ;;
  *) echo "On Windows, copy this folder to %APPDATA%\\Commander\\plugins\\csv-viewer" >&2; exit 1 ;;
esac

mkdir -p "$destination"
cp "$(dirname "$0")/plugin.json" "$(dirname "$0")/csv_viewer.py" "$destination/"
echo "Installed csv-viewer in $destination"
