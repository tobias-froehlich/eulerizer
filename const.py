import sys
import os

assert len(sys.argv) == 2, "You must give one parameter: The path of the config file."
assert not sys.argv[1].endswith(".py"), "Do not give the config file, give just the path. The UI will ask for the config file."
configPath = sys.argv[1]

def updateConst(const, configFilename):

    sys.path.append(configPath)
    config = __import__(configFilename)
    globals().update(config.__dict__)

    const.clear()

    const["CONFIG_FILENAME"] = configFilename
    const["ACTIVE_SLEEP_DURATION_IN_SECONDS"] = ACTIVE_SLEEP_DURATION_IN_SECONDS
    const["STANDBY_SLEEP_DURATION_IN_SECONDS"] = STANDBY_SLEEP_DURATION_IN_SECONDS
    const["STANDBY_AFTER_SECONDS"] = STANDBY_AFTER_SECONDS
    const["EULER_NET"] = EULER_NET
    const["INIT_POS"] = INIT_POS
    const["INIT_NAME"] = INIT_NAME
    const["INIT_FREQ"] = INIT_FREQ
    const["INIT_MIDI"] = INIT_MIDI
    const["FACTOR_TWO"] = FACTOR_TWO
    const["FACTOR_THREE"] = FACTOR_THREE
    const["FACTOR_FIVE"] = FACTOR_FIVE
    const["FACTOR_SEVEN"] = FACTOR_SEVEN
    const["OCTAVES_SHARE_CHANNEL"] = OCTAVES_SHARE_CHANNEL
    const["CTRL_CHANNEL"] = CTRL_CHANNEL
    const["THROUGH_CHANNELS"] = THROUGH_CHANNELS
    const["PARAMS"] = PARAMS

    const["NUMBER_OF_LOOPS_UNTIL_STANDBY"] = const["STANDBY_AFTER_SECONDS"] // const["ACTIVE_SLEEP_DURATION_IN_SECONDS"] + 1

    const["EULERNET_DISTANCE"] = 90
    const["LETTER_SIZE"] = (80, 80)
    
    const["EULER_PEDALS"] = 8
    if const["EULER_NET"] == "STANDARD":
        const["EULER_COLS"] = 11
        const["EULER_ROWS"] = 3
        const["EULER_LAYERS"] = 1
    elif const["EULER_NET"] == "MEANTONE":
        const["EULER_COLS"] = 11
        const["EULER_ROWS"] = 5
        const["EULER_LAYERS"] = 1
    elif const["EULER_NET"] == "STANDARD7":
        const["EULER_COLS"] = 11
        const["EULER_ROWS"] = 3
        const["EULER_LAYERS"] = 2
    
    
    const["BACKGROUND_COLOR"] = "white"
    const["REGION_COLOR"] = "#bbb"
    const["REGION_BORDER_COLOR"] = "#444"
    const["REGION_BORDER_WIDTH"] = 4
    
    const["NO_BENDING"] = False
    
    
    const["NOTE_NAMES"] = [
        "fb", "cb", "gb", "db", "ab", "eb", "bb",
        "f",  "c",  "g",  "d",  "a",  "e",  "b",
        "f#", "c#", "g#", "d#", "a#", "e#", "b#"
    ]

    const["CONSOLE_IO"] = True

    const["RUN"] = True

