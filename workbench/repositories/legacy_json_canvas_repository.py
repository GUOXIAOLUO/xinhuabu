"""Compatibility repository for the existing one-file-per-Canvas JSON store."""

import json
import os
import re
from pathlib import Path
from typing import Any, Callable

from .canvas_repository import (
    CanvasDeletedError,
    CanvasNotFoundError,
    CanvasRepository,
    CanvasValidationError,
    StaleCanvasRevisionError,
)


class LegacyJsonCanvasRepository(CanvasRepository):
    """Preserves current JSON shape and monotonic ``updated_at`` save semantics."""

    def __init__(self, directory: str | Path, *, clock_ms: Callable[[], int], lock: Any):
        self._directory = Path(directory)
        self._clock_ms = clock_ms
        self._lock = lock

    def path_for(self, canvas_id: str) -> Path:
        cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", str(canvas_id or ""))
        if not cleaned:
            raise CanvasValidationError("invalid canvas id")
        return self._directory / f"{cleaned}.json"

    def load(self, canvas_id: str, *, include_deleted: bool = False) -> dict[str, Any]:
        path = self.path_for(canvas_id)
        if not path.exists():
            raise CanvasNotFoundError("canvas not found")
        with path.open("r", encoding="utf-8") as handle:
            canvas = json.load(handle)
        if canvas.get("deleted_at") and not include_deleted:
            raise CanvasDeletedError("canvas is deleted")
        return canvas

    def save(self, canvas: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            return self._save_unlocked(canvas)

    def save_if_current(self, canvas: dict[str, Any], *, expected_updated_at: int | None) -> dict[str, Any]:
        canvas_id = str(canvas.get("id") or "")
        with self._lock:
            current = self.load(canvas_id, include_deleted=True)
            current_updated_at = int(current.get("updated_at") or 0)
            if expected_updated_at and current_updated_at and int(expected_updated_at) < current_updated_at:
                raise StaleCanvasRevisionError(current)
            return self._save_unlocked(canvas)

    def purge(self, canvas_id: str) -> bool:
        path = self.path_for(canvas_id)
        with self._lock:
            if not path.exists():
                return False
            os.remove(path)
            return True

    def mutate_if_current(
        self,
        canvas_id: str,
        *,
        expected_updated_at: int | None,
        already_applied: Callable[[dict[str, Any]], bool] | None = None,
        mutation: Callable[[dict[str, Any]], None],
    ) -> dict[str, Any]:
        """Apply one caller-owned mutation while holding the Legacy Canvas lock."""
        with self._lock:
            canvas = self.load(canvas_id, include_deleted=False)
            if already_applied is not None and already_applied(canvas):
                return canvas
            current_updated_at = int(canvas.get("updated_at") or 0)
            if expected_updated_at and current_updated_at and int(expected_updated_at) < current_updated_at:
                raise StaleCanvasRevisionError(canvas)
            mutation(canvas)
            return self._save_unlocked(canvas)

    def _save_unlocked(self, canvas: dict[str, Any]) -> dict[str, Any]:
        canvas_id = str(canvas.get("id") or "")
        path = self.path_for(canvas_id)
        previous_updated_at = int(canvas.get("updated_at") or 0)
        current_updated_at = int(self._clock_ms())
        canvas["updated_at"] = max(current_updated_at, previous_updated_at + 1) if previous_updated_at else current_updated_at
        self._directory.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(canvas, handle, ensure_ascii=False, indent=2)
        return canvas
