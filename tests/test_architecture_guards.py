"""Automated architecture guards for the merged R4 state.

Each guard pins one AGENTS.md hard constraint against the current source tree.
They are source scans on purpose: they must hold for any future edit without a
running server, and a violation must fail the suite before merge.
"""

import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CORE_PYTHON_LAYERS = ("workbench/domain", "workbench/application")
ALL_PYTHON_SURFACES = ("workbench", "main.py")
PRODUCT_JS_ROOT = "static/js"
PRODUCT_JS_EXCLUDED = (ROOT / "static" / "vendor",)
PRODUCT_HTML = tuple((ROOT / "static").glob("*.html"))

FORBIDDEN_GIT_HOSTING_PATTERNS = (
    "raw.githubusercontent.com",
    "codeload.github.com",
    "github.com/raw/",
    "github.com/tree/",
    "gist.githubusercontent.com",
)


def iter_python_files(relative_roots):
    for root in relative_roots:
        root_path = ROOT / root
        if root_path.is_file():
            yield root_path
            continue
        for path in sorted(root_path.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            yield path


def imported_modules(path):
    """Return absolute dotted module names referenced by imports in one file.

    Relative imports are resolved against the file's package path so a
    `from ..codex import x` inside a core layer cannot hide behind its level.
    """
    package_parts = path.parent.relative_to(ROOT).parts
    modules = set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module)
            if node.level:
                # `from .sibling import x` inside workbench/domain resolves
                # against the file's own package; level counts the dots.
                base = package_parts[: len(package_parts) - (node.level - 1)] if node.level > 1 else package_parts
                if node.module:
                    modules.add(".".join([*base, node.module]))
                else:
                    modules.add(".".join(base))
    return modules


def iter_product_js_files():
    for path in sorted((ROOT / PRODUCT_JS_ROOT).rglob("*.js")):
        if any(PRODUCT_JS_EXCLUDED[0] in path.parents for _ in [0]) or str(PRODUCT_JS_EXCLUDED[0]) in str(path):
            continue
        yield path


class ArchitectureGuardsTests(unittest.TestCase):
    def test_core_domain_and_application_do_not_import_codex_runtime(self):
        # AGENTS.md §15: core domain must not import raw Codex runtime/protocol
        # modules; only workbench/codex owns that boundary.
        violations = []
        for path in iter_python_files(CORE_PYTHON_LAYERS):
            for module in imported_modules(path):
                if module == "codex" or module.startswith("codex.") or module == "workbench.codex" or module.startswith("workbench.codex."):
                    violations.append(f"{path.relative_to(ROOT)} -> {module}")
        self.assertEqual(violations, [])

    def test_core_python_surfaces_do_not_reference_wholehouse_package(self):
        # AGENTS.md §1: core remains industry-neutral; WholeHouse belongs under
        # packages/wholehouse and must never be imported by Core surfaces.
        violations = []
        for path in iter_python_files(ALL_PYTHON_SURFACES):
            source = path.read_text(encoding="utf-8")
            for module in imported_modules(path):
                if "wholehouse" in module.lower():
                    violations.append(f"{path.relative_to(ROOT)} imports {module}")
            if "wholehouse" in source.lower().replace("wholehouse belongs", ""):
                # String references count too: they create the same coupling.
                for line_number, line in enumerate(source.splitlines(), start=1):
                    if "wholehouse" in line.lower() and not line.strip().startswith("#"):
                        violations.append(f"{path.relative_to(ROOT)}:{line_number} mentions wholehouse")
        self.assertEqual(violations, [])

    def test_product_runtime_sources_have_no_git_hosting_fetch_dependency(self):
        # AGENTS.md §29: no GitHub raw/tree URLs, no source-repository update
        # code, no startup dependency on Git hosting. Plain repository page
        # links (e.g. window.open to an upstream project) stay allowed.
        violations = []
        surfaces = [ROOT / "main.py", *iter_product_js_files(), *PRODUCT_HTML]
        for path in surfaces:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for pattern in FORBIDDEN_GIT_HOSTING_PATTERNS:
                if pattern in lowered:
                    violations.append(f"{path.relative_to(ROOT)} contains {pattern}")
            for line_number, line in enumerate(text.splitlines(), start=1):
                if ".git\"" in line or ".git'" in line or line.rstrip().endswith(".git"):
                    violations.append(f"{path.relative_to(ROOT)}:{line_number} references a .git URL")
        self.assertEqual(violations, [])

    def test_guard_surface_inventory_is_nonempty(self):
        # The guards above are only meaningful while the scanned surfaces exist.
        self.assertGreater(len(list(iter_python_files(CORE_PYTHON_LAYERS))), 0)
        self.assertGreater(len(list(iter_product_js_files())), 0)
        self.assertGreater(len(PRODUCT_HTML), 0)


if __name__ == "__main__":
    unittest.main()
