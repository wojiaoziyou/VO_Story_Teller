# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from termcolor import colored
import time

os.system("color")
sys.stdout.reconfigure(encoding="utf-8")


def output_line(
    line: str, slow_down: bool = True, color: str = "white", attrs: list = ["bold"]
) -> None:
    """Output line to terminal in slow-down speed and colors
    
    Parameters
    ----------
    line : str
        The contexts to output
    slow_down : bool, optional
        Whether to slow down (default is True)
    color : str, optional
        The color of contexts in terminal (default is "white")
        Rule of colors:
        - "white": most of informational contexts
        - "red": for warnings and bad endings
        - "green": for breakthroughs and good endings
        - "yellow": for choices
        - "blue": [no suggestion]
        - "magenta": for change of scores (only for debugging)
        - "cyan": for dialogues
    attrs : list, optional
        The special effects of contexts in terminal (default is ["bold"])
        Other useful options include: underline, reverse
    """
    if not slow_down:
        sys.stdout.write(colored(line, color, attrs=attrs))
        sys.stdout.flush()
    else:
        for char in line:
            sys.stdout.write(colored(char, color, attrs=attrs))
            sys.stdout.flush()
            time.sleep(0.03)
    sys.stdout.write("\n")
    sys.stdout.flush()
