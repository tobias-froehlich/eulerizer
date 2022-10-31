from config import *

EULERNET_DISTANCE = 90
LETTER_SIZE = (80, 80)

EULER_PEDALS = 8
if EULER_NET == "STANDARD":
    EULER_COLS = 11
    EULER_ROWS = 3
    EULER_LAYERS = 1
elif EULER_NET == "MEANTONE":
    EULER_COLS = 11
    EULER_ROWS = 5
    EULER_LAYERS = 1
elif EULER_NET == "STANDARD7":
    EULER_COLS = 11
    EULER_ROWS = 3
    EULER_LAYERS = 2


BACKGROUND_COLOR = "white"
REGION_COLOR = "#bbb"
REGION_BORDER_COLOR = "#444"
REGION_BORDER_WIDTH = 4

NO_BENDING = False

CTRL_CHANNEL = 10

NOTE_NAMES = [
    "fb", "cb", "gb", "db", "ab", "eb", "bb",
    "f",  "c",  "g",  "d",  "a",  "e",  "b",
    "f#", "c#", "g#", "d#", "a#", "e#", "b#"
]

