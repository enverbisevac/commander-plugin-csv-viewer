#!/usr/bin/env python3
"""Commander CSV/TSV viewer plugin (protocol v1).

Invoked as:  csv_viewer.py <method> <paramsJson>
Prints:      {"ok": true, "kind": "table", "columns": [...], "rows": [[...]]}

Renders a delimited-text file as a real column/row table (the "table" viewer
kind). The delimiter is sniffed (comma / tab / semicolon / pipe); the first row
is treated as the header. Reads at most `maxBytes` so a giant CSV still previews
quickly.
"""
import csv
import io
import json
import os
import sys

MAX_ROWS = 500
MAX_COLS = 60
MAX_CELL = 500
DEFAULT_READ = 4 * 1024 * 1024


def fail(msg):
    print(json.dumps({"ok": False, "error": str(msg)}))
    sys.exit(0)


def clip(s):
    if s is None:
        return ""
    if len(s) > MAX_CELL:
        return s[:MAX_CELL] + "…"
    return s


def render(path, max_bytes):
    if not os.path.exists(path):
        fail("file not found")
    try:
        with open(path, "rb") as f:
            raw = f.read(max_bytes)
    except OSError as e:
        fail("cannot read file: %s" % e)
    text = raw.decode("utf-8", "replace")
    truncated_bytes = os.path.getsize(path) > len(raw)

    # Sniff the delimiter from a sample; fall back to comma / the extension.
    sample = text[:8192]
    delim = ","
    if path.lower().endswith(".tsv"):
        delim = "\t"
    else:
        try:
            delim = csv.Sniffer().sniff(sample, delimiters=",\t;|").delimiter
        except csv.Error:
            pass

    reader = csv.reader(io.StringIO(text), delimiter=delim)
    rows = []
    header = None
    row_truncated = False
    for i, row in enumerate(reader):
        if header is None:
            header = [clip(c) for c in row[:MAX_COLS]]
            continue
        if len(rows) >= MAX_ROWS:
            row_truncated = True
            break
        rows.append([clip(c) for c in row[:MAX_COLS]])

    if header is None:
        fail("empty file")

    # Pad/truncate every row to the header width so the grid stays rectangular.
    width = len(header)
    rows = [(r + [""] * width)[:width] for r in rows]

    fmt = {"\t": "TSV", ",": "CSV", ";": "CSV (;)", "|": "CSV (|)"}.get(delim, "CSV")
    out = {"ok": True, "kind": "table", "columns": header, "rows": rows, "meta": fmt}
    if row_truncated or truncated_bytes:
        out["note"] = "Showing the first %d rows." % MAX_ROWS
    print(json.dumps(out))


def main():
    if len(sys.argv) < 3:
        fail("usage: csv_viewer.py <method> <paramsJson>")
    method = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except (ValueError, IndexError):
        fail("bad params json")
    if method != "viewer.render":
        fail("unknown method: %s" % method)
    path = params.get("path")
    if not path:
        fail("no path")
    render(path, int(params.get("maxBytes", DEFAULT_READ)))


if __name__ == "__main__":
    main()
