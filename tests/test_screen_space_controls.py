import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "static" / "js" / "workbench" / "canvas" / "screen-space-controls.js"


class ScreenSpaceControlsTests(unittest.TestCase):
    def test_controls_keep_target_pixel_size_across_zoom_range(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const api = sandbox.window.WorkbenchScreenSpaceControls;
const node = {{id: 'node-1', position: {{x: 10, y: 20}}, size: {{width: 100, height: 80}}}};
console.log(JSON.stringify({{
  screen: api.worldToScreen({{x: 10, y: 20}}, {{x: 5, y: 7, scale: 2}}),
  near: api.controlViewModel(node, {{x: 0, y: 0, scale: .25}}, 28),
  far: api.controlViewModel(node, {{x: 0, y: 0, scale: 2}}, 28),
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        values = json.loads(result.stdout)
        self.assertEqual(values["screen"], {"x": 25, "y": 47})
        self.assertEqual(values["near"]["targetPixels"], values["far"]["targetPixels"])
        self.assertEqual((values["near"]["worldControlSize"], values["far"]["worldControlSize"]), (112, 14))
        self.assertEqual(values["far"]["toolbar"], {"x": 120, "y": 40})
        self.assertEqual(values["far"]["inputPort"], {"x": 20, "y": 120})
        self.assertEqual(values["far"]["outputPort"], {"x": 220, "y": 120})
