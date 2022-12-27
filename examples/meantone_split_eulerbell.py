ACTIVE_SLEEP_DURATION_IN_SECONDS = 0.001
STANDBY_SLEEP_DURATION_IN_SECONDS = 0.5
STANDBY_AFTER_SECONDS = 20

EULER_NET = "MEANTONE"

INIT_POS = (6, 2, 0)

INIT_NAME = "a"
INIT_FREQ = 440.0
INIT_MIDI = 57

exponent = 0.96875
FACTOR_TWO = 2.00**exponent
FACTOR_THREE = 3.00**exponent
FACTOR_FIVE = 5.00**exponent
FACTOR_SEVEN = 7.00**exponent


OCTAVES_SHARE_CHANNEL = False

CTRL_CHANNEL = 10

PARAMS = [
    {   
        "IN_CHANNEL": 1,
        "CHANNELS": [1, 2, 3, 4, 5, 6, 7, 8],
        "BENDING": 2,
        "LEGATO": False,
        "MIDI_RANGE": [0, 62],
        "TRANSPOSE": 0,
    },
    {   
        "IN_CHANNEL": 1,
        "CHANNELS": [9, 11, 12, 13, 14, 15, 16],
        "BENDING": 2,
        "LEGATO": False,
        "MIDI_RANGE": [63, 127],
        "TRANSPOSE": -12 ,
    },
]


