"""Enum Classes for Mirascope CLI."""
from enum import Enum, EnumMeta
from typing import Any


class _Metaclass(EnumMeta):
    """Base `EnumMeta` subclass for accessing enum members directly."""

    def __getattribute__(cls, __name: str) -> Any:
        value = super().__getattribute__(__name)
        if isinstance(value, Enum):
            value = value.value
        return value


class _Enum(str, Enum, metaclass=_Metaclass):
    """Base Enum Class."""


class MirascopeCommand(_Enum):
    """CLI commands to be executed.

    - ADD: save a modified prompt to the `versions/` folder.
    - USE: load a specific version of the prompt from `versions/` as the current prompt.
    - STATUS: display if any changes have been made to prompts, and if a prompt is
        specified, displays changes for only said prompt.
    - INIT: initializes the necessary folders for prompt versioning with CLI.
    """

    ADD = "add"
    USE = "use"
    STATUS = "status"
    INIT = "init"
