"""Node creation/query adapters over the existing Legacy JSON Canvas store."""

from typing import Any

from workbench.application.node_creation import NodeCreationPersistence
from workbench.application.graph_mutation import CreateNodeAndEdgeCommand, GraphMutationPersistence
from workbench.application.node_mutation import NodeDeleteCommand, NodeMutationPersistence, NodeUpdateCommand
from workbench.domain.canvas.legacy_adapter import LegacyCanvasAdapter
from workbench.domain.canvas.models import NodeRecord

from .canvas_repository import StaleCanvasRevisionError
from .legacy_json_canvas_repository import LegacyJsonCanvasRepository


class LegacyCanvasProjectAuthorizer:
    """Scope a local actor to one Canvas project and, when present, its owner."""

    def __init__(self, repository: LegacyJsonCanvasRepository, *, allow_unowned_local: bool = False):
        self._repository = repository
        self._allow_unowned_local = allow_unowned_local

    def can_edit(self, actor_id: str, project_id: str, canvas_id: str) -> bool:
        try:
            canvas = self._repository.load(canvas_id)
        except Exception:
            return False
        if str(canvas.get("project") or "") != project_id:
            return False
        owner = str(canvas.get("owner") or "").strip()
        return owner == actor_id or (not owner and self._allow_unowned_local)


class LegacyJsonNodeCreationRepository:
    """Persist approved Legacy node shapes with durable idempotency."""

    REQUEST_METADATA_KEY = "_workbench_node_create_request_id"

    def __init__(self, repository: LegacyJsonCanvasRepository):
        self._repository = repository

    def create_node(self, node: NodeRecord, *, expected_revision: int | None, request_id: str) -> NodeCreationPersistence:
        if node.definition_ref.type != "legacy" or node.definition_ref.id not in {"image", "prompt", "loop", "group", "output", "smart-prompt", "smart-loop", "smart-group", "smart-minimax"} or node.definition_ref.version != "0":
            raise ValueError("this Legacy node repository only supports approved Legacy definitions")

        result: NodeCreationPersistence | None = None

        def find_existing(canvas: dict[str, Any]) -> bool:
            nonlocal result
            for existing in canvas.get("nodes") or []:
                if isinstance(existing, dict) and existing.get(self.REQUEST_METADATA_KEY) == request_id:
                    record = LegacyCanvasAdapter.node_to_record(existing, canvas=canvas)
                    result = NodeCreationPersistence(node=record, canvas_revision=int(canvas.get("updated_at") or 1), created=False)
                    return True
            return False

        def append(canvas: dict[str, Any]) -> None:
            definition_id = node.definition_ref.id
            is_smart_image = definition_id == "image" and canvas.get("kind") == "smart"
            payload: dict[str, Any] = {
                "id": node.id,
                "type": "smart-image" if is_smart_image else definition_id,
                "x": node.position.x,
                "y": node.position.y,
                "w": node.size.width,
                "h": node.size.height,
                self.REQUEST_METADATA_KEY: request_id,
            }
            if definition_id == "image":
                if is_smart_image:
                    payload.update({"title": node.title, "images": []})
                else:
                    payload["name"] = node.title
            elif definition_id == "output":
                payload["images"] = []
            elif node.definition_ref.id == "prompt":
                payload["text"] = str(node.config.get("text") or "")
            elif node.definition_ref.id == "smart-prompt":
                for key, default in {
                    "title": "Prompt", "text": "", "promptResult": "", "promptResultOutdated": False, "promptSeparator": ";", "promptSplitEnabled": False,
                    "llmEnabled": False, "llmProvider": "", "llmModel": "", "llmSystemEnabled": False,
                    "llmSystemPrompt": "You are a helpful prompt assistant.", "llmInstruction": "",
                    "promptSkillEnabled": True, "promptSkillPack": "MiniMax H3 Skills",
                    "promptSkillDefinition": "3D动画短片生成器", "promptOutputMode": "text", "promptAttachments": [],
                }.items():
                    payload[key] = node.title if key == "title" else node.config.get(key, default)
            elif node.definition_ref.id == "smart-loop":
                payload.update({"title": node.title, "count": 1, "mode": "serial", "showPrompt": False, "imageInput": False, "loopStart": 1, "imageBatchSize": 1, "variablePrompt": ""})
            elif node.definition_ref.id == "smart-minimax":
                payload.update(_smart_minimax_payload(node))
            elif node.definition_ref.id in {"group", "smart-group"}:
                payload.update({"title": node.title, "items": []})
            else:
                payload.update({
                    "count": int(node.config.get("count") or 3), "mode": "serial",
                    "showPrompt": False, "imageInput": False, "videoInput": False,
                    "loopStart": 1, "imageBatchSize": 1, "videoBatchSize": 1,
                    "variablePrompt": "", "fixedPrompt": "",
                })
            canvas.setdefault("nodes", []).append(payload)

        saved = self._repository.mutate_if_current(
            node.canvas_id,
            expected_updated_at=expected_revision,
            already_applied=find_existing,
            mutation=append,
        )
        if result is not None:
            return result
        return NodeCreationPersistence(
            node=node,
            canvas_revision=int(saved.get("updated_at") or 1),
            created=True,
        )


