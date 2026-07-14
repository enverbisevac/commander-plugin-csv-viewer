# CSV Viewer for Commander

A small, cross-platform [Commander](https://enver.bisevac.com/commander) protocol-v1
plugin that renders `.csv` and `.tsv` files as an aligned table in Quick View and the
F3 viewer instead of raw comma-separated text.

It uses Python's built-in `csv` module to sniff the delimiter and columns — no
third-party packages, so it runs the same on macOS, Linux, and Windows.

## Install

Python 3.9 or newer is recommended.

```sh
./install.sh
```

Restart Commander, then select a `.csv`/`.tsv` file and open Quick View or press F3.
The viewer reads local files only; the original file is never changed.

To install manually, copy this directory to Commander's user plugin folder:

- macOS: `~/Library/Application Support/Commander/plugins/csv-viewer`
- Linux: `${XDG_DATA_HOME:-~/.local/share}/commander/plugins/csv-viewer`
- Windows: `%APPDATA%\Commander\plugins\csv-viewer`

## Test and develop

Run the plugin directly against a file:

```sh
python3 csv_viewer.py viewer.render '{"path":"/absolute/path/data.csv"}'
```

The program writes exactly one JSON reply to stdout. Diagnostics belong on stderr.
A handled problem returns exit status 0 with `{"ok":false,"error":"..."}`, allowing
Commander to fall back safely.

## Protocol

Commander drives a plugin as a one-shot subprocess: `<exec...> <method> <paramsJson>`,
reading one JSON object from stdout. This plugin implements `viewer.render` and returns
Commander's `table` kind. The full wire protocol and catalog schema live in the
[Commander documentation](https://enver.bisevac.com/commander).

## Packaging

A marketplace entry points at a zip of `plugin.json` + the executable at its root, plus
the archive's SHA-256 checksum. The [commander-plugins](https://github.com/enverbisevac/commander-plugins)
catalog builds that automatically from the pinned submodule.

## License

MIT.
