CONSOLE_IO = True
ACTIVE_SLEEP_DURATION_IN_SECONDS = 0.001
STANDBY_SLEEP_DURATION_IN_SECONDS = 0.5
STANDBY_AFTER_SECONDS = 20

EULERNET_DISTANCE = 90
LETTER_SIZE = (80, 80)
EULER_PEDALS = 8
EULER_ROWS = 5
EULER_LAYERS = 2
BACKGROUND_COLOR = "white"
REGION_COLOR = "#bbb"
REGION_BORDER_COLOR = "#444"
REGION_BORDER_WIDTH = 4


USE_SEVEN = False
REGION_MODE = "MEANTONE"

if USE_SEVEN:
    INIT_POS = (4, 1, 0)
else:
    INIT_POS = (5, 2, 0)

INIT_NAME = "a"
INIT_FREQ = 440.0
INIT_MIDI = 57

FACTOR_TWO = 2.00
FACTOR_THREE = 3.00
#FACTOR_FIVE = 5.0625 # pythogorean
FACTOR_FIVE = 5.00
FACTOR_SEVEN = 7.00



NO_BENDING = False

OCTAVES_SHARE_CHANNEL = True

CTRL_CHANNEL = 10

which_params = "piano"

params_piano = [
    {   
        "IN_CHANNEL": 1,
        "CHANNELS": [2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16],
        "BENDING": 2,
        "LEGATO": False,
    },
]
params_4voices = [
    {   
        "IN_CHANNEL": 1,
        "CHANNELS": [1, 2],
        "BENDING": 2,
        "LEGATO": True,
    },
    {   
        "IN_CHANNEL": 2,
        "CHANNELS": [3, 4],
        "BENDING": 2,
        "LEGATO": True,
    },
    {   
        "IN_CHANNEL": 3,
        "CHANNELS": [5, 6],
        "BENDING": 2,
        "LEGATO": True,
    },
    {   
        "IN_CHANNEL": 4,
        "CHANNELS": [7, 8],
        "BENDING": 2,
        "LEGATO": True,
    },
]


def choose_params(which_params):
    if which_params == "piano":
        return params_piano
    elif which_params == "4voices":
        return params_4voices

PARAMS = choose_params(which_params)

NOTE_NAMES = [
    "fb", "cb", "gb", "db", "ab", "eb", "bb",
    "f",  "c",  "g",  "d",  "a",  "e",  "b",
    "f#", "c#", "g#", "d#", "a#", "e#", "b#"
]

