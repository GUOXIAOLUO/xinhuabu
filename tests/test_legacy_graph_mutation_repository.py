import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

from workbench.application.graph_mutation import CreateNodeAndEdgeCommand
from workbench.application.legacy_definitions import LegacyDefinitionRegistry
from workbench.domain.canvas.models import EdgeRecord, NodeRecord, Position, RendererRef, Size
from workbench.domain.canvas.ports import PortSet
from workbench.domain.canvas.states import NodeState
from workbench.repositories.legacy_json_canvas_repository import LegacyJsonCanvasRepository
from workbench.repositories.legacy_json_node_repository import LegacyJsonGraphMutationRepository


class LegacyJsonGraphMutationRepositoryTests(unittest.TestCase):
    def test_creates_group_and_edge_under_one_canvas_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = LegacyJsonCanvasRepository(Path(directory), clock_ms=lambda: 100, lock=Lock())
            repository.save({"id": "canvas", "project": "project", "nodes": [{"id": "origin", "type": "image"}], "connections": [], "updated_at": 99})
            revision = repository.load("canvas")["updated_at"]
            timestamp = datetime(2026, 9, 2, tzinfo=UTC)
            group = NodeRecord(id="group", project_id="project", canvas_id="canvas", kind="group", definition_ref=LegacyDefinitionRegistry.GROUP, renderer=RendererRef(id="legacy", version="1"), state=NodeState.READY, title="Group", position=Position(x=10, y=20), size=Size(width=300, height=220), ports=PortSet(), created_by="actor", created_at=timestamp, updated_at=timestamp)
            edge = EdgeRecord(id="edge", canvas_id="canvas", **{"from": {"node_id": "origin", "port_id": "legacy.out"}, "to": {"node_id": "group", "port_id": "legacy.in"}})
            result = LegacyJsonGraphMutationRepository(repository).create_node_and_edge(CreateNodeAndEdgeCommand(actor_id="actor", project_id="project", canvas_id="canvas", expected_revision=revision, node=group, edge=edge))
            saved = repository.load("canvas")
            self.assertGreater(result.canvas_revision, revision)
            self.assertEqual(saved["nodes"][-1]["items"], [])
            self.assertEqual(saved["connections"][-1], {"id": "edge", "from": "origin", "to": "group", "kind": "input"})

    def test_creates_smart_group_and_edge_under_one_canvas_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = LegacyJsonCanvasRepository(Path(directory), clock_ms=lambda: 100, lock=Lock())
            repository.save({"id": "canvas", "project": "project", "nodes": [{"id": "origin", "type": "smart-image"}], "connections": [], "updated_at": 99})
            revision = repository.load("canvas")["updated_at"]
            timestamp = datetime(2026, 9, 3, tzinfo=UTC)
            group = NodeRecord(id="group", project_id="project", canvas_id="canvas", kind="group", definition_ref=LegacyDefinitionRegistry.SMART_GROUP, renderer=RendererRef(id="legacy", version="1"), state=NodeState.READY, title="智能分组", position=Position(x=10, y=20), size=Size(width=340, height=286), ports=PortSet(), created_by="actor", created_at=timestamp, updated_at=timestamp)
            edge = EdgeRecord(id="edge", canvas_id="canvas", **{"from": {"node_id": "origin", "port_id": "legacy.out"}, "to": {"node_id": "group", "port_id": "legacy.in"}})
            LegacyJsonGraphMutationRepository(repository).create_node_and_edge(CreateNodeAndEdgeCommand(actor_id="actor", project_id="project", canvas_id="canvas", expected_revision=revision, node=group, edge=edge))
            saved = repository.load("canvas")
            self.assertEqual(saved["nodes"][-1]["type"], "smart-group")
            self.assertEqual(saved["nodes"][-1]["title"], "智能分组")
            self.assertEqual(saved["connections"][-1]["kind"], "input")

    def test_creates_smart_prompt_with_its_safe_config_and_edge(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = LegacyJsonCanvasRepository(Path(directory), clock_ms=lambda: 100, lock=Lock())
            repository.save({"id": "canvas", "project": "project", "nodes": [{"id": "origin", "type": "smart-image"}], "connections": [], "updated_at": 99})
            revision = repository.load("canvas")["updated_at"]
            timestamp = datetime(2026, 9, 3, tzinfo=UTC)
            prompt = NodeRecord(id="prompt", project_id="project", canvas_id="canvas", kind="legacy", definition_ref=LegacyDefinitionRegistry.SMART_PROMPT, renderer=RendererRef(id="legacy", version="1"), state=NodeState.READY, title="Prompt", position=Position(x=10, y=20), size=Size(width=316, height=240), ports=PortSet(), config={"text": "hello", "llmEnabled": True}, created_by="actor", created_at=timestamp, updated_at=timestamp)
            edge = EdgeRecord(id="edge", canvas_id="canvas", **{"from": {"node_id": "origin", "port_id": "legacy.out"}, "to": {"node_id": "prompt", "port_id": "legacy.in"}})
            LegacyJsonGraphMutationRepository(repository).create_node_and_edge(CreateNodeAndEdgeCommand(actor_id="actor", project_id="project", canvas_id="canvas", expected_revision=revision, node=prompt, edge=edge))
            saved = repository.load("canvas")
            self.assertEqual(saved["nodes"][-1]["type"], "smart-prompt")
            self.assertEqual(saved["nodes"][-1]["text"], "hello")
            self.assertTrue(saved["nodes"][-1]["llmEnabled"])

    def test_creates_smart_loop_with_its_safe_input_config_and_edge(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = LegacyJsonCanvasRepository(Path(directory), clock_ms=lambda: 100, lock=Lock())
            repository.save({"id": "canvas", "project": "project", "nodes": [{"id": "origin", "type": "smart-image"}], "connections": [], "updated_at": 99})
            revision = repository.load("canvas")["updated_at"]
            timestamp = datetime(2026, 9, 3, tzinfo=UTC)
            loop = NodeRecord(id="loop", project_id="project", canvas_id="canvas", kind="legacy", definition_ref=LegacyDefinitionRegistry.SMART_LOOP, renderer=RendererRef(id="legacy", version="1"), state=NodeState.READY, title="Loop", position=Position(x=10, y=20), size=Size(width=340, height=168), ports=PortSet(), config={"imageInput": True, "showPrompt": False}, created_by="actor", created_at=timestamp, updated_at=timestamp)
            edge = EdgeRecord(id="edge", canvas_id="canvas", **{"from": {"node_id": "origin", "port_id": "legacy.out"}, "to": {"node_id": "loop", "port_id": "legacy.in"}})
            LegacyJsonGraphMutationRepository(repository).create_node_and_edge(CreateNodeAndEdgeCommand(actor_id="actor", project_id="project", canvas_id="canvas", expected_revision=revision, node=loop, edge=edge))
            saved = repository.load("canvas")
            self.assertTrue(saved["nodes"][-1]["imageInput"])
            self.assertFalse(saved["nodes"][-1]["showPrompt"])
