import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FrontendWorkbenchModulesTests(unittest.TestCase):
    def test_opening_a_classic_canvas_does_not_issue_a_touch_write(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        opening = classic[classic.index("async function openCanvas(id){") : classic.index("function applyRemoteCanvasData(remote){")]
        self.assertNotIn("touchCanvasOpened", classic)
        self.assertNotIn("/touch", opening)

    def test_both_canvas_pages_load_compatibility_modules_before_editor(self):
        for page, editor in (("canvas.html", "canvas.js"), ("smart-canvas.html", "smart-canvas.js")):
            text = (ROOT / "static" / page).read_text(encoding="utf-8")
            self.assertLess(text.index("workbench/canvas/records.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/node-inspector.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/node-creation-client.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/creation-catalog.js"), text.index("workbench/canvas/command-registry.js"))
            self.assertLess(text.index("workbench/canvas/generation-intent.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/command-registry.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/runtime-state.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/graph-geometry.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/graph-interaction.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/group-membership.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/viewport-recovery.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/node-card-host.js"), text.index("workbench/canvas/unified-render-host.js"))
            self.assertLess(text.index("workbench/canvas/media-renderer.js"), text.index("workbench/canvas/unified-render-host.js"))
            self.assertLess(text.index("workbench/canvas/unified-render-host.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/node-shell.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/legacy-renderer.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/media-renderer.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/semantic-zoom.js"), text.index(editor))
            self.assertLess(text.index("workbench/canvas/screen-space-controls.js"), text.index(editor))

    def test_performance_harness_only_forwards_explicit_renderer_feature_gates(self):
        harness = (ROOT / "static" / "canvas-performance-harness.html").read_text(encoding="utf-8")
        self.assertIn("const rendererFlags = [", harness)
        self.assertIn("'node_shell', 'legacy_renderer', 'media_renderer', 'semantic_zoom'", harness)
        self.assertIn("'screen_space_controls', 'unified_canvas'", harness)
        self.assertIn(".filter(name => params.get(name) === '1')", harness)
        self.assertIn("const benchmarkNonce = Date.now();", harness)
        self.assertIn("&benchmark=1&benchmark_nonce=${benchmarkNonce}${rendererQuery}", harness)
        self.assertIn("renderer_flags=${rendererFlags.length ? rendererFlags.join(',') : 'none'}", harness)
        self.assertIn("const visibleTarget = params.get('visible') === '1';", harness)
        self.assertIn("document.body.classList.toggle('visible-target', visibleTarget);", harness)
        self.assertIn("target_visibility=${visibleTarget ? 'visible' : 'offscreen'}", harness)

    def test_classic_minimap_updates_the_viewport_box_without_rebuilding_nodes(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        harness = (ROOT / "static" / "canvas-performance-harness.html").read_text(encoding="utf-8")
        apply_viewport = classic[classic.index("function applyViewport()") : classic.index("function canvasNodeShellSemanticZoomEnabled()")]
        self.assertIn("scheduleMinimapViewportUpdate();", apply_viewport)
        self.assertNotIn("scheduleMinimapRender();", apply_viewport)
        self.assertIn("function scheduleMinimapViewportUpdate(){", classic)
        self.assertIn("updateMinimapViewport();", classic)
        self.assertIn("if(!enabled){\n        existingIndicator?.remove();\n        return;\n    }", classic)
        self.assertIn("const oldViewportStyle = oldViewport?.getAttribute('style') || '';", harness)
        self.assertIn("nextViewport.getAttribute('style') !== oldViewportStyle", harness)

    def test_unified_render_host_selects_registered_renderers_without_source_page_branches(self):
        host = (ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js").read_text(encoding="utf-8")
        card_host = (ROOT / "static" / "js" / "workbench" / "canvas" / "node-card-host.js").read_text(encoding="utf-8")
        self.assertIn("WorkbenchNodeCardHost.mount", host)
        self.assertIn("WorkbenchNodeCardHost.mountContent", host)
        self.assertIn("function mountShellAtCardBoundary(settings)", host)
        self.assertIn("function mountCard(settings)", host)
        self.assertIn("function mountAdapterCard(settings)", host)
        self.assertIn("function mountAdapterContent(settings)", host)
        self.assertIn("removeControlsBeforeMount", host)
        self.assertIn("preserveLegacyContent", host)
        self.assertIn("cardClasses must be an array", host)
        self.assertIn("function createIntentAdapter(handlers)", host)
        self.assertIn("function cardShellView(options)", host)
        self.assertIn("showDelete: settings.showDelete !== false", host)
        self.assertIn("function removeCardControls(settings)", host)
        self.assertIn("const control = card.querySelector(selector);", host)
        self.assertIn("card.querySelectorAll(selector).forEach(control => {", host)
        self.assertIn("control.remove();", host)
        self.assertIn("const handler = callbacks[intent.type];", host)
        self.assertIn("const mounted = mount(settings);", host)
        self.assertIn("mountShellAtCardBoundary({card:settings.card, contentHost:settings.contentHost, shell:mounted.shell});", host)
        self.assertIn("contentHost.replaceChildren(shell.element);", host)
        self.assertIn("card.append(inputPort);", host)
        self.assertIn("card.append(outputPort);", host)
        self.assertNotIn("smart-canvas", host)
        self.assertNotIn("canvas.js", host)
        self.assertIn("registerBuiltIns();", card_host)
        self.assertIn("hasRenderer('media', '1')", card_host)

    def test_unified_render_host_uses_one_registry_for_media_and_lossless_legacy_content(self):
        registry = ROOT / "static" / "js" / "workbench" / "canvas" / "renderer-registry.js"
        card_host = ROOT / "static" / "js" / "workbench" / "canvas" / "node-card-host.js"
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(registry))}, 'utf8'), sandbox);
const calls = [];
sandbox.window.WorkbenchNodeShell = {{create: settings => ({{
  element: {{dataset: {{}}}}, contentHost: {{}}, destroy: () => calls.push('shell-destroy'),
}})}};
sandbox.window.WorkbenchMediaRenderer = {{
  canRender: node => node.kind === 'asset',
  mount: (shell, node, options) => {{ calls.push(['media', node.id, options.legacyContent || null]); return {{destroy() {{ calls.push('media-destroy'); }}}}; }},
}};
sandbox.window.WorkbenchLegacyRenderer = {{
  canRender: node => node.renderer && node.renderer.id === 'legacy',
  mount: (shell, node, options) => {{ calls.push(['legacy', node.id, options.legacyContent]); return {{destroy() {{ calls.push('legacy-destroy'); }}}}; }},
}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(card_host))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const host = sandbox.window.WorkbenchUnifiedRenderHost;
const source = {{
  children: ['first', 'second'],
  get firstChild() {{ return this.children[0] || null; }},
}};
const adopted = host.adoptLegacyContent({{
  legacyContentHost: source,
  document: {{createElement: () => ({{
    className: '', children: [],
    appendChild(child) {{ source.children.splice(source.children.indexOf(child), 1); this.children.push(child); }},
  }})}},
}});
const media = host.mount({{node:{{id:'asset-1', kind:'asset', renderer:{{id:'legacy', version:'1'}}}}}});
const direct = host.mountContent({{node:{{id:'asset-2', kind:'asset', renderer:{{id:'legacy', version:'1'}}}}, contentHost: {{}}}});
const legacy = host.mount({{node:{{id:'legacy-1', kind:'legacy', renderer:{{id:'legacy', version:'1'}}}}, legacyContent:'preserved-dom'}});
legacy.destroy();
console.log(JSON.stringify({{
  mediaRenderer: media.renderer.id,
  directRenderer: direct.renderer.id,
  legacyRenderer: legacy.renderer.id,
  mediaDataset: media.element.dataset.rendererId,
  legacyDataset: legacy.element.dataset.rendererId,
  adoptedClass: adopted.className,
  adoptedChildren: adopted.children,
  sourceChildren: source.children,
  calls,
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        mounted = json.loads(result.stdout)
        self.assertEqual(mounted["mediaRenderer"], "media")
        self.assertEqual(mounted["directRenderer"], "media")
        self.assertEqual(mounted["legacyRenderer"], "source-payload")
        self.assertEqual(mounted["mediaDataset"], "media")
        self.assertEqual(mounted["legacyDataset"], "source-payload")
        self.assertEqual(mounted["adoptedClass"], "workbench-legacy-renderer__legacy-content")
        self.assertEqual(mounted["adoptedChildren"], ["first", "second"])
        self.assertEqual(mounted["sourceChildren"], [])
        self.assertIn(["media", "asset-1", None], mounted["calls"])
        self.assertIn(["media", "asset-2", None], mounted["calls"])
        self.assertIn(["legacy", "legacy-1", "preserved-dom"], mounted["calls"])
        self.assertIn("legacy-destroy", mounted["calls"])
        self.assertIn("shell-destroy", mounted["calls"])

    def test_unified_render_host_promotes_shell_ports_to_the_card_boundary(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{WorkbenchNodeCardHost: {{}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const inputPort = {{id:'input'}};
const outputPort = {{id:'output'}};
const shell = {{element: {{
  id:'shell',
  querySelector: selector => selector === '.workbench-node-shell__port--input' ? inputPort : selector === '.workbench-node-shell__port--output' ? outputPort : null,
}}}};
const card = {{appended: [], append: child => card.appended.push(child)}};
const contentHost = {{children: ['legacy'], replaceChildren: child => {{ contentHost.children = [child]; }}}};
const mounted = sandbox.window.WorkbenchUnifiedRenderHost.mountShellAtCardBoundary({{card, contentHost, shell}});
console.log(JSON.stringify({{
  content: contentHost.children.map(item => item.id),
  appended: card.appended.map(item => item.id),
  returned: [mounted.inputPort.id, mounted.outputPort.id],
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        mounted = json.loads(result.stdout)
        self.assertEqual(mounted["content"], ["shell"])
        self.assertEqual(mounted["appended"], ["input", "output"])
        self.assertEqual(mounted["returned"], ["input", "output"])

    def test_unified_render_host_mount_card_combines_renderer_and_card_boundary_contracts(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const inputPort = {{id:'input'}};
const outputPort = {{id:'output'}};
const shell = {{element: {{querySelector: selector => selector.endsWith('input') ? inputPort : outputPort}}}};
const received = [];
const sandbox = {{window: {{WorkbenchNodeCardHost: {{
  mount: settings => {{ received.push(settings.node.id); return {{shell, renderer: {{id:'source-payload'}}}}; }},
}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const card = {{appended: [], append: item => card.appended.push(item)}};
const contentHost = {{replaceChildren: item => {{ contentHost.child = item; }}}};
const mounted = sandbox.window.WorkbenchUnifiedRenderHost.mountCard({{node:{{id:'mixed-node'}}, card, contentHost}});
console.log(JSON.stringify({{
  received,
  childIsShell: contentHost.child === shell.element,
  appended: card.appended.map(item => item.id),
  renderer: mounted.renderer.id,
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        mounted = json.loads(result.stdout)
        self.assertEqual(mounted["received"], ["mixed-node"])
        self.assertTrue(mounted["childIsShell"])
        self.assertEqual(mounted["appended"], ["input", "output"])
        self.assertEqual(mounted["renderer"], "source-payload")

    def test_unified_render_host_mount_adapter_card_owns_control_cleanup_and_card_classes(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const calls = [];
const inputPort = {{id:'input'}};
const outputPort = {{id:'output'}};
const shell = {{element: {{querySelector: selector => selector.endsWith('input') ? inputPort : outputPort}}}};
const sandbox = {{window: {{WorkbenchNodeCardHost: {{
  mount: settings => {{ calls.push(['mount', settings.rendererOptions.legacyContent.children]); return {{shell, renderer: {{id:'legacy'}}}}; }},
}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const removed = [];
const added = [];
const preservedContent = {{
  children: [],
  appendChild: child => {{
    contentHost.children.splice(contentHost.children.indexOf(child), 1);
    preservedContent.children.push(child);
  }},
}};
const card = {{
  append: item => calls.push(`port:${{item.id}}`),
  classList: {{add: (...classes) => added.push(...classes)}},
  querySelectorAll: selector => [{{remove: () => removed.push(selector)}}],
}};
const contentHost = {{
  children: ['preserved'],
  get firstChild() {{ return this.children[0] || null; }},
  ownerDocument: {{createElement: () => preservedContent}},
  replaceChildren: () => calls.push('replace'),
}};
sandbox.window.WorkbenchUnifiedRenderHost.mountAdapterCard({{
  node: {{id:'node'}}, card, contentHost,
  controlSettings: {{selectors:['.legacy-control']}},
  removeControlsBeforeMount: true,
  preserveLegacyContent: true,
  cardClasses: ['node-shell-mounted', false, 'legacy-renderer-mounted'],
}});
console.log(JSON.stringify({{calls, removed, added}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        mounted = json.loads(result.stdout)
        self.assertEqual(mounted["removed"], [".legacy-control"])
        self.assertEqual(mounted["calls"], [["mount", ["preserved"]], "replace", "port:input", "port:output"])
        self.assertEqual(mounted["added"], ["node-shell-mounted", "legacy-renderer-mounted"])

    def test_unified_render_host_mount_adapter_content_owns_card_classes(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const received = [];
const sandbox = {{window: {{WorkbenchNodeCardHost: {{
  mountContent: settings => {{ received.push(settings); return {{element: settings.contentHost, renderer: {{id:'media'}}}}; }},
}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const added = [];
const card = {{classList: {{add: (...classes) => added.push(...classes)}}}};
const contentHost = {{id:'content'}};
const mounted = sandbox.window.WorkbenchUnifiedRenderHost.mountAdapterContent({{
  node: {{id:'media-node'}}, card, contentHost,
  cardClasses:['media-renderer-mounted'],
}});
console.log(JSON.stringify({{receivedNode: received[0].node.id, receivedHost: received[0].contentHost.id, added, renderer: mounted.renderer.id}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        mounted = json.loads(result.stdout)
        self.assertEqual(mounted["receivedNode"], "media-node")
        self.assertEqual(mounted["receivedHost"], "content")
        self.assertEqual(mounted["added"], ["media-renderer-mounted"])
        self.assertEqual(mounted["renderer"], "media")

    def test_unified_render_host_dispatches_shell_intents_through_page_callbacks(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{WorkbenchNodeCardHost: {{}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const calls = [];
const dispatch = sandbox.window.WorkbenchUnifiedRenderHost.createIntentAdapter({{
  select: intent => calls.push(['select', intent.nodeId]),
  connect_start: intent => calls.push(['connect', intent.detail.direction]),
}});
dispatch({{nodeId:'node-1', type:'select'}});
dispatch({{nodeId:'node-2', type:'connect_start', detail:{{direction:'output'}}}});
dispatch({{nodeId:'node-3', type:'resize_start'}});
dispatch({{type:'delete'}});
console.log(JSON.stringify(calls));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        self.assertEqual(json.loads(result.stdout), [["select", "node-1"], ["connect", "output"]])

    def test_unified_render_host_builds_a_page_agnostic_node_shell_view_model(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{WorkbenchNodeCardHost: {{}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const callback = () => {{}};
const defaultView = sandbox.window.WorkbenchUnifiedRenderHost.cardShellView({{selected:1, onIntent:callback}});
const outputOnly = sandbox.window.WorkbenchUnifiedRenderHost.cardShellView({{selected:false, onIntent:callback, showDelete:false, ports:{{input:false, output:true}}}});
console.log(JSON.stringify({{
  selected: defaultView.viewState.selected,
  defaultDelete: defaultView.showDelete,
  callbackKept: defaultView.onIntent === callback,
  hiddenDelete: outputOnly.showDelete,
  ports: outputOnly.ports,
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        view = json.loads(result.stdout)
        self.assertTrue(view["selected"])
        self.assertTrue(view["defaultDelete"])
        self.assertTrue(view["callbackKept"])
        self.assertFalse(view["hiddenDelete"])
        self.assertEqual(view["ports"], {"input": False, "output": True})

    def test_unified_render_host_removes_only_page_declared_legacy_controls(self):
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{WorkbenchNodeCardHost: {{}}}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const removed = [];
const card = {{querySelectorAll: selector => selector === '.legacy-port' ? [{{remove: () => removed.push('legacy-port')}}] : [{{remove: () => removed.push('legacy-resize')}}]}};
const count = sandbox.window.WorkbenchUnifiedRenderHost.removeCardControls({{card, selectors:['.legacy-port', '.legacy-resize']}});
console.log(JSON.stringify({{count, removed}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        removed = json.loads(result.stdout)
        self.assertEqual(removed["count"], 2)
        self.assertEqual(removed["removed"], ["legacy-port", "legacy-resize"])

    def test_unified_render_host_mounts_mixed_legacy_records_without_source_mode(self):
        records = ROOT / "static" / "js" / "workbench" / "canvas" / "records.js"
        registry = ROOT / "static" / "js" / "workbench" / "canvas" / "renderer-registry.js"
        card_host = ROOT / "static" / "js" / "workbench" / "canvas" / "node-card-host.js"
        unified_host = ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(records))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(registry))}, 'utf8'), sandbox);
const calls = [];
sandbox.window.WorkbenchNodeShell = {{create: () => ({{element: {{dataset: {{}}}}, contentHost: {{}}, destroy() {{}}}})}};
sandbox.window.WorkbenchMediaRenderer = {{
  canRender: node => node.kind === 'asset',
  mount: (_shell, node) => {{ calls.push(['media', node.id]); return {{destroy() {{}}}}; }},
}};
sandbox.window.WorkbenchLegacyRenderer = {{
  canRender: node => node.renderer && node.renderer.id === 'legacy',
  mount: (_shell, node) => {{ calls.push(['source-payload', node.id]); return {{destroy() {{}}}}; }},
}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(card_host))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(unified_host))}, 'utf8'), sandbox);
const adapt = sandbox.window.WorkbenchCanvas.legacyNodeView;
const records = [
  adapt({{id:'classic-prompt', type:'prompt', title:'Prompt'}}, {{canvasId:'shared'}}),
  adapt({{id:'smart-image', type:'smart-image', title:'Image'}}, {{canvasId:'shared'}}),
];
const mounted = records.map(node => sandbox.window.WorkbenchUnifiedRenderHost.mount({{node}}));
console.log(JSON.stringify({{
  kinds: records.map(node => node.kind),
  definitions: records.map(node => node.definition_ref.id),
  renderers: mounted.map(item => item.renderer.id),
  calls,
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        mounted = json.loads(result.stdout)
        self.assertEqual(mounted["kinds"], ["legacy", "asset"])
        self.assertEqual(mounted["definitions"], ["prompt", "smart-image"])
        self.assertEqual(mounted["renderers"], ["source-payload", "media"])
        self.assertEqual(mounted["calls"], [["source-payload", "classic-prompt"], ["media", "smart-image"]])

    def test_smart_canvas_cache_busts_current_node_shell_assets(self):
        page = (ROOT / "static" / "smart-canvas.html").read_text(encoding="utf-8")
        self.assertIn("smart-canvas.css?v=2026.09.04.2", page)
        self.assertIn("node-shell.js?v=2026.09.04.2", page)
        self.assertIn("records.js?v=2026.08.28.1788439786", page)
        self.assertIn("node-inspector.js?v=2026.08.28.1788441997", page)
        self.assertIn("legacy-renderer.js?v=2026.08.28.1788438695", page)
        self.assertIn("media-renderer.js?v=2026.08.28.1788438695", page)
        self.assertIn("semantic-zoom.js?v=2026.08.28.1788370356", page)
        self.assertIn("command-registry.js?v=2026.09.04.5", page)
        self.assertIn("creation-catalog.js?v=2026.09.04.1", page)
        self.assertIn("generation-intent.js?v=2026.09.04.1", page)
        self.assertIn("smart-canvas.js?v=2026.09.04.9", page)

    def test_smart_node_inspector_sections_are_ephemeral_and_collapsible(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        self.assertIn("const smartNodeInspectorCollapsedSections = new Map();", smart)
        self.assertIn("sectionId !== 'identity'", smart)
        self.assertIn("label.setAttribute('aria-expanded'", smart)
        self.assertIn("label.setAttribute('aria-controls'", smart)
        self.assertIn("smartNodeInspector?.addEventListener('keydown'", smart)
        self.assertIn("target?.closest?.('#smartNodeInspector')", smart)
        self.assertIn("if(event.key === 'Tab' && !event.shiftKey && !insideInspector", smart)
        self.assertIn("firstToggle.focus();", smart)
        self.assertIn("smartNodeInspectorTabEntryNodeId = '';", smart)
        self.assertIn("function toggleSmartNodeInspectorSection(nodeId, sectionId, options={})", smart)
        self.assertIn("toggleSmartNodeInspectorSection(toggle.dataset.inspectorNodeId", smart)
        self.assertIn("restoredToggle?.focus({preventScroll:true});", smart)
        self.assertIn("function smartNodeInspectorSelectionIdentity()", smart)
        self.assertIn("inspector.selectionViewModel(records)", smart)
        self.assertIn("function applySmartNodeSelection(nodeId, options={})", smart)
        self.assertIn("smartSelectionToggleRequested(e)", smart)
        self.assertIn("const CANVAS_SCALE_MIN = 0.06;", smart)
        self.assertIn("const CANVAS_SCALE_MAX = 3;", smart)
        self.assertIn("const CANVAS_WHEEL_DELTA_LIMIT = 240;", smart)
        self.assertIn("const nextScale = safeScale(viewport.scale * factor);", smart)
        self.assertIn("function recoverSmartViewportIfCorrupt()", smart)
        self.assertIn("function restoreSmartViewportToVisibleNodes()", smart)
        self.assertIn("if(key === 'f'){", smart)
        self.assertIn("nodeCommand('canvas.node.inspect', 'smart')", smart)
        self.assertIn("function focusSmartNodeInspector(nodeId)", smart)
        self.assertIn(".workbench-node-shell__menu::before { content:'⋯';", styles)
        self.assertIn("padding:0 84px 0 18px", styles)
        self.assertIn("right:16px; min-height:64px", styles)
        self.assertIn("workbench-node-shell__actions", styles)
        self.assertIn("workbench-node-shell__delete::before", styles)
        self.assertIn("right:10px; min-height:32px", styles)
        self.assertIn("WorkbenchUnifiedRenderHost.cardShellView({selected:isNodeSelected(node.id), onIntent:handleSmartNodeShellIntent})", smart)
        self.assertIn("const smartNodeShellIntentAdapter = window.WorkbenchUnifiedRenderHost.createIntentAdapter({", smart)
        self.assertIn("delete:intent => deleteNodeFromButton(intent.nodeId)", smart)
        self.assertIn("function ordinarySmartViewportNodes()", smart)
        self.assertIn("if(recoveredSpatialViewport) toast('检测到异常视口，已恢复到可见节点');", smart)
        self.assertIn("event.stopImmediatePropagation();", smart)
        self.assertIn("}, true);", smart)
        self.assertIn("fields.hidden = collapsed", smart)
        self.assertIn("smart-node-inspector__toggle", styles)
        self.assertIn("smart-node-inspector__toggle:focus-visible", styles)
        self.assertIn("smart-node-inspector__section.is-collapsed", styles)

    def test_smart_canvas_context_menu_matches_the_classic_single_column_treatment(self):
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        self.assertIn("width:190px", styles)
        self.assertIn("border-radius:18px", styles)
        self.assertIn(".create-menu-grid { display:flex; flex-direction:column; gap:0; }", styles)
        self.assertIn("min-height:38px", styles)
        self.assertIn(".create-card-sub { display:none; }", styles)
        self.assertIn("const w = 190;", smart)
        self.assertIn("const h = 206;", smart)

    def test_common_create_and_group_intents_use_the_shared_command_catalog(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        registry = (ROOT / "static" / "js" / "workbench" / "canvas" / "command-registry.js").read_text(encoding="utf-8")
        self.assertIn("WorkbenchCanvasCommands", registry)
        self.assertIn("canvas.create.group", registry)
        self.assertIn("canvas.selection.group", registry)
        self.assertIn("canvas.graph.connect", registry)
        self.assertIn("canvas.graph.create-connected", registry)
        self.assertIn("canvas.group.add-member", registry)
        self.assertIn("creationCatalogFor", registry)
        self.assertIn("usesVersionedBlankCreation", registry)
        self.assertIn("usesVersionedConnectedCreation", registry)
        self.assertIn("orderCreateMenuItems", registry)
        self.assertIn("WorkbenchCanvasCommands?.createCommand(type, 'classic')", classic)
        self.assertIn("WorkbenchCanvasCommands?.createCommand(type, 'smart')", smart)
        self.assertIn("canvas.selection.group', 'classic'", classic)
        self.assertIn("canvas.selection.group', 'smart'", smart)
        self.assertIn("syncClassicCreateMenuCommands", classic)
        self.assertIn("syncSmartCreateMenuCommands", smart)
        self.assertIn("creationCatalogFor('classic')", classic)
        self.assertIn("creationCatalogFor('smart')", smart)
        self.assertIn("const classicVersionedBlankNodeCreators = Object.freeze({", classic)
        self.assertIn("function createClassicMenuNode(command, point){", classic)
        self.assertIn("usesVersionedBlankCreation(command, 'classic')", classic)
        self.assertIn("const classicVersionedConnectedNodeCreators = Object.freeze({", classic)
        self.assertIn("usesVersionedConnectedCreation(command, 'classic')", classic)
        self.assertIn("function quickAdd(type){", classic)
        self.assertIn("return createClassicMenuNode(command, point);", classic)
        self.assertIn("const smartVersionedBlankNodeCreators = Object.freeze({", smart)
        self.assertIn("function createVersionedSmartTopLevelMenuNode(command, point){", smart)
        self.assertIn("usesVersionedBlankCreation(command, 'smart')", smart)
        self.assertIn("WorkbenchGenerationIntent?.planResultTarget({", smart)
        self.assertIn("const smartVersionedConnectedNodeCreators = Object.freeze({", smart)
        self.assertIn("usesVersionedConnectedCreation(command, 'smart')", smart)
        self.assertIn("graphCommand('canvas.graph.connect', 'classic')", classic)
        self.assertIn("graphCommand('canvas.graph.connect', 'smart')", smart)
        self.assertIn("graphCommand('canvas.graph.create-connected', 'smart')", smart)
        self.assertIn("graphCommand('canvas.group.add-member', 'classic')", classic)
        self.assertIn("graphCommand('canvas.group.add-member', 'smart')", smart)
        self.assertIn("openSmartPortCreateMenu(drag, e)", smart)
        self.assertIn("createSmartConnectedNodeFromMenu(command, portCreate)", smart)
        self.assertIn("group: createVersionedConnectedSmartGroup", smart)
        self.assertIn("prompt: createVersionedConnectedSmartPrompt", smart)
        self.assertIn("loop: createVersionedConnectedSmartLoop", smart)
        self.assertIn("image: createVersionedConnectedSmartImage", smart)
        self.assertIn("minimax: createVersionedConnectedSmartMinimax", smart)
        self.assertIn("applyVersionedSmartConnectedNode", smart)
        self.assertIn("WorkbenchNodeClient.createNodeAndEdge", smart)
        self.assertLess(
            smart.index("nodes.push(node);", smart.index("function applyVersionedSmartConnectedNode")),
            smart.index("const target = nodes.find", smart.index("function applyVersionedSmartConnectedNode")),
        )
        self.assertIn("connectInputNode(fromId, toId)", smart)

    def test_shared_command_catalog_orders_common_menu_items_consistently(self):
        registry = ROOT / "static" / "js" / "workbench" / "canvas" / "command-registry.js"
        catalog = ROOT / "static" / "js" / "workbench" / "canvas" / "creation-catalog.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(catalog))}, 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync({json.dumps(str(registry))}, 'utf8'), sandbox);
const api = sandbox.window.WorkbenchCanvasCommands;
const menuItems = [
  {{dataset: {{canvasCommand: 'canvas.create.group'}}, hidden: false, name: 'group'}},
  {{dataset: {{canvasCommand: 'canvas.create.image'}}, hidden: false, name: 'image'}},
  {{dataset: {{canvasCommand: 'canvas.create.llm'}}, hidden: false, name: 'llm'}},
];
const menu = api.orderCreateMenuItems(menuItems, api.creationCatalogFor('smart'));
console.log(JSON.stringify({{
  smart: api.createCommandsFor('smart').map(command => command.createType),
  classic: api.createCommandsFor('classic').slice(0, 5).map(command => command.createType),
  smartCatalog: api.creationCatalogFor('smart'),
  smartMenu: menu.map(item => item.name),
  hidden: menuItems.filter(item => item.hidden).map(item => item.name),
  versioned: {{
    classicImage: api.usesVersionedBlankCreation(api.createCommand('image', 'classic'), 'classic'),
    smartPrompt: api.usesVersionedBlankCreation(api.createCommand('prompt', 'smart'), 'smart'),
    classicMinimax: api.usesVersionedBlankCreation(api.createCommand('minimax', 'classic'), 'classic'),
  }},
  connectedVersioned: {{
    smartImage: api.usesVersionedConnectedCreation(api.createCommand('image', 'smart'), 'smart'),
    smartMinimax: api.usesVersionedConnectedCreation(api.createCommand('minimax', 'smart'), 'smart'),
    classicImage: api.usesVersionedConnectedCreation(api.createCommand('image', 'classic'), 'classic'),
    classicGroup: api.usesVersionedConnectedCreation(api.createCommand('group', 'classic'), 'classic'),
  }},
  connectedCreation: Boolean(api.graphCommand('canvas.graph.create-connected', 'classic')),
  smartConnectedCreation: Boolean(api.graphCommand('canvas.graph.create-connected', 'smart')),
  inspect: Boolean(api.nodeCommand('canvas.node.inspect', 'smart')),
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        ordered = json.loads(result.stdout)
        self.assertEqual(ordered["smart"], ["image", "prompt", "loop", "group", "minimax"])
        self.assertEqual(ordered["classic"], ordered["smart"])
        self.assertEqual(
            ordered["smartCatalog"],
            [
                {"id": "canvas.create.image", "definition_ref": {"id": "image", "type": "legacy-node", "version": "0"}, "order": 10},
                {"id": "canvas.create.prompt", "definition_ref": {"id": "prompt", "type": "legacy-node", "version": "0"}, "order": 20},
                {"id": "canvas.create.loop", "definition_ref": {"id": "loop", "type": "legacy-node", "version": "0"}, "order": 30},
                {"id": "canvas.create.group", "definition_ref": {"id": "group", "type": "legacy-node", "version": "0"}, "order": 40},
                {"id": "canvas.create.minimax", "definition_ref": {"id": "minimax", "type": "legacy-node", "version": "0"}, "order": 50},
            ],
        )
        self.assertEqual(ordered["smartMenu"], ["image", "group"])
        self.assertEqual(ordered["hidden"], ["llm"])
        self.assertEqual(ordered["versioned"], {"classicImage": True, "smartPrompt": True, "classicMinimax": False})
        self.assertEqual(ordered["connectedVersioned"], {"smartImage": True, "smartMinimax": True, "classicImage": False, "classicGroup": True})
        self.assertTrue(ordered["connectedCreation"])
        self.assertTrue(ordered["smartConnectedCreation"])
        self.assertTrue(ordered["inspect"])

    def test_creation_catalog_normalizes_generic_creation_definitions_without_side_effects(self):
        catalog = ROOT / "static" / "js" / "workbench" / "canvas" / "creation-catalog.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(catalog))}, 'utf8'), sandbox);
const api = sandbox.window.WorkbenchCreationCatalog;
const definitions = api.create([
  {{id: 'canvas.create.b', definition_ref: {{id: 'b', type: 'legacy-node', version: '0'}}, order: 20}},
  {{id: 'canvas.create.a', definition_ref: {{id: 'a', type: 'legacy-node', version: '0'}}, order: 10}},
]);
let duplicate = false;
try {{ api.create([
  {{id: 'canvas.create.a', definition_ref: {{id: 'a', type: 'legacy-node', version: '0'}}, order: 1}},
  {{id: 'canvas.create.a', definition_ref: {{id: 'a2', type: 'legacy-node', version: '0'}}, order: 2}},
]); }} catch (error) {{ duplicate = error.name === 'RangeError'; }}
console.log(JSON.stringify({{
  ids: definitions.all().map(entry => entry.id),
  definition: definitions.get('canvas.create.a').definition_ref,
  missing: definitions.get('missing'),
  duplicate,
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        output = json.loads(result.stdout)
        self.assertEqual(output["ids"], ["canvas.create.a", "canvas.create.b"])
        self.assertEqual(output["definition"], {"id": "a", "type": "legacy-node", "version": "0"})
        self.assertIsNone(output["missing"])
        self.assertTrue(output["duplicate"])

    def test_generation_intent_plans_result_placement_without_execution_side_effects(self):
        intent = ROOT / "static" / "js" / "workbench" / "canvas" / "generation-intent.js"
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(intent))}, 'utf8'), sandbox);
const api = sandbox.window.WorkbenchGenerationIntent;
console.log(JSON.stringify({{
  branch: api.planResultTarget({{sourceId:'source', isGroup:false, hasMedia:true, workflowMode:false}}),
  inPlace: api.planResultTarget({{sourceId:'source', isGroup:false, hasMedia:true, workflowMode:true}}),
  group: api.planResultTarget({{sourceId:'source', isGroup:true, hasMedia:false, workflowMode:true}}),
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        output = json.loads(result.stdout)
        self.assertEqual(output["branch"], {"sourceId": "source", "disposition": "branch"})
        self.assertEqual(output["inPlace"], {"sourceId": "source", "disposition": "in_place"})
        self.assertEqual(output["group"], {"sourceId": "source", "disposition": "branch"})

    def test_compatibility_modules_are_explicitly_dom_and_storage_free(self):
        for name in ("records.js", "node-creation-client.js", "creation-catalog.js", "generation-intent.js", "command-registry.js"):
            text = (ROOT / "static" / "js" / "workbench" / "canvas" / name).read_text(encoding="utf-8")
            self.assertNotIn("localStorage", text)
            self.assertNotIn("document.", text)

    def test_top_level_blank_image_menus_use_versioned_client_only_on_loopback(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        client = (ROOT / "static" / "js" / "workbench" / "canvas" / "node-creation-client.js").read_text(encoding="utf-8")
        self.assertIn("addVersionedBlankImageNode", classic)
        self.assertIn("canUseVersionedImageCreation()", classic)
        self.assertIn("createVersionedBlankSmartImageAt", smart)
        self.assertIn("canUseVersionedSmartImageCreation()", smart)
        self.assertIn("isLoopback", client)
        self.assertIn("isEnabled", client)
        self.assertIn("versioned_nodes", client)
        self.assertIn("undoStack.push(undoSnapshot)", classic)
        self.assertIn("undoStack.push(undoSnapshot)", smart)
        self.assertIn("addVersionedBlankPromptNode", classic)
        self.assertIn("createVersionedLinkedGroup", classic)
        self.assertIn("createNodeAndEdge", client)
        self.assertIn("createVersionedBlankSmartPrompt", smart)
        self.assertIn("createVersionedBlankSmartLoop", smart)
        self.assertIn("createVersionedBlankSmartGroup", smart)
        self.assertIn("function createVersionedSmartTopLevelMenuNode(command, point){", smart)
        self.assertIn("if(!groupId && createVersionedSmartTopLevelMenuNode(command, p))", smart)
        self.assertIn("const shouldCreateBranchOutput = resultTarget?.disposition === 'branch';", smart)
        self.assertIn("quickAdd('image')", (ROOT / "static" / "canvas.html").read_text(encoding="utf-8"))
        toolbar = (ROOT / "static" / "canvas.html").read_text(encoding="utf-8").split('<div class="toolbar-items">', 1)[1].split('</div>', 1)[0]
        for create_type in ("llm", "generator", "msgen", "video", "minimax", "rh", "comfy", "ltxDirector", "output"):
            self.assertIn(f"quickAdd('{create_type}')", toolbar)
        self.assertNotIn("onclick=\"addLLMNode()\"", toolbar)
        self.assertIn("function quickAdd(type)", classic)

    def test_node_shell_emits_intents_without_storage_or_network_side_effects(self):
        shell = (ROOT / "static" / "js" / "workbench" / "canvas" / "node-shell.js").read_text(encoding="utf-8")
        self.assertIn("WorkbenchNodeShell", shell)
        self.assertIn("contentHost", shell)
        self.assertIn("toolbarHost", shell)
        self.assertIn("drag_start", shell)
        self.assertIn("resize_start", shell)
        self.assertIn("connect_start", shell)
        self.assertNotIn("localStorage", shell)
        self.assertNotIn("fetch(", shell)

    def test_legacy_renderer_uses_one_payload_adapter_without_node_type_branches(self):
        renderer = (ROOT / "static" / "js" / "workbench" / "canvas" / "legacy-renderer.js").read_text(encoding="utf-8")
        self.assertIn("WorkbenchLegacyRenderer", renderer)
        self.assertIn("legacyPayload", renderer)
        self.assertIn("shell.contentHost", renderer)
        self.assertNotIn("node.type ===", renderer)
        self.assertNotIn("fetch(", renderer)
        self.assertNotIn("localStorage", renderer)

    def test_media_renderer_is_data_driven_and_has_no_persistence_side_effects(self):
        renderer = (ROOT / "static" / "js" / "workbench" / "canvas" / "media-renderer.js").read_text(encoding="utf-8")
        self.assertIn("WorkbenchMediaRenderer", renderer)
        self.assertIn("mediaItems", renderer)
        self.assertIn("output_refs", renderer)
        self.assertIn("mountInto", renderer)
        self.assertIn("media.preload = 'metadata'", renderer)
        self.assertIn("media.playsInline = true", renderer)
        self.assertIn("preserveNativeMediaInteraction(media)", renderer)
        self.assertIn("event.stopPropagation()", renderer)
        self.assertIn("value == null ? [] : [value]", renderer)
        self.assertIn("loading = 'lazy'", renderer)
        self.assertNotIn("node.type ===", renderer)
        self.assertNotIn("fetch(", renderer)
        self.assertNotIn("localStorage", renderer)

    def test_legacy_video_overlays_follow_the_real_playback_state(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        self.assertIn("function bindSmartVideoOverlay(video)", smart)
        self.assertIn("['play', 'playing', 'pause', 'ended']", smart)
        self.assertIn("['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'click', 'dblclick', 'contextmenu', 'wheel']", smart)
        self.assertIn("function bindCanvasVideoOverlay(video)", classic)
        self.assertIn("['play', 'playing', 'pause', 'ended']", classic)
        self.assertIn("['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'click', 'dblclick', 'contextmenu', 'wheel']", classic)

    def test_semantic_zoom_mount_is_explicit_local_and_covers_node_shell_and_legacy_nodes(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        policy = (ROOT / "static" / "js" / "workbench" / "canvas" / "semantic-zoom.js").read_text(encoding="utf-8")
        self.assertIn("function nodeShellSemanticZoomEnabled()", smart)
        self.assertIn("params.get('semantic_zoom') === '1'", smart)
        self.assertIn("params.get('node_shell') === '1'", smart)
        self.assertIn("WorkbenchSemanticZoom.viewModel(node, viewport.scale)", smart)
        self.assertIn("setAttribute('data-semantic-presentation', model.presentation)", smart)
        self.assertIn("applyNodeShellSemanticZoom();", smart)
        self.assertIn("semanticZoomIndicator", smart)
        self.assertIn("Math.round(viewport.scale * 100)", smart)
        self.assertIn("${shells.length} 节点", smart)
        self.assertIn("setVisible(slots.content, model.showContent)", smart)
        self.assertIn("port.hidden = !model.showPorts", smart)
        self.assertIn("port.style.display = model.showPorts ? '' : 'none'", smart)
        self.assertIn("function applyLegacySmartSemanticZoom(enabled)", smart)
        self.assertIn(".image-node:not(.node-shell-mounted)", smart)
        self.assertIn("smartActions:nodeEl.querySelector(':scope > .smart-node-floating-menu')", smart)
        self.assertIn("shellEl.closest('.image-node')?.querySelectorAll(':scope > .smart-node-floating-menu, :scope > .floating-node-actions')", smart)
        self.assertIn("Object.freeze(['full', 'summary'])", policy)
        self.assertIn("scale >= 0.75 ? 'full' : 'summary'", policy)
        self.assertIn('width:190px', styles)
        self.assertIn(".node-shell-semantic-zoom", styles)
        self.assertIn(".semantic-zoom-indicator", styles)
        self.assertNotIn("data-semantic-presentation=\"icon\"", styles)
        self.assertIn("function nodeShellScreenSpaceControlsEnabled()", smart)
        self.assertIn("params.get('screen_space_controls') === '1'", smart)
        self.assertIn("WorkbenchScreenSpaceControls.controlViewModel", smart)
        self.assertIn("--screen-space-port-size", styles)
        self.assertIn("--screen-space-toolbar-scale", styles)

    def test_node_shell_mount_is_explicit_and_supports_smart_groups(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        self.assertIn("node_shell", smart)
        self.assertIn("canUseNodeShellForSmartGroup", smart)
        self.assertNotIn("!smartGroupMembers(node).length", smart)
        self.assertIn("mountNodeShellForSmartGroups();", smart)
        self.assertIn("handleSmartNodeShellIntent", smart)

    def test_legacy_renderer_has_an_opt_in_non_media_smart_canvas_adapter(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        page = (ROOT / "static" / "smart-canvas.html").read_text(encoding="utf-8")
        self.assertIn("function canUseNodeShellForSmartLegacy(node)", smart)
        self.assertIn("params.get('legacy_renderer') === '1'", smart)
        self.assertIn("function mountNodeShellForSmartLegacyNodes()", smart)
        self.assertIn("mountNodeShellForSmartLegacyNodes();", smart)
        self.assertIn("preserveLegacyContent:true", smart)
        self.assertIn("function adoptLegacyContent(settings)", (ROOT / "static" / "js" / "workbench" / "canvas" / "unified-render-host.js").read_text(encoding="utf-8"))
        self.assertIn("node && !isSmartImageNode(node) && !isSmartGroupNode(node) && node.type !== 'group'", smart)
        self.assertIn(".image-node.legacy-renderer-mounted > .floating-node-actions", styles)
        self.assertIn("smart-canvas.js?v=2026.09.04.9", page)

    def test_classic_output_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'output') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.output-node .canvas-node-shell-legacy-content", styles)
        self.assertIn("overflow:auto", styles)

    def test_classic_legacy_renderer_gate_covers_all_migrated_families_and_port_contracts(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        migrated = [
            "prompt", "loop", "output", "llm", "generator", "midjourney",
            "msgen", "video", "comfy", "rh", "ltxDirector", "minimax", "promptGroup",
        ]
        self.assertIn("params.get('node_shell') === '1'", classic)
        self.assertIn("params.get('legacy_renderer') === '1'", classic)
        self.assertIn("window.WorkbenchNodeClient?.isLoopback?.()", classic)
        self.assertIn(
            "['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', "
            "'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)",
            classic,
        )
        self.assertIn("if(node?.type === 'prompt') return {input:false, output:true};", classic)
        self.assertIn("if(node?.type === 'promptGroup') return {input:false, output:true};", classic)
        for node_type in [node for node in migrated if node not in {"prompt", "promptGroup"}]:
            self.assertIn(f"if(node?.type === '{node_type}') return {{input:true, output:true}};", classic)

    def test_classic_llm_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'llm') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.llm-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.llm-node .llm-body", styles)

    def test_classic_generator_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'generator') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.generator-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.generator-node .generator-body", styles)

    def test_classic_midjourney_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'midjourney') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.midjourney-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.midjourney-node .generator-body", styles)

    def test_classic_modelscope_generation_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'msgen') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.msgen-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.msgen-node .generator-body", styles)

    def test_classic_video_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'video') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.video-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.video-node .generator-body", styles)

    def test_classic_comfy_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'comfy') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.comfy-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.comfy-node .comfy-body", styles)

    def test_classic_runninghub_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'rh') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.rh-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.rh-node .rh-body", styles)

    def test_classic_ltx_director_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'ltxDirector') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.ltxDirector-node .canvas-node-shell-legacy-content", styles)
        self.assertIn(".node.node-shell-mounted.ltxDirector-node .ltx-director-body", styles)

    def test_classic_minimax_node_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'minimax') return {input:true, output:true};", classic)
        self.assertIn(".node.node-shell-mounted.minimax-node .workbench-legacy-renderer", styles)
        self.assertIn(".node.node-shell-mounted.minimax-node .minimax-canvas-workbench", styles)

    def test_classic_prompt_group_can_use_the_opt_in_shared_legacy_renderer(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("if(node?.type === 'promptGroup') return {input:false, output:true};", classic)
        self.assertIn("if(node.type === 'promptGroup') {", classic)
        self.assertIn("${promptNodes.length} ${tr('canvas.promptCount')} ${tr('canvas.grouped')}", classic)

    def test_prompt_node_uses_the_compact_llm_card_hierarchy(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        self.assertIn('class="prompt-node-studio-head"', smart)
        self.assertIn('class="prompt-node-models"', smart)
        self.assertIn('class="prompt-node-tools prompt-node-footer ${node.promptSkillEnabled', smart)
        self.assertIn('class="prompt-node-run prompt-node-control"', smart)
        self.assertIn(".prompt-node-studio-head", styles)
        self.assertIn(".prompt-node-models", styles)
        self.assertIn(".prompt-node-footer", styles)
        self.assertIn('promptSkillPack', smart)
        self.assertIn('promptSkillDefinition', smart)
        self.assertIn('function openPromptNodeUpload(nodeId)', smart)
        self.assertIn('function attachFilesToPromptNode(files, nodeId)', smart)
        self.assertIn('function promptNodeSkillSystemPrompt(node)', smart)
        self.assertIn('const PROMPT_SKILL_VISUAL_CATALOG', smart)
        self.assertIn('function promptSkillVisual(pack, definition)', smart)
        self.assertIn('聘才猫简历优化', smart)
        self.assertIn('Pincaimiao Skills', smart)
        self.assertIn('node.title = visual.definition;', smart)
        self.assertIn('function promptNodeContextChipsHtml(node, upstreamItems=[])', smart)
        self.assertIn('class="prompt-node-context-row"', smart)
        self.assertIn('data-lucide="brain"', smart)
        self.assertIn("node.title = node.promptSkillEnabled ? promptSkillVisual", smart)
        self.assertIn('.prompt-node-footer .prompt-skill-toggle:not(.active)', styles)
        self.assertIn('.image-node.prompt-smart-node.node-shell-mounted .workbench-node-shell__header', styles)
        self.assertIn('.image-node.prompt-smart-node.node-shell-mounted .workbench-node-shell__footer', styles)
        self.assertIn('.image-node.prompt-smart-node.node-shell-mounted .workbench-node-shell__resize', styles)
        self.assertIn('container-name:prompt-card; overflow:visible; border:1px solid #e8edf3; border-radius:18px; background:rgba(255,255,255,.96)', styles)
        self.assertIn('box-sizing:border-box; gap:0; padding:0; overflow:hidden; border:0; border-radius:inherit; background:transparent; box-shadow:none;', styles)
        self.assertIn('margin:0 18px 18px; padding-right:32px;', styles)
        self.assertIn('@container prompt-card (max-width: 420px)', styles)
        self.assertIn('.image-node.prompt-smart-node.node-shell-mounted .workbench-node-shell__port--input', styles)
        self.assertIn('.image-node.prompt-smart-node.node-shell-mounted .workbench-node-shell__port--output', styles)
        self.assertIn('visibility\n   still follows the shared selected/hover/connection interaction contract', styles)
        self.assertIn('WorkbenchUnifiedRenderHost.mountAdapterCard({', smart)
        self.assertIn('card:el, contentHost,', smart)
        self.assertIn('function nodeShellPortElements(shellEl)', smart)
        self.assertIn('w:340, h:286', smart)
        self.assertIn('function promptNodeOutputItems(node)', smart)
        self.assertIn('node.promptResult = (result.text || \'\').trim();', smart)
        self.assertIn('node.promptResultOutdated = false;', smart)
        self.assertIn("node?.promptResultOutdated === true", smart)
        self.assertIn('prompt-node-result ${node.promptResultOutdated', smart)
        self.assertIn("node?.promptOutputMode === 'list'", smart)
        self.assertIn('system_prompt:systemPrompt', smart)
        self.assertIn('function smartMinimaxUpstreamScript(node)', smart)
        self.assertIn('function smartMinimaxApplyUpstreamScript(node)', smart)
        self.assertIn('class="minimax-upstream-script"', smart)
        self.assertIn('未填写片段 Prompt 时将用于生成', smart)
        self.assertIn('data-minimax-apply-upstream="1"', smart)
        self.assertIn("if(node?.type === 'smart-prompt'){", smart)
        self.assertIn('return promptNodeInputMediaForLLM(node)', smart)
        self.assertIn("selectSmartNodeFromShell", smart)
        self.assertIn("startSmartPortDrag", smart)
        self.assertIn("startSmartNodeDrag", smart)
        self.assertIn("startSmartNodeResize", smart)

    def test_node_shell_ports_emit_mouse_coordinates_and_use_legacy_port_contract(self):
        shell = (ROOT / "static" / "js" / "workbench" / "canvas" / "node-shell.js").read_text(encoding="utf-8")
        self.assertIn("connect_start", shell)
        self.assertIn("clientX: event.clientX", shell)
        self.assertIn("clientY: event.clientY", shell)
        self.assertIn("workbench-node-shell__port", shell)
        self.assertNotIn("node-port", shell)
        self.assertIn("dataset.port", shell)
        self.assertIn("resize_start", shell)
        self.assertIn("drag_start", shell)
        self.assertIn("port.addEventListener('mousedown'", shell)
        self.assertIn("resize.addEventListener('mousedown'", shell)
        self.assertIn("header.addEventListener('mousedown'", shell)
        self.assertIn("event.stopPropagation();", shell)
        self.assertNotIn("pointerdown", shell)

    def test_legacy_renderer_can_preserve_existing_legacy_content_in_a_shell_slot(self):
        renderer = (ROOT / "static" / "js" / "workbench" / "canvas" / "legacy-renderer.js").read_text(encoding="utf-8")
        self.assertIn("legacyContent", renderer)
        self.assertIn("root.append(legacyContent)", renderer)

    def test_node_shell_mount_removes_legacy_controls_owned_by_the_shell(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        self.assertIn("controlSettings:{selectors:SMART_NODE_SHELL_LEGACY_CONTROLS}", smart)
        self.assertIn("removeControlsBeforeMount:true", smart)

    def test_node_shell_ports_override_legacy_port_geometry(self):
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        self.assertIn(".image-node.node-shell-mounted .workbench-node-shell__port", styles)
        self.assertIn(".image-node.node-shell-mounted.selected > .workbench-node-shell__port", styles)
        self.assertIn(".image-node.node-shell-mounted.port-dragging > .workbench-node-shell__port", styles)
        self.assertIn(".workbench-node-shell__port--input { left:-8px; right:auto; }", styles)
        self.assertIn(".workbench-node-shell__port--output { right:-8px; left:auto; }", styles)
        self.assertIn(".shell.port-dragging .workbench-node-shell__port", styles)
        self.assertIn(".image-node.node-shell-mounted.dragging .workbench-node-shell__port", styles)

    def test_smart_group_node_shell_uses_classic_group_card_treatment(self):
        styles = (ROOT / "static" / "css" / "smart-canvas.css").read_text(encoding="utf-8")
        self.assertIn("Smart Group NodeShell adopts the established Classic Canvas group card", styles)
        self.assertIn(".image-node.smart-group-node.node-shell-mounted .workbench-node-shell__header", styles)
        self.assertIn("min-height:66px", styles)
        self.assertIn(".workbench-node-shell__menu::before { content:'⋯'", styles)

    def test_smart_canvas_accepts_both_legacy_and_node_shell_ports(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        self.assertIn(".node-port, .workbench-node-shell__port", smart)
        self.assertIn('querySelector(`[data-port="${portDragState.hoverPort}"]`)', smart)

    def test_media_renderer_mount_is_explicit_and_limited_to_top_level_smart_images(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        self.assertIn("canUseMediaRendererForSmartImage", smart)
        self.assertIn("media_renderer", smart)
        self.assertIn("mountNodeShellForSmartImages();", smart)
        self.assertIn("smart-group-member-node", smart)
        self.assertIn("WorkbenchUnifiedRenderHost.mount", smart)

    def test_media_renderer_has_opt_in_group_and_classic_canvas_adapters(self):
        smart = (ROOT / "static" / "js" / "smart-canvas.js").read_text(encoding="utf-8")
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        self.assertIn("canUseMediaRendererForSmartGroup", smart)
        self.assertIn("smartGroupMediaRecord", smart)
        self.assertIn("const ownMedia = (node.images || [])", smart)
        self.assertIn("canUseCanvasMediaRenderer", classic)
        self.assertIn("canvasMediaRecord", classic)
        self.assertIn("WorkbenchUnifiedRenderHost.mountAdapterContent", classic)
        self.assertIn("cardClasses:['media-renderer-mounted']", classic)

    def test_classic_media_node_shell_reuses_legacy_gesture_and_link_state_machines(self):
        classic = (ROOT / "static" / "js" / "canvas.js").read_text(encoding="utf-8")
        styles = (ROOT / "static" / "css" / "canvas.css").read_text(encoding="utf-8")
        page = (ROOT / "static" / "canvas.html").read_text(encoding="utf-8")
        self.assertIn("function canvasNodeShellEnabled()", classic)
        self.assertIn("params.get('node_shell') === '1'", classic)
        self.assertIn("function mountCanvasNodeShellForMedia", classic)
        self.assertIn("onclick=\"menuAdd('group')\"", page)
        self.assertIn("function addVersionedBlankGroupNode", classic)
        self.assertIn("definition_ref:{type:'legacy', id:'group', version:'0'}", classic)
        self.assertIn("node?.type === 'group'", classic)
        self.assertIn("workbench-node-shell__group-empty", classic)
        self.assertIn("WorkbenchUnifiedRenderHost.mount", classic)
        self.assertIn("canvas-node-shell-legacy-content", classic)
        self.assertIn("WorkbenchUnifiedRenderHost.mountAdapterCard({", classic)
        self.assertIn("card:el, contentHost:body", classic)
        self.assertIn("controlSettings:CANVAS_NODE_SHELL_LEGACY_CONTROLS", classic)
        self.assertIn("cardClasses:['node-shell-mounted'", classic)
        self.assertIn("function canvasLegacyRendererEnabled()", classic)
        self.assertIn("params.get('legacy_renderer') === '1'", classic)
        self.assertIn("function mountCanvasNodeShellForLegacy", classic)
        self.assertIn("['prompt', 'loop', 'output', 'llm', 'generator', 'midjourney', 'msgen', 'video', 'comfy', 'rh', 'ltxDirector', 'minimax', 'promptGroup'].includes(node?.type)", classic)
        self.assertIn("function canvasLegacyNodeShellPorts(node)", classic)
        self.assertIn("node?.type === 'loop'", classic)
        self.assertIn("if(node?.type === 'loop') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'llm') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'generator') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'midjourney') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'msgen') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'video') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'comfy') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'rh') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'ltxDirector') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'minimax') return {input:true, output:true};", classic)
        self.assertIn("if(node?.type === 'promptGroup') return {input:false, output:true};", classic)
        self.assertIn("ports:canvasLegacyNodeShellPorts(node)", classic)
        self.assertIn("WorkbenchUnifiedRenderHost.cardShellView({selected:selected.has(node.id), onIntent:handleCanvasNodeShellIntent, ports:canvasLegacyNodeShellPorts(node)})", classic)
        self.assertIn("portVisibility.input !== false", (ROOT / "static" / "js" / "workbench" / "canvas" / "node-shell.js").read_text(encoding="utf-8"))
        self.assertIn("if(to.type === 'group') return ['image','prompt'].includes(from.type)", classic)
        self.assertIn("group.items.push(fromId)", classic)
        self.assertIn("function canvasNodeShellSemanticZoomEnabled()", classic)
        self.assertIn("params.get('semantic_zoom') === '1'", classic)
        self.assertIn("WorkbenchSemanticZoom.viewModel(node, viewport.scale)", classic)
        self.assertIn("nodeEl.dataset.semanticPresentation = model.presentation", classic)
        self.assertIn(".node:not(.node-shell-mounted)", classic)
        self.assertIn("canvasSemanticZoomIndicator", classic)
        self.assertIn("WorkbenchUnifiedRenderHost.mount", classic)
        self.assertIn("handleCanvasNodeShellIntent", classic)
        self.assertIn("startNodeDrag(canvasShellPointer(intent.detail), node)", classic)
        self.assertIn("startNodeResize(canvasShellPointer(intent.detail), node)", classic)
        self.assertIn("startLink(canvasShellPointer(intent.detail)", classic)
        self.assertIn(".workbench-node-shell__port--output", classic)
        self.assertIn(".node.node-shell-mounted .workbench-node-shell", styles)
        self.assertIn(".workbench-node-shell__content > .workbench-media-renderer", styles)
        self.assertIn(".node.node-shell-mounted .workbench-legacy-renderer", styles)
        self.assertIn("margin:12px; border-radius:16px", styles)
        self.assertIn("display:flex; flex:1; min-height:0; overflow:hidden", styles)
        self.assertIn("border:0; border-radius:inherit; background:transparent", styles)
        self.assertIn(".node.node-shell-mounted > .workbench-node-shell__port", styles)
        self.assertIn(".node-shell-semantic-zoom .node:not(.node-shell-mounted)[data-semantic-presentation=\"summary\"]", styles)
        self.assertIn(".canvas-semantic-zoom-indicator", styles)
        self.assertIn(".workbench-node-shell__port--input { left:-25px; }", styles)
        self.assertIn(".workbench-node-shell__port--output { right:-21px; }", styles)
        self.assertIn("canvas.css?v=2026.09.04.1", page)
        self.assertIn("command-registry.js?v=2026.09.04.5", page)
        self.assertIn("creation-catalog.js?v=2026.09.04.1", page)
        self.assertIn("generation-intent.js?v=2026.09.04.1", page)
        self.assertIn("canvas.js?v=2026.09.04.16", page)
        self.assertIn("WorkbenchUnifiedRenderHost.cardShellView({selected:selected.has(node.id), onIntent:handleCanvasNodeShellIntent})", classic)
        self.assertIn("const canvasNodeShellIntentAdapter = window.WorkbenchUnifiedRenderHost.createIntentAdapter({", classic)
        self.assertIn("delete:intent => deleteNodeFromButton(intent.nodeId)", classic)
        self.assertIn("workbench-node-shell__actions", styles)
        self.assertIn("workbench-node-shell__delete::before", styles)
