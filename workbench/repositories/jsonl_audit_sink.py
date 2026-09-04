"""Append-only, secret-free local audit sink for transitional Canvas-node actions."""

import json
from pathlib import Path
from typing import Any

from workbench.application.node_creation import NodeCreatedAuditEvent
from workbench.application.node_mutation import NodeDeletedAuditEvent, NodeUpdatedAuditEvent
from workbench.application.graph_mutation import NodeAndEdgeCreatedAuditEvent


class JsonlAuditSink:
    def __init__(self, path: str | Path, *, lock: Any):
        self._path = Path(path)
        self._lock = lock

    def append(self, event: NodeCreatedAuditEvent | NodeUpdatedAuditEvent | NodeDeletedAuditEvent | NodeAndEdgeCreatedAuditEvent) -> None:
        payload = {
            "event": "canvas.node.created",
            "actor_id": event.actor_id,
            "project_id": event.project_id,
            "canvas_id": event.canvas_id,
            "node_id": event.node_id,
            "occurred_at": event.occurred_at.isoformat(),
        }
        if isinstance(event, NodeCreatedAuditEvent):
            payload.update({
                "request_id": event.request_id,
                "definition_ref": event.definition_ref.model_dump(mode="json"),
                "source": event.source.value,
            })
        elif isinstance(event, NodeUpdatedAuditEvent):
            payload["event"] = "canvas.node.updated"
        elif isinstance(event, NodeAndEdgeCreatedAuditEvent):
            payload["event"] = "canvas.graph.node_and_edge_created"
            payload["edge_id"] = event.edge_id
        else:
            payload["event"] = "canvas.node.deleted"
        with self._lock:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
