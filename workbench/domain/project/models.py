"""Pydantic records for the R3 Project/Canvas authority boundary."""

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


PROJECT_SCHEMA_VERSION = "workbench.project/1"
CANVAS_SCHEMA_VERSION = "workbench.canvas/1"
OpaqueId = Annotated[str, Field(min_length=1, max_length=255)]
ProjectRole = Literal["owner", "editor", "viewer"]


class ProjectRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal[PROJECT_SCHEMA_VERSION] = PROJECT_SCHEMA_VERSION
    id: OpaqueId
    name: Annotated[str, Field(min_length=1, max_length=500)]
    workspace_id: OpaqueId
    created_by: OpaqueId
    created_at: datetime
    updated_at: datetime
    revision: Annotated[int, Field(ge=1)] = 1
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProjectMember(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    project_id: OpaqueId
    actor_id: OpaqueId
    role: ProjectRole
    created_at: datetime


class CanvasRecord(BaseModel):
    """Canonical graph-container metadata; graph payload stays lossless during R3."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal[CANVAS_SCHEMA_VERSION] = CANVAS_SCHEMA_VERSION
    id: OpaqueId
    project_id: OpaqueId
    title: Annotated[str, Field(min_length=1, max_length=500)]
    viewport: dict[str, Any] = Field(default_factory=dict)
    revision: Annotated[int, Field(ge=1)] = 1
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
