import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "static" / "js" / "workbench" / "canvas" / "node-inspector.js"
MEDIA_MODULE = ROOT / "static" / "js" / "workbench" / "canvas" / "media-renderer.js"
MEDIA_KIND_MODULE = ROOT / "static" / "js" / "workbench" / "canvas" / "media-kind.js"
RECORDS_MODULE = ROOT / "static" / "js" / "workbench" / "canvas" / "records.js"


class NodeInspectorTests(unittest.TestCase):
    def test_generic_read_only_sections_are_derived_from_node_record(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const result = sandbox.window.WorkbenchNodeInspector.viewModel({{
  id: 'node-1', title: '测试节点', kind: 'legacy', state: 'running',
  definition_ref: {{id: 'prompt'}}, position: {{x: 12.8, y: -2.2}},
  size: {{width: 340, height: 286}},
}});
console.log(JSON.stringify(result));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        model = json.loads(result.stdout)
        self.assertEqual(model["nodeId"], "node-1")
        self.assertEqual(model["title"], "测试节点")
        self.assertEqual([section["id"] for section in model["sections"]], ["identity", "geometry", "status", "version", "input-output"])
        self.assertEqual(model["sections"][0]["fields"], [
            {"id": "type", "label": "类型", "value": "prompt"},
            {"id": "state", "label": "状态", "value": "running"},
        ])
        self.assertEqual(model["sections"][1]["fields"], [
            {"id": "position", "label": "位置", "value": "13, -2"},
            {"id": "size", "label": "尺寸", "value": "340 × 286"},
        ])
        self.assertEqual(model["sections"][2]["fields"], [
            {"id": "description", "label": "说明", "value": "正在执行"},
            {"id": "changed-at", "label": "状态时间", "value": "未记录"},
        ])
        self.assertEqual(model["sections"][3]["fields"], [
            {"id": "revision", "label": "版本", "value": "r1"},
            {"id": "origin", "label": "来源", "value": "未记录"},
        ])
        self.assertEqual(model["sections"][4]["fields"], [
            {"id": "input-references", "label": "输入引用", "value": "0 项"},
            {"id": "output-references", "label": "输出引用", "value": "0 项"},
            {"id": "input-connections", "label": "输入连接", "value": "0 条"},
            {"id": "output-connections", "label": "输出连接", "value": "0 条"},
        ])

    def test_renderer_can_register_a_namespaced_read_only_section(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const api = sandbox.window.WorkbenchNodeInspector;
api.registerSectionProvider({{id: 'legacy', version: '1'}}, node => ({{
  id: 'legacy-renderer', title: '兼容适配',
  fields: [{{id: 'payload', label: '内容', value: node.extensions.legacy.payload.type}}],
}}));
const legacy = api.viewModel({{renderer: {{id: 'legacy', version: '1'}}, extensions: {{legacy: {{payload: {{type: 'prompt'}}}}}}}});
const other = api.viewModel({{renderer: {{id: 'media', version: '1'}}}});
console.log(JSON.stringify({{legacy, other}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        model = json.loads(result.stdout)
        self.assertEqual([section["id"] for section in model["legacy"]["sections"]], ["identity", "geometry", "status", "version", "input-output", "legacy-renderer"])
        self.assertEqual(model["legacy"]["sections"][5]["fields"][0]["value"], "prompt")
        self.assertEqual([section["id"] for section in model["other"]["sections"]], ["identity", "geometry", "status", "version", "input-output"])

    def test_media_renderer_registers_a_safe_media_summary(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(MEDIA_KIND_MODULE))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(MEDIA_MODULE))}, 'utf8'), sandbox);
const model = sandbox.window.WorkbenchNodeInspector.viewModel({{
  renderer: {{id: 'legacy', version: '1'}},
  extensions: {{legacy: {{payload: {{images: [
    {{url: '/assets/one.png'}}, {{url: '/assets/two.mp4'}}, {{url: '/assets/three.mp3'}},
  ]}}}}}},
}});
console.log(JSON.stringify(model));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        model = json.loads(result.stdout)
        self.assertEqual([section["id"] for section in model["sections"]], ["identity", "geometry", "status", "version", "input-output", "media-renderer"])
        self.assertEqual(model["sections"][5]["fields"], [
            {"id": "media-count", "label": "数量", "value": "3 项"},
            {"id": "media-summary", "label": "类型", "value": "图片 1 · 视频 1 · 音频 1"},
        ])

    def test_input_output_summary_counts_active_incoming_and_outgoing_edges(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const model = sandbox.window.WorkbenchNodeInspector.viewModel({{id: 'current'}}, {{connections: [
  {{from: 'upstream', to: 'current'}},
  {{from: {{node_id: 'another'}}, to: {{node_id: 'current'}}}},
  {{from: 'current', to: 'downstream'}},
  {{from: 'current', to: 'disabled', state: 'disabled'}},
]}});
console.log(JSON.stringify(model));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        model = json.loads(result.stdout)
        self.assertEqual([section["id"] for section in model["sections"]], ["identity", "geometry", "status", "version", "input-output"])
        self.assertEqual(model["sections"][4]["fields"], [
            {"id": "input-references", "label": "输入引用", "value": "0 项"},
            {"id": "output-references", "label": "输出引用", "value": "0 项"},
            {"id": "input-connections", "label": "输入连接", "value": "2 条"},
            {"id": "output-connections", "label": "输出连接", "value": "1 条"},
        ])

    def test_multi_selection_summary_is_read_only_and_compact(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const model = sandbox.window.WorkbenchNodeInspector.selectionViewModel([
  {{id: 'node-b', kind: 'legacy', definition_ref: {{id: 'prompt'}}, state: 'running'}},
  {{id: 'node-a', kind: 'legacy', definition_ref: {{id: 'prompt'}}, state: 'ready'}},
  {{id: 'node-c', kind: 'legacy', definition_ref: {{id: 'image'}}, state: 'ready'}},
]);
console.log(JSON.stringify(model));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout), {
            "nodeId": "selection:node-a|node-b|node-c",
            "title": "已选中 3 个节点",
            "sections": [
                {"id": "identity", "title": "选择", "fields": [
                    {"id": "selected-count", "label": "节点", "value": "3 个"},
                    {"id": "type-count", "label": "类型", "value": "2 种"},
                ]},
                {"id": "status", "title": "状态", "fields": [
                    {"id": "state-summary", "label": "分布", "value": "running 1 · ready 2"},
                ]},
            ],
        })

    def test_legacy_adapter_marks_fallback_origin_without_faking_provenance(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(RECORDS_MODULE))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const record = sandbox.window.WorkbenchCanvas.legacyNodeView({{
  id: 'old', type: 'smart-prompt', revision: 4, inputNodeIds: ['upstream'],
  output_refs: [{{type: 'asset_version', id: 'asset-1'}}],
}}, {{projectId: 'p', canvasId: 'c'}});
const model = sandbox.window.WorkbenchNodeInspector.viewModel(record);
console.log(JSON.stringify({{version: model.sections[3].fields, references: model.sections[4].fields}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout), {
            "version": [
                {"id": "revision", "label": "版本", "value": "r4"},
                {"id": "origin", "label": "来源", "value": "兼容画布"},
            ],
            "references": [
                {"id": "input-references", "label": "输入引用", "value": "1 项"},
                {"id": "output-references", "label": "输出引用", "value": "1 项"},
                {"id": "input-connections", "label": "输入连接", "value": "0 条"},
                {"id": "output-connections", "label": "输出连接", "value": "0 条"},
            ],
        })

    def test_status_summary_uses_only_explicit_state_timestamp(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const model = sandbox.window.WorkbenchNodeInspector.viewModel({{
  state: 'completed', metadata: {{state_changed_at: 1700000000000}},
}});
console.log(JSON.stringify(model.sections[2].fields));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout), [
            {"id": "description", "label": "说明", "value": "已完成"},
            {"id": "changed-at", "label": "状态时间", "value": "2023-11-14 22:13 UTC"},
        ])

    def test_reference_summary_counts_only_explicit_input_and_output_references(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const model = sandbox.window.WorkbenchNodeInspector.viewModel({{
  input_bindings: [{{node_id: 'input-a'}}, {{node_id: 'input-b'}}],
  output_refs: [{{type: 'asset_version', id: 'asset-a'}}],
}});
console.log(JSON.stringify(model.sections[4].fields));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout), [
            {"id": "input-references", "label": "输入引用", "value": "2 项"},
            {"id": "output-references", "label": "输出引用", "value": "1 项"},
            {"id": "input-connections", "label": "输入连接", "value": "0 条"},
            {"id": "output-connections", "label": "输出连接", "value": "0 条"},
        ])
