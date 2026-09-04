"""Industry-neutral renderer manifests for the finite Canvas renderer set."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import NodeKind, RendererRef


RENDERER_MANIFEST_SCHEMA_VERSION = "workbench.renderer/1"


class RendererManifest(BaseModel):
    """A renderer capability declaration, independent of Skills and providers."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal[RENDERER_MANIFEST_SCHEMA_VERSION] = RENDERER_MANIFEST_SCHEMA_VERSION
    renderer: RendererRef
    display_name: str = Field(min_length=1, max_length=120)
    supported_kinds: tuple[NodeKind, ...] = Field(min_length=1)
    view_model_version: str = Field(min_length=1, max_length=120)
    supports_ports: bool = True
    supports_selection: bool = True
    supports_resize: bool = True

