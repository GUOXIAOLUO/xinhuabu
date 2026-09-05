#!/usr/bin/env python3
"""Create or validate an R4 source-record backup; never rewrites Canvas sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from workbench.application.canvas_source_backup import create_canvas_source_backup, validate_canvas_source_backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backup-dir", required=True, type=Path)
    parser.add_argument("--canvases-dir", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        if args.canvases_dir is not None:
            parser.error("--canvases-dir is not used with --verify")
        report = validate_canvas_source_backup(args.backup_dir)
    else:
        if args.canvases_dir is None:
            parser.error("--canvases-dir is required when creating a backup")
        report = create_canvas_source_backup(args.canvases_dir, args.backup_dir)
    print(f"backup={report.backup_directory} files={report.file_count} manifest_sha256={report.manifest_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
