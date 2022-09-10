# ****************************** Imports ****************************** #


import enum


# ****************************** Physical ****************************** #


c = 299792458

# URAD limits
urad_fc_min = 24.000e9
urad_fc_max = 24.250e9
urad_bw_max = urad_fc_max - urad_fc_min


# ****************************** Application ****************************** #


DEFAULT_PADDING = 6
DEFAULT_CARD_WIDTH = 96
DEFAULT_CARD_HEIGHT = 96
GRAPH_UNIT_SIZE = 18 
LABEL_COL_WIDTH = 96

FONT_HEADING = ('Helvetica', 12,  'bold')
FONT_DESCRIPTION = ('Helvetica', 8)

waveform_types = {
    "ContinuousWave": "CW",
    "Sawtooth": "Up",
    "Triangle": "Triangle",
    "DualRate": "DualRate",
}

class OperationModes(enum.IntEnum):
    URAD = 1
    Extended = 2

class ClutterModes(enum.IntEnum):
    Environment = 1
    Wall = 2