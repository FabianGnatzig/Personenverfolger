"""
Created by Fabian Gnatzig in 2024
Contact: fabiangnatzig@gmx.de
"""
import dataclasses

import numpy as np


@dataclasses.dataclass
class Constants:
    """
    Constants class for camera.
    """
    H_COLOR_BORDER = 179
    S_COLOR_BORDER = 255
    V_COLOR_BORDER = 255
    H_STEP = 15
    S_STEP = 32
    V_STEP = 32
    ESC_KEY = 27
    ENTER_KEY = 13
    BLUR = 10
    NULL_ARRAY = np.array([0, 0, 0])
    NEW_REGION_STRING = "##############################################################"
