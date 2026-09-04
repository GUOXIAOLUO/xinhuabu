"""Industry-neutral, UI-free update and deletion service for migrated nodes."""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Callable, Protocol

from workbench.application.node_creation import ProjectAuthorizer
from workbench.domain.canvas.models import NodeRecord, Position


class NodeMutationError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


@dataclass(frozen=True)
class NodeUpdateCommand:
    actor_id: str
    project_id: str
    canvas_id: str
    node_id: str
    expected_revision: int
    title: str | None = None
    position: Position | None = None


@dataclass(frozen=True)
class NodeDeleteCommand:
    actor_id: str
    project_id: str
    canvas_id: str
    node_id: str
    expected_revision: int


@dataclass(frozen=True)
class NodeMutationPersistence:
    canvas_revision: int
    node: NodeRecord | None = None


@dataclass(frozen=True)
class NodeUpdatedAuditEvent:
    actor_id: str
    project_id: str
    canvas_id: str
    node_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class NodeDeletedAuditEvent:
    actor_id: str
    project_id: str
    canvas_id: str
    node_id: str
    occurred_at: datetime


class AtomicNodeMutationRepository(Protocol):
    def update_node(self, command: NodeUpdateCommand) -> NodeMutationPersistence: ...

    def delete_node(self, command: NodeDeleteCommand) -> NodeMutationPersistence: ...


class AuditSink(Protocol):
    def append(self, event: NodeUpdatedAuditEvent | NodeDeletedAuditEvent) -> None: ...


class NodeMutationService:
    """Authorize and audit changes without knowing routes, DOM, or Legacy JSON."""

    def __init__(
        self,
        *,
        authorizer: ProjectAuthorizer,
        repository: AtomicNodeMutationRepository,
        audit_sink: AuditSink,
        clock: Callable[[], datetime] | None = None,
    ):
        self._authorizer = authorizer
        self._repository = repository
        self._audit_sink = audit_sink
        self._clock = clock or (lambda: datetime.now(UTC))

    def update(self, command: NodeUpdateCommand) -> NodeMutationPersistence:
        self._validate_update(command)
        self._authorize(command.actor_id, command.project_id, command.canvas_id)
        persisted = self._repository.update_node(command)
        self._audit_sink.append(NodeUpdatedAuditEvent(
            actor_id=command.actor_id, project_id=command.project_id, canvas_id=command.canvas_id,
            node_id=command.node_id, occurred_at=self._clock(),
        ))
        return persisted

    def delete(self, command: NodeDeleteCommand) -> NodeMutationPersistence:
        self._validate_delete(command)
        self._authorize(command.actor_id, command.project_id, command.canvas_id)
        persisted = self._repository.delete_node(command)
        self._audit_sink.append(NodeDeletedAuditEvent(
            actor_id=command.actor_id, project_id=command.project_id, canvas_id=command.canvas_id,
            node_id=command.node_id, occurred_at=self._clock(),
        ))
        return persisted

    def _authorize(self, actor_id: str, project_id: str, canvas_id: str) -> None:
        if not self._authorizer.can_edit(actor_id, project_id, canvas_id):
            raise NodeMutationError("forbidden", "actor is not permitted to edit this Canvas")

    @staticmethod
    def _validate_identity(command: NodeUpdateCommand | NodeDeleteCommand) -> None:
        for name in ("actor_id", "project_id", "canvas_id", "node_id"):
            if not str(getattr(command, name) or "").strip():
                raise NodeMutationError("invalid_request", f"{name} is required")
        if command.expected_revision < 1:
            raise NodeMutationError("invalid_request", "expected_revision must be positive")

    @classmethod
    def _validate_update(cls, command: NodeUpdateCommand) -> None:
        cls._validate_identity(command)
        if command.title is None and command.position is None:
            raise NodeMutationError("invalid_request", "at least one mutable field is required")

    @classmethod
    def _validate_delete(cls, command: NodeDeleteCommand) -> None:
        cls._validate_identity(command)
