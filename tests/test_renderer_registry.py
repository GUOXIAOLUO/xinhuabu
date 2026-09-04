import json
import unittest
from datetime import UTC, datetime
from pathlib import Path

from workbench.application.renderer_registry import RendererRegistry, RendererRegistryError
from workbench.domain.canvas.models import DefinitionRef, NodeRecord, Position, RendererRef, Size
from workbench.domain.canvas.ports import PortSet
from workbench.domain.canvas.renderers import RENDERER_MANIFEST_SCHEMA_VERSION, RendererManifest
from workbench.domain.canvas.states import NodeState


SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "renderer" / "renderer-manifest.v1.schema.json"


def manifest(**overrides):
    values = {
        "renderer": RendererRef(id="legacy", version="1"),
        "display_name": "Legacy Renderer",
        "supported_kinds": ("asset", "group", "legacy"),
        "view_model_version": "1",
    }
    values.update(overrides)
    return RendererManifest(**values)


def node(**overrides):
    values = {
        "id": "node-1", "project_id": "project-1", "canvas_id": "canvas-1", "kind": "legacy",
        "definition_ref": DefinitionRef(type="legacy", id="prompt", version="0"),
        "renderer": RendererRef(id="legacy", version="1"), "state": NodeState.READY,
        "title": "Prompt", "position": Position(x=0, y=0), "size": Size(width=280, height=180),
        "ports": PortSet(), "created_by": "user-1",
        "created_at": datetime(2026, 9, 2, tzinfo=UTC), "updated_at": datetime(2026, 9, 2, tzinfo=UTC),
    }
    values.update(overrides)
    return NodeRecord(**values)


class RendererRegistryTests(unittest.TestCase):
    def test_resolves_versioned_renderer_without_skill_branches(self):
        registry = RendererRegistry([manifest()])
        self.assertEqual(registry.require(RendererRef(id="legacy", version="1")).display_name, "Legacy Renderer")
        self.assertTrue(registry.supports(node()))
        self.assertFalse(registry.supports(node(kind="task")))

    def test_rejects_duplicate_registration_and_unknown_renderer(self):
        registry = RendererRegistry([manifest()])
        with self.assertRaisesRegex(RendererRegistryError, "already registered"):
            registry.register(manifest())
        with self.assertRaisesRegex(RendererRegistryError, "not registered"):
            registry.require(RendererRef(id="form", version="1"))

    def test_manifest_schema_is_versioned_and_matches_domain_constant(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], RENDERER_MANIFEST_SCHEMA_VERSION)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(manifest().schema_version, RENDERER_MANIFEST_SCHEMA_VERSION)
