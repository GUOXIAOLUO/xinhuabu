import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRY_COMPATIBILITY = ROOT / "static" / "js" / "workbench" / "canvas" / "canvas-entry-compatibility.js"


class CanvasEntryTests(unittest.TestCase):
    def test_new_canvas_flow_has_one_normal_creation_choice(self):
        source = (ROOT / "static" / "js" / "canvas-list.js").read_text(encoding="utf-8")
        create_flow = source[source.index("function openCreateCard") : source.index("/* ===== Card context menu")]
        self.assertNotIn("ws-create-toggle", create_flow)
        self.assertNotIn("createKind", create_flow)
        self.assertIn("kind: 'classic'", create_flow)
        self.assertNotIn("kind: 'smart'", create_flow)

    def test_canvas_list_does_not_display_legacy_source_kind_labels(self):
        source = (ROOT / "static" / "js" / "canvas-list.js").read_text(encoding="utf-8")
        self.assertNotIn("智能画布", source)
        self.assertNotIn("普通画布", source)
        self.assertNotIn("ws-card-kind", source)

    def test_canvas_list_uses_one_normal_open_entry(self):
        source = (ROOT / "static" / "js" / "canvas-list.js").read_text(encoding="utf-8")
        opening = source[source.index("function openCanvas(c){") : source.index("/* ===== Card create flow")]
        self.assertIn("/static/canvas.html", opening)
        self.assertNotIn("/static/smart-canvas.html", opening)

    def test_entry_compatibility_keeps_one_normal_entry_and_scopes_smart_handoff(self):
        source = ENTRY_COMPATIBILITY.read_text(encoding="utf-8")
        self.assertNotIn("fetch(", source)
        self.assertNotIn("localStorage", source)
        result = subprocess.run(["node", "-e", f"""
const fs=require('fs'), vm=require('vm'); const sandbox={{window:{{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(ENTRY_COMPATIBILITY))}, 'utf8'), sandbox);
const E=sandbox.window.WorkbenchCanvasEntryCompatibility;
console.log(JSON.stringify({{
  normal:E.normalCanvasUrl('canvas / 1', 'project / 1'),
  smart:E.legacySmartCanvasUrl('canvas / 1'),
  historical:E.requiresLegacySmartHandoff({{kind:'smart'}}),
  normalRecord:E.requiresLegacySmartHandoff({{kind:'classic'}}),
  missingKind:E.requiresLegacySmartHandoff({{}}),
}}));
"""], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout), {
            "normal": "/static/canvas.html?id=canvas%20%2F%201&project=project%20%2F%201",
            "smart": "/static/smart-canvas.html?id=canvas%20%2F%201",
            "historical": True,
            "normalRecord": False,
            "missingKind": False,
        })
