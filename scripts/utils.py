# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import time

sys.stdout.reconfigure(encoding="utf-8")


def output_line(line: str, slow_down: bool = True) -> None:
    line += "\n"
    if not slow_down:
        sys.stdout.write(line)
        sys.stdout.flush()
    else:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)
