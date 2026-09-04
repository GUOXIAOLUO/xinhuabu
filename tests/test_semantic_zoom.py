import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "static" / "js" / "workbench" / "canvas" / "semantic-zoom.js"


class SemanticZoomTests(unittest.TestCase):
    def invoke(self):
        script = f"""
const fs = require('fs');
const vm = require('vm');
const sandbox = {{window: {{}}}};
vm.runInNewContext(fs.readFileSync({json.dumps(str(MODULE))}, 'utf8'), sandbox);
const api = sandbox.window.WorkbenchSemanticZoom;
const hundred = Array.from({{length: 100}}, (_, index) => ({{id: `n-${{index}}`}}));
const threeHundred = Array.from({{length: 300}}, (_, index) => ({{id: `n-${{index}}`}}));
console.log(JSON.stringify({{
  levels: [api.presentationForScale(1), api.presentationForScale(.75), api.presentationForScale(.749), api.presentationForScale(.1)],
  full: api.viewModel({{id: 'one'}}, 1),
  summary: api.viewModel({{id: 'one'}}, .1),
  hundred: api.viewModels(hundred, .6).length,
  threeHundred: api.viewModels(threeHundred, .25).length,
}}));
"""
        result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
        return json.loads(result.stdout)

    def test_two_semantic_presentations_and_batch_view_models(self):
        result = self.invoke()
        self.assertEqual(result["levels"], ["full", "full", "summary", "summary"])
        self.assertTrue(result["full"]["showContent"])
        self.assertTrue(result["summary"]["showTitle"])
        self.assertTrue(result["summary"]["showPorts"])
        self.assertFalse(result["summary"]["showContent"])
        self.assertEqual((result["hundred"], result["threeHundred"]), (100, 300))
