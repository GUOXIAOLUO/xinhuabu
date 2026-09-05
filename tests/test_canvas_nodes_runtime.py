import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from workbench.api.canvas_nodes import CreateNodeAndEdgePayload, NodeCreatePayload, NodeDeletePayload, NodeUpdatePayload


class CanvasNodesRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.canvas_dir = Path(self.temp.name) / "canvases"
        self.canvas_dir.mkdir(parents=True)
        self.audit_path = Path(self.temp.name) / "audit" / "events.jsonl"
        self.canvas_patch = patch.object(main, "CANVAS_DIR", str(self.canvas_dir))
        self.audit_patch = patch.object(main, "CANVAS_NODE_AUDIT_PATH", str(self.audit_path))
        self.canvas_patch.start()
        self.audit_patch.start()

    def tearDown(self):
        self.audit_patch.stop()
        self.canvas_patch.stop()
        self.temp.cleanup()

    def endpoint(self, path, method):
        pending = list(main.app.routes)
        while pending:
            route = pending.pop()
            if getattr(route, "path", None) == path and method in getattr(route, "methods", set()):
                return route.endpoint
            pending.extend(getattr(route, "routes", []))
            pending.extend(getattr(getattr(route, "original_router", None), "routes", []))
        self.fail(f"versioned Canvas-node {method} route is not registered")

    def test_transitional_node_api_is_enabled_only_for_loopback_hosts(self):
        self.assertTrue(main.node_api_is_enabled_for_host("127.0.0.1"))
        self.assertTrue(main.node_api_is_enabled_for_host("::1"))
        self.assertFalse(main.node_api_is_enabled_for_host("0.0.0.0"))
        self.assertFalse(main.node_api_is_enabled_for_host("192.168.1.5"))

    def test_registered_local_route_creates_and_persists_one_legacy_image(self):
        canvas = main.new_canvas("node API test", kind="classic", project="default")
        payload = NodeCreatePayload(
            request_id="runtime-request-1",
            project_id="default",
            source="legacy",
            definition_ref={"type": "legacy", "id": "image", "version": "0"},
            position={"x": 12, "y": 24},
            expected_revision=canvas["updated_at"],
        )
        create = self.endpoint("/api/v1/canvases/{canvas_id}/nodes", "POST")
        response = asyncio.run(create(canvas["id"], payload, x_user_id="local-user"))
        duplicate = asyncio.run(create(canvas["id"], payload, x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertTrue(response.created)
        self.assertFalse(duplicate.created)
        self.assertEqual(len(saved["nodes"]), 1)
        self.assertEqual(saved["nodes"][0]["type"], "image")
        self.assertTrue(self.audit_path.exists())

    def test_registered_local_route_creates_empty_smart_group(self):
        canvas = main.new_canvas("smart group API test", kind="classic", project="default")
        create = self.endpoint("/api/v1/canvases/{canvas_id}/nodes", "POST")
        response = asyncio.run(create(canvas["id"], NodeCreatePayload(
            request_id="runtime-smart-group-1", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "smart-group", "version": "0"},
            position={"x": 12, "y": 24}, expected_revision=canvas["updated_at"], title="智能分组",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertTrue(response.created)
        self.assertEqual((saved["nodes"][0]["type"], saved["nodes"][0]["w"], saved["nodes"][0]["h"], saved["nodes"][0]["items"]), (
            "smart-group", 340, 286, [],
        ))

    def test_registered_local_route_creates_empty_classic_group(self):
        canvas = main.new_canvas("classic group API test", kind="classic", project="default")
        create = self.endpoint("/api/v1/canvases/{canvas_id}/nodes", "POST")
        response = asyncio.run(create(canvas["id"], NodeCreatePayload(
            request_id="runtime-group-1", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "group", "version": "0"},
            position={"x": 12, "y": 24}, expected_revision=canvas["updated_at"], title="Group",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertTrue(response.created)
        self.assertEqual((saved["nodes"][0]["type"], saved["nodes"][0]["w"], saved["nodes"][0]["h"], saved["nodes"][0]["items"]), (
            "group", 300, 220, [],
        ))

    def test_registered_local_route_creates_empty_classic_output(self):
        canvas = main.new_canvas("classic output API test", kind="classic", project="default")
        create = self.endpoint("/api/v1/canvases/{canvas_id}/nodes", "POST")
        response = asyncio.run(create(canvas["id"], NodeCreatePayload(
            request_id="runtime-output-1", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "output", "version": "0"},
            position={"x": 12, "y": 24}, expected_revision=canvas["updated_at"], title="Output",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertTrue(response.created)
        self.assertEqual((saved["nodes"][0]["type"], saved["nodes"][0]["images"], saved["nodes"][0]["w"], saved["nodes"][0]["h"]), (
            "output", [], 460, 180,
        ))

    def test_registered_routes_update_and_delete_legacy_image(self):
        canvas = main.new_canvas("node mutation API test", kind="classic", project="default")
        create = self.endpoint("/api/v1/canvases/{canvas_id}/nodes", "POST")
        created = asyncio.run(create(canvas["id"], NodeCreatePayload(
            request_id="runtime-mutation-1", project_id="default", source="legacy",
            definition_ref={"type": "legacy", "id": "image", "version": "0"}, position={"x": 12, "y": 24},
            expected_revision=canvas["updated_at"],
        ), x_user_id="local-user"))
        update = self.endpoint("/api/v1/canvases/{canvas_id}/nodes/{node_id}", "PUT")
        updated = asyncio.run(update(canvas["id"], created.node["id"], NodeUpdatePayload(
            project_id="default", expected_revision=created.canvas_revision, title="Updated", position={"x": 55, "y": 66},
        ), x_user_id="local-user"))
        self.assertEqual(updated["node"]["title"], "Updated")
        delete = self.endpoint("/api/v1/canvases/{canvas_id}/nodes/{node_id}", "DELETE")
        deleted = asyncio.run(delete(canvas["id"], created.node["id"], NodeDeletePayload(
            project_id="default", expected_revision=updated["canvas_revision"],
        ), x_user_id="local-user"))
        self.assertTrue(deleted["deleted"])
        self.assertEqual(main.load_canvas(canvas["id"])["nodes"], [])

    def test_registered_graph_route_creates_group_and_edge_atomically(self):
        canvas = main.new_canvas("graph API test", kind="classic", project="default")
        main.canvas_repository().mutate_if_current(canvas["id"], expected_updated_at=canvas["updated_at"], mutation=lambda item: item["nodes"].append({"id": "origin", "type": "image"}))
        revision = main.load_canvas(canvas["id"])["updated_at"]
        endpoint = self.endpoint("/api/v1/canvases/{canvas_id}/graph/create-node-and-edge", "POST")
        result = asyncio.run(endpoint(canvas["id"], CreateNodeAndEdgePayload(
            request_id="graph-request", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "group", "version": "0"}, position={"x": 10, "y": 20},
            expected_revision=revision, existing_node_id="origin", edge_id="edge-1",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertEqual(result["edge"]["to"]["node_id"], result["node"]["id"])
        self.assertEqual(len(saved["nodes"]), 2)
        self.assertEqual(len(saved["connections"]), 1)

    def test_registered_graph_route_creates_smart_group_and_edge_atomically(self):
        canvas = main.new_canvas("smart graph API test", kind="smart", project="default")
        main.canvas_repository().mutate_if_current(canvas["id"], expected_updated_at=canvas["updated_at"], mutation=lambda item: item["nodes"].append({"id": "origin", "type": "smart-image"}))
        revision = main.load_canvas(canvas["id"])["updated_at"]
        endpoint = self.endpoint("/api/v1/canvases/{canvas_id}/graph/create-node-and-edge", "POST")
        result = asyncio.run(endpoint(canvas["id"], CreateNodeAndEdgePayload(
            request_id="smart-graph-request", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "smart-group", "version": "0"}, position={"x": 10, "y": 20},
            expected_revision=revision, existing_node_id="origin", edge_id="edge-smart-1",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertEqual(result["edge"]["to"]["node_id"], result["node"]["id"])
        self.assertEqual(saved["nodes"][-1]["type"], "smart-group")
        self.assertEqual(saved["connections"][-1]["kind"], "input")

    def test_registered_graph_route_creates_smart_prompt_and_edge_atomically(self):
        canvas = main.new_canvas("smart prompt graph API test", kind="smart", project="default")
        main.canvas_repository().mutate_if_current(canvas["id"], expected_updated_at=canvas["updated_at"], mutation=lambda item: item["nodes"].append({"id": "origin", "type": "smart-image"}))
        revision = main.load_canvas(canvas["id"])["updated_at"]
        endpoint = self.endpoint("/api/v1/canvases/{canvas_id}/graph/create-node-and-edge", "POST")
        asyncio.run(endpoint(canvas["id"], CreateNodeAndEdgePayload(
            request_id="smart-prompt-graph-request", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "smart-prompt", "version": "0"}, position={"x": 10, "y": 20},
            initial_config={"text": "hello", "llmEnabled": True}, expected_revision=revision,
            existing_node_id="origin", edge_id="edge-smart-prompt-1",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertEqual(saved["nodes"][-1]["type"], "smart-prompt")
        self.assertEqual(saved["nodes"][-1]["text"], "hello")
        self.assertTrue(saved["nodes"][-1]["llmEnabled"])

    def test_registered_graph_route_creates_smart_image_and_edge_atomically(self):
        canvas = main.new_canvas("smart image graph API test", kind="smart", project="default")
        main.canvas_repository().mutate_if_current(canvas["id"], expected_updated_at=canvas["updated_at"], mutation=lambda item: item["nodes"].append({"id": "origin", "type": "smart-prompt"}))
        revision = main.load_canvas(canvas["id"])["updated_at"]
        endpoint = self.endpoint("/api/v1/canvases/{canvas_id}/graph/create-node-and-edge", "POST")
        asyncio.run(endpoint(canvas["id"], CreateNodeAndEdgePayload(
            request_id="smart-image-graph-request", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "image", "version": "0"}, position={"x": 10, "y": 20},
            expected_revision=revision, existing_node_id="origin", edge_id="edge-smart-image-1",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertEqual(saved["nodes"][-1]["type"], "smart-image")
        self.assertEqual(saved["nodes"][-1]["images"], [])

    def test_registered_graph_route_creates_smart_minimax_and_edge_atomically(self):
        canvas = main.new_canvas("smart minimax graph API test", kind="smart", project="default")
        main.canvas_repository().mutate_if_current(canvas["id"], expected_updated_at=canvas["updated_at"], mutation=lambda item: item["nodes"].append({"id": "origin", "type": "smart-image"}))
        revision = main.load_canvas(canvas["id"])["updated_at"]
        endpoint = self.endpoint("/api/v1/canvases/{canvas_id}/graph/create-node-and-edge", "POST")
        asyncio.run(endpoint(canvas["id"], CreateNodeAndEdgePayload(
            request_id="smart-minimax-graph-request", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "smart-minimax", "version": "0"}, position={"x": 10, "y": 20},
            expected_revision=revision, existing_node_id="origin", edge_id="edge-smart-minimax-1",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertEqual(saved["nodes"][-1]["type"], "smart-minimax")
        self.assertFalse(saved["nodes"][-1]["running"])

    def test_registered_local_route_creates_empty_smart_minimax(self):
        canvas = main.new_canvas("smart minimax API test", kind="smart", project="default")
        create = self.endpoint("/api/v1/canvases/{canvas_id}/nodes", "POST")
        response = asyncio.run(create(canvas["id"], NodeCreatePayload(
            request_id="runtime-smart-minimax-1", project_id="default", source="context_menu",
            definition_ref={"type": "legacy", "id": "smart-minimax", "version": "0"},
            position={"x": 12, "y": 24}, expected_revision=canvas["updated_at"], title="MiniMax H3",
        ), x_user_id="local-user"))
        saved = main.load_canvas(canvas["id"])
        self.assertTrue(response.created)
        self.assertEqual(saved["nodes"][0]["type"], "smart-minimax")
        self.assertFalse(saved["nodes"][0]["running"])
