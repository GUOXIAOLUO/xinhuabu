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
    def purge(self, canvas_id: str) -> bool:
        raise NotImplementedError
