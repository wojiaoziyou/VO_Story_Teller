# -*- coding: utf-8 -*-
from __future__ import annotations

# Constants
rider_cnt: int = 10  # Step_2
v_love_ending_5: int = 1  # Ending_5
v_intelligence_ending_5: int = 5  # Ending_5 (TODO: TBD)
order_num_low_judge_7: float = 30  # Judge_7 (TODO: TBD)
order_num_high_judge_7: float = 40  # Judge_7 (TODO: TBD)
o_intelligence_judge_8_1: int = 5  # Judge_8_1 (TODO: TBD)
o_love_judge_9: int = 4  # Judge_9 (TODO: TBD)

# Variables initialized at beginning
rider_ids: list[int] = []  # Step_2

# Variables changed in game
# V info
v_name: str = "5-1000"
v_intelligence: int = 0
v_strength: int = 0
v_love: int = 0

# O info
o_name: str = "0113号骑手"
o_intelligence: int = 0
o_strength: int = 0
o_love: int = 0

# System info
s_strength: int = 10
s_emotion: int = 0

# Flag values
activity_cnt: int = 0  # Choice_1
tip_flag: bool = False  # Judge_1_1
music_flag: bool = False  # Choice_1_2
painting_flag: bool = False  # Choice_1_3
poetry_flag: bool = False  # Choice_1_4

reward_cnt: int = 0  # Choice_2_1, Judge_2_1
punish_cnt: int = 0  # Choice_2_2, Judge_2_2
attention_flag: bool = False  # Choice_2_2, Judge_2_2
photo_flag: bool = False  # Step 4
camera_flag: bool = False  # Step_5_1

v_name_flag: bool = False  # Step 12
v_love_feeling_flag: bool = False  # Step12-1

# Stage 6-7 loops
order_num: int = 10  # Choice_6
