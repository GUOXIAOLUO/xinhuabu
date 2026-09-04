"""The only persisted execution-state vocabulary used by Canvas domain records."""

from enum import StrEnum


class NodeState(StrEnum):
    DRAFT = "draft"
    READY = "ready"
    MISSING_INPUT = "missing_input"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_USER = "waiting_user"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    OUTDATED = "outdated"
    FROZEN = "frozen"


_TRANSITIONS: dict[NodeState, frozenset[NodeState]] = {
    NodeState.DRAFT: frozenset({NodeState.READY, NodeState.MISSING_INPUT, NodeState.FROZEN}),
    NodeState.READY: frozenset({NodeState.MISSING_INPUT, NodeState.QUEUED, NodeState.OUTDATED, NodeState.FROZEN}),
    NodeState.MISSING_INPUT: frozenset({NodeState.DRAFT, NodeState.READY, NodeState.FROZEN}),
    NodeState.QUEUED: frozenset({NodeState.RUNNING, NodeState.FAILED, NodeState.OUTDATED, NodeState.FROZEN}),
    NodeState.RUNNING: frozenset({NodeState.WAITING_USER, NodeState.WAITING_APPROVAL, NodeState.COMPLETED, NodeState.FAILED, NodeState.OUTDATED}),
    NodeState.WAITING_USER: frozenset({NodeState.READY, NodeState.QUEUED, NodeState.FAILED, NodeState.FROZEN}),
    NodeState.WAITING_APPROVAL: frozenset({NodeState.READY, NodeState.QUEUED, NodeState.COMPLETED, NodeState.FAILED, NodeState.FROZEN}),
    NodeState.COMPLETED: frozenset({NodeState.OUTDATED, NodeState.FROZEN}),
    NodeState.FAILED: frozenset({NodeState.READY, NodeState.QUEUED, NodeState.FROZEN}),
    NodeState.OUTDATED: frozenset({NodeState.READY, NodeState.QUEUED, NodeState.FROZEN}),
    NodeState.FROZEN: frozenset(),
}


def can_transition(current: NodeState, target: NodeState) -> bool:
    """Return whether a state transition is permitted without an explicit unfreeze action."""
    return current == target or target in _TRANSITIONS[current]