class LegacyJsonNodeLookup:
    def __init__(self, repository: LegacyJsonCanvasRepository, authorizer: LegacyCanvasProjectAuthorizer):
        self._repository = repository
        self._authorizer = authorizer

    def get(self, *, actor_id: str, project_id: str, canvas_id: str, node_id: str) -> NodeRecord:
        if not self._authorizer.can_edit(actor_id, project_id, canvas_id):
            raise LookupError
        canvas = self._repository.load(canvas_id)
        node = next((item for item in canvas.get("nodes") or [] if isinstance(item, dict) and item.get("id") == node_id), None)
        if node is None:
            raise LookupError
        return LegacyCanvasAdapter.node_to_record(node, canvas=canvas)


class LegacyJsonNodeMutationRepository:
    """Update or delete transitional Image and safe Classic/Smart simple node shapes."""

    def __init__(self, repository: LegacyJsonCanvasRepository):
        self._repository = repository

    def update_node(self, command: NodeUpdateCommand) -> NodeMutationPersistence:
        updated: dict[str, Any] | None = None

        def mutation(canvas: dict[str, Any]) -> None:
            nonlocal updated
            updated = self._find_mutable_node(canvas, command.node_id)
            if command.title is not None:
                if updated.get("type") == "smart-image":
                    updated["title"] = command.title
                else:
                    updated["name"] = command.title
            if command.position is not None:
                updated["x"] = command.position.x
                updated["y"] = command.position.y

        saved = self._repository.mutate_if_current(
            command.canvas_id, expected_updated_at=command.expected_revision, mutation=mutation,
        )
        if updated is None:  # Defensive: mutation either finds a node or raises.
            raise LookupError("node not found")
        return NodeMutationPersistence(
            node=LegacyCanvasAdapter.node_to_record(updated, canvas=saved),
            canvas_revision=int(saved.get("updated_at") or 1),
        )

    def delete_node(self, command: NodeDeleteCommand) -> NodeMutationPersistence:
        def mutation(canvas: dict[str, Any]) -> None:
            self._find_mutable_node(canvas, command.node_id)
            canvas["nodes"] = [
                node for node in canvas.get("nodes") or []
                if not isinstance(node, dict) or node.get("id") != command.node_id
            ]
            canvas["connections"] = [
                edge for edge in canvas.get("connections") or []
                if not isinstance(edge, dict)
                or (edge.get("from") != command.node_id and edge.get("to") != command.node_id)
            ]

        saved = self._repository.mutate_if_current(
            command.canvas_id, expected_updated_at=command.expected_revision, mutation=mutation,
        )
        return NodeMutationPersistence(canvas_revision=int(saved.get("updated_at") or 1))

    @staticmethod
    def _find_mutable_node(canvas: dict[str, Any], node_id: str) -> dict[str, Any]:
        node = next((item for item in canvas.get("nodes") or [] if isinstance(item, dict) and item.get("id") == node_id), None)
        if node is None or node.get("type") not in {"image", "smart-image", "prompt", "loop", "output", "group", "smart-group", "smart-loop", "smart-prompt"}:
            raise LookupError("node not found")
        return node


