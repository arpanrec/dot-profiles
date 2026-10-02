"""
This module defines and validates the schema of conf.yaml.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConfigEntry(BaseModel):
    """One named entry of the "save" or "export" section."""

    model_config = ConfigDict(extra="forbid")

    location: str = Field(min_length=1)
    entries: list[str] = Field(default_factory=list[str])

    @field_validator("entries", mode="before")
    @classmethod
    def empty_entries_to_list(cls, value: Any) -> Any:
        """Treats an empty "entries" key, which yaml parses as None, as an empty list.

        Args:
            value: the raw value of "entries"
        """
        return [] if value is None else value


class Config(BaseModel):
    """The whole conf.yaml file."""

    model_config = ConfigDict(extra="forbid")

    save: dict[str, ConfigEntry] = Field(default_factory=dict[str, ConfigEntry])
    export: dict[str, ConfigEntry] = Field(default_factory=dict[str, ConfigEntry])

    def sections(self) -> list[dict[str, ConfigEntry]]:
        """Returns the "save" and "export" sections."""
        return [self.save, self.export]
