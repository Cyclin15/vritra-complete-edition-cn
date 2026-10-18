# -*- coding: utf-8 -*-
import os, sys
from view import view
ROOT = os.path.dirname(os.path.abspath(__file__))
UI = os.path.join(ROOT, '..', 'Resources', 'asset_ui')
for f, w in [('ranking_tab.png', 160), ('replaylist_tab.png', 155),
             ('practice_tab.png', 122),
             ('weponset_btn_a_off.png', 170), ('weponset_btn_a_on.png', 170),
             ('weponset_btn_b_off.png', 170),
             ('config_controller.png', 160)]:
    print()
    view(os.path.join(UI, f), w)
