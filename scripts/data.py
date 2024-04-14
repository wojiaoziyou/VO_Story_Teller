# -*- coding: utf-8 -*-
from __future__ import annotations

# Constants
rider_cnt: int = 10

# Variables initialized at beginning
rider_ids: list[int]  # Step_2

# Variables changed in game
# V info
v_name: str = "5-1000"
v_intelligence: int
v_strength: int
v_love: int

# O info
o_name: str = "0113号骑手"
o_intelligence: int
o_strength: int
o_love: int

# System info
s_strength: int

# Flag values
tip_flag: bool  # Judge_1_1
music_flag: bool  # Choice_1_2
painting_flag: bool  # Choice_1_3
poetry_flag: bool  # Choice_1_4

comfort_flag: bool
awake_flag: bool
suicide_flag: bool

reward_cnt: int  # Choice_2_1, Judge_2_1
punish_cnt: int  # Choice_2_2, Judge_2_2
attention_flag: bool  # Choice_2_2, Judge_2_2
photo_flag: bool  # Step 4
monthly_ranking_flag: bool  # Step_13_2

# Stage 6-7 loops
order_num: int = 10  # Choice_6