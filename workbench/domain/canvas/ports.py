"""Typed, generic input and output port contracts."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


PortId = Annotated[str, Field(min_length=1, max_length=160)]
ArtifactType = Annotated[str, Field(min_length=1, max_length=160)]


class InputPort(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: PortId
    accepts: list[ArtifactType] = Field(min_length=1)
    required: bool = False
    multiple: bool = False


class OutputPort(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: PortId
    produces: list[ArtifactType] = Field(min_length=1)
    multiple: bool = False


class PortSet(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    inputs: list[InputPort] = Field(default_factory=list)
    outputs: list[OutputPort] = Field(default_factory=list)
