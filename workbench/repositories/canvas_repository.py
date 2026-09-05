"""Industry-neutral persistence contract for Legacy and future Canvas stores."""

from abc import ABC, abstractmethod
from typing import Any


class CanvasRepositoryError(RuntimeError):
    """Base error for repository failures that routes can map to transport errors."""


class CanvasNotFoundError(CanvasRepositoryError):
    pass


class CanvasDeletedError(CanvasRepositoryError):
    pass


class CanvasValidationError(CanvasRepositoryError):
    pass


class StaleCanvasRevisionError(CanvasRepositoryError):
    def __init__(self, current: dict[str, Any]):
        self.current = current
        super().__init__("canvas revision is stale")


class CanvasRepository(ABC):
    """Raw Canvas persistence contract during the Legacy JSON transition."""

    @abstractmethod
    def load(self, canvas_id: str, *, include_deleted: bool = False) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save(self, canvas: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save_if_current(self, canvas: dict[str, Any], *, expected_updated_at: int | None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save_metadata(self, canvas: dict[str, Any]) -> dict[str, Any]:
        """Persist metadata without changing Legacy ``updated_at`` compatibility value."""
        raise NotImplementedError

    @abstractmethod
    def list_payloads(self, *, include_deleted: bool = False) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def list_payloads_with_diagnostics(self, *, include_deleted: bool = False) -> tuple[list[dict[str, Any]], bool]:
        """Return payloads plus whether unreadable source state makes destructive work unsafe."""
        raise NotImplementedError

    @abstractmethod
    def purge_expired_deleted(self, *, before_ms: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def reassign_project(self, *, source_project_id: str, target_project_id: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def purge(self, canvas_id: str) -> bool:
        raise NotImplementedError
