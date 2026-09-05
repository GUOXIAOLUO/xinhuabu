"""R4 source-record backup and validation for Legacy Canvas JSON files."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


BACKUP_SCHEMA_VERSION = "workbench.canvas-source-backup/1"


class CanvasBackupError(RuntimeError):
    pass


@dataclass(frozen=True)
class CanvasBackupReport:
    backup_directory: Path
    file_count: int
    manifest_sha256: str


def create_canvas_source_backup(source_directory: Path, backup_directory: Path) -> CanvasBackupReport:
    source = source_directory.resolve()
    destination = backup_directory.resolve()
    if not source.is_dir():
        raise CanvasBackupError(f"source directory does not exist: {source}")
    if destination.exists():
        raise CanvasBackupError(f"backup destination already exists: {destination}")
    destination.mkdir(parents=True)
    files = _source_files(source)
    manifest_files = []
    for path in files:
        target = destination / path.name
        shutil.copy2(path, target)
        manifest_files.append({"name": path.name, "sha256": _sha256(target), "bytes": target.stat().st_size})
    manifest = {"schema_version": BACKUP_SCHEMA_VERSION, "source_directory": str(source), "files": manifest_files}
    manifest_path = destination / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validate_canvas_source_backup(destination)
    return CanvasBackupReport(destination, len(files), _sha256(manifest_path))


def validate_canvas_source_backup(backup_directory: Path) -> CanvasBackupReport:
    destination = backup_directory.resolve()
    manifest_path = destination / "manifest.json"
    if not manifest_path.is_file():
        raise CanvasBackupError("backup manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != BACKUP_SCHEMA_VERSION or not isinstance(manifest.get("files"), list):
        raise CanvasBackupError("backup manifest is invalid")
    expected = {item.get("name"): item for item in manifest["files"] if isinstance(item, dict)}
    if len(expected) != len(manifest["files"]):
        raise CanvasBackupError("backup manifest has duplicate or invalid names")
    actual = {path.name for path in destination.glob("*.json") if path.name != "manifest.json"}
    if actual != set(expected):
        raise CanvasBackupError("backup file set differs from manifest")
    for name, item in expected.items():
        path = destination / name
        if not path.is_file() or path.is_symlink() or _sha256(path) != item.get("sha256") or path.stat().st_size != item.get("bytes"):
            raise CanvasBackupError(f"backup validation failed: {name}")
    return CanvasBackupReport(destination, len(expected), _sha256(manifest_path))


def _source_files(source: Path) -> list[Path]:
    files = []
    for path in sorted(source.glob("*.json")):
        if path.is_symlink() or not path.is_file() or path.resolve().parent != source:
            raise CanvasBackupError(f"unsafe source file: {path}")
        files.append(path)
    return files


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
