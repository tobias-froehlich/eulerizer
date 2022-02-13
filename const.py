EULERNET_DISTANCE = 90
LETTER_SIZE = (80, 80)
EULER_PEDALS = 8
EULER_ROWS = 3
EULER_LAYERS = 2
BACKGROUND_COLOR = "white"
REGION_COLOR = "#bbb"
REGION_BORDER_COLOR = "#444"
REGION_BORDER_WIDTH = 4


USE_SEVEN = False

if USE_SEVEN:
    INIT_POS = (4, 1, 0)
else:
    INIT_POS = (5, 1, 0)

INIT_NAME = "a"
INIT_FREQ = 440.0
INIT_MIDI = 57

FACTOR_TWO = 2.00
FACTOR_THREE = 3.0
FACTOR_FIVE = 5.00
FACTOR_SEVEN = 7.00



NO_BENDING = False

OCTAVES_SHARE_CHANNEL = False

CTRL_CHANNEL = 10
PARAMS = [
    {   
        "IN_CHANNEL": 1,
        "CHANNELS": [2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16],
        "BENDING": 2
    },
]

NOTE_NAMES = [
    "fb", "cb", "gb", "db", "ab", "eb", "bb",
    "f",  "c",  "g",  "d",  "a",  "e",  "b",
    "f#", "c#", "g#", "d#", "a#", "e#", "b#"
]

