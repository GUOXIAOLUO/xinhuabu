"""Persistence interfaces and compatibility implementations for Workbench."""

from .canvas_repository import CanvasRepository
from .legacy_json_canvas_repository import LegacyJsonCanvasRepository

__all__ = ["CanvasRepository", "LegacyJsonCanvasRepository"]