class LegacyJsonGraphMutationRepository:
    """One-lock Legacy JSON implementation of the create-node-and-edge transaction."""

    def __init__(self, repository: LegacyJsonCanvasRepository):
        self._repository = repository

    def create_node_and_edge(self, command: CreateNodeAndEdgeCommand) -> GraphMutationPersistence:
        definition_id = command.node.definition_ref.id
        if command.node.definition_ref.type != "legacy" or definition_id not in {"image", "prompt", "loop", "group", "smart-group", "smart-prompt", "smart-loop", "smart-minimax"}:
            raise ValueError("this Legacy graph repository only supports approved image, prompt, loop, group, and MiniMax definitions")

        def mutation(canvas: dict[str, Any]) -> None:
            node_ids = {item.get("id") for item in canvas.get("nodes") or [] if isinstance(item, dict)}
            if command.node.id in node_ids:
                raise ValueError("node id already exists")
            if command.edge.from_.node_id not in node_ids and command.edge.to.node_id not in node_ids:
                raise ValueError("edge must connect the new node to an existing Legacy node")
            legacy_type = "smart-image" if definition_id == "image" and canvas.get("kind") == "smart" else definition_id
            payload: dict[str, Any] = {
                "id": command.node.id, "type": legacy_type, "title": command.node.title,
                "x": command.node.position.x, "y": command.node.position.y,
                "w": command.node.size.width, "h": command.node.size.height,
            }
            if definition_id == "image":
                payload["images"] = []
                if legacy_type == "smart-image":
                    payload.pop("name", None)
                else:
                    payload["name"] = command.node.title
            elif definition_id == "prompt":
                payload["text"] = str(command.node.config.get("text") or "")
            elif definition_id == "loop":
                payload.update({
                    "count": int(command.node.config.get("count") or 3), "mode": "serial",
                    "showPrompt": False, "imageInput": False, "videoInput": False,
                    "loopStart": 1, "imageBatchSize": 1, "videoBatchSize": 1,
                    "variablePrompt": "", "fixedPrompt": "",
                })
            elif definition_id == "smart-prompt":
                for key, default in {
                    "text": "", "promptResult": "", "promptResultOutdated": False, "promptSeparator": ";", "promptSplitEnabled": False,
                    "llmEnabled": False, "llmProvider": "", "llmModel": "", "llmSystemEnabled": False,
                    "llmSystemPrompt": "You are a helpful prompt assistant.", "llmInstruction": "",
                    "promptSkillEnabled": True, "promptSkillPack": "MiniMax H3 Skills",
                    "promptSkillDefinition": "3D动画短片生成器", "promptOutputMode": "text", "promptAttachments": [],
                }.items():
                    payload[key] = command.node.config.get(key, default)
            elif definition_id == "smart-loop":
                payload.update({"count": 1, "mode": "serial",
                                "showPrompt": bool(command.node.config.get("showPrompt", False)),
                                "imageInput": bool(command.node.config.get("imageInput", False)),
                                "loopStart": 1, "imageBatchSize": 1, "variablePrompt": ""})
            elif definition_id == "smart-minimax":
                payload.update(_smart_minimax_payload(command.node))
            else:
                payload["items"] = []
            canvas.setdefault("nodes", []).append(payload)
            canvas.setdefault("connections", []).append({
                "id": command.edge.id, "from": command.edge.from_.node_id, "to": command.edge.to.node_id, "kind": "input",
            })
            target = next((item for item in canvas["nodes"] if isinstance(item, dict) and item.get("id") == command.edge.to.node_id), None)
            if target is None:  # Defensive: GraphMutationService already validates this relationship.
                raise LookupError("edge target not found")
            target["inputNodeIds"] = list(dict.fromkeys([*(target.get("inputNodeIds") or []), command.edge.from_.node_id]))

        saved = self._repository.mutate_if_current(
            command.canvas_id, expected_updated_at=command.expected_revision, mutation=mutation,
        )
        return GraphMutationPersistence(canvas_revision=int(saved.get("updated_at") or 1), node=command.node, edge=command.edge)


def _smart_minimax_payload(node: NodeRecord) -> dict[str, Any]:
    """Safe blank-node defaults; provider credentials and runtime state never persist here."""
    duration = 8
    return {
        "workflow": "MiniMax_H3.json", "minimaxEngine": "comfyui", "minimaxRunningHubWorkflowId": "",
        "duration": duration, "aspectRatio": "16:9 (Widescreen)", "megapixels": 0.4,
        "promptDraftText": "", "refs": {"image": [], "video": [], "audio": []}, "materials": [],
        "segments": [{"id": f"{node.id}:segment-1", "start": 0, "duration": duration, "prompt": "",
                      "refs": {"image": [], "video": [], "audio": []}, "refItems": [], "trimIn": 0,
                      "trimOut": duration, "result": None, "results": []}],
        "selectedSegmentId": "", "playhead": 0, "timelineZoom": 1, "minimaxPreviewH": 190,
        "minimaxVideoTrackH": 70, "minimaxRefLaneH": 42, "minimaxMuted": False,
        "timelinePlaying": False, "running": False,
    }
