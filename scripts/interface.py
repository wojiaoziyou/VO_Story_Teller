# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Choice:
    """
    A choice block, to set up branching storylines.

    Features:
    - Usually text-based
    - Usually have value change based on player choice
    """
    id: str
    text: list[str] = field(default_factory=list)
    options: dict[str, ChoiceOption] = field(default_factory=dict)

    lead_from: list[str] = field(default_factory=list)

@dataclass
class ChoiceOption:
    """
    A choice option mini-block, to set up effect of an option.
    """
    text: list[str] = field(default_factory=list)
    value_change: dict[str, int] = field(default_factory=dict)

    lead_to: Optional[str] = ""

@dataclass
class Ending:
    """
    An ending block, to conclude storylines.

    Features:
    - Heavily text-based
    - Lead to end of game, allow option to restart
    """
    id: str
    title: str
    text: list[str] = field(default_factory=list)

    lead_from: list[str] = field(default_factory=list)

@dataclass
class Judge:
    """
    A judge block, to decide story flow based on all the choices made so far.

    Features:
    - Math-based operations
    - Usually do not have value change
    - Value decision logic includes:
        - Deterministic: static comparison
        - Non-deterministic: randomized dice roll, similar to DnD
    """
    id: str
    condition: str
    options: dict[str, JudgeOption] = field(default_factory=dict)

    lead_from: list[str] = field(default_factory=list)
    lead_to: Optional[str] = ""

@dataclass
class JudgeOption:
    """
    A judge option mini-block, to set up effect of an option.
    """
    condition: str
    text: list[str] = field(default_factory=list)
    value_change: dict[str, int] = field(default_factory=dict)

    lead_to: Optional[str] = ""

@dataclass
class Step:
    """
    A narrative step block, to set up stages of the story.

    Features:
    - Heavily text-based
    - Occasionally have value change
    - Often have major bump in stage id
    """
    id: str
    text: list[str] = field(default_factory=list)
    value_change: dict[str, int] = field(default_factory=dict)

    lead_from: list[str] = field(default_factory=list)
    lead_to: Optional[str] = ""
