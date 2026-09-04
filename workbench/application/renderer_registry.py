"""Application registry for Canvas renderers.

The registry deliberately has no Skill, provider, DOM, or persistence dependency.
"""

from collections.abc import Iterable

from workbench.domain.canvas.models import NodeRecord, RendererRef
from workbench.domain.canvas.renderers import RendererManifest


class RendererRegistryError(ValueError):
    """Raised when renderer registration or resolution violates its contract."""


class RendererRegistry:
    """Resolve a finite, versioned renderer set without branching on Skill IDs."""

    def __init__(self, manifests: Iterable[RendererManifest] = ()):
        self._manifests: dict[tuple[str, str], RendererManifest] = {}
        for manifest in manifests:
            self.register(manifest)

    def register(self, manifest: RendererManifest) -> None:
        key = self._key(manifest.renderer)
        if key in self._manifests:
            raise RendererRegistryError(f"renderer is already registered: {manifest.renderer.id}@{manifest.renderer.version}")
        self._manifests[key] = manifest

    def resolve(self, renderer: RendererRef) -> RendererManifest | None:
        return self._manifests.get(self._key(renderer))

    def require(self, renderer: RendererRef) -> RendererManifest:
        manifest = self.resolve(renderer)
        if manifest is None:
            raise RendererRegistryError(f"renderer is not registered: {renderer.id}@{renderer.version}")
        return manifest

    def supports(self, node: NodeRecord) -> bool:
        manifest = self.resolve(node.renderer)
        return manifest is not None and node.kind in manifest.supported_kinds

    def all(self) -> tuple[RendererManifest, ...]:
        return tuple(self._manifests.values())

    @staticmethod
    def _key(renderer: RendererRef) -> tuple[str, str]:
        return renderer.id, renderer.version

