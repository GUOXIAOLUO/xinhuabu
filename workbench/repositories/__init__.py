"""Persistence interfaces and compatibility implementations for Workbench."""

from .canvas_repository import CanvasRepository
from .legacy_json_canvas_repository import LegacyJsonCanvasRepository
from .sqlite_project_canvas_repository import SqliteProjectCanvasRepository
from .sqlite_canvas_compatibility_repository import SqliteCanvasCompatibilityRepository

__all__ = ["CanvasRepository", "LegacyJsonCanvasRepository", "SqliteProjectCanvasRepository", "SqliteCanvasCompatibilityRepository"]
