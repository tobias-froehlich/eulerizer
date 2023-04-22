import serial
import time
import threading
import mido
import sys
import os
from const import updateConst


const = {} # never dereference!

updateConst(const, "standard")

configDirectory = sys.argv[1]

def getConfigs():
    filenames = os.listdir(configDirectory)
    filenames.sort()
    configs = []
    index = 1
    for filename in filenames:
        if filename.endswith(".py"):
            configs.append({
                "index": index,
                "filename": filename[:-3],
            })
            index += 1
    return configs

arduino = None
try:
    arduino = serial.Serial(
        "/dev/ttyUSB0",
        9600
    )
except:
    print("Use without pedals.")

flag = [1,]

midiInputPort = mido.open_input(
    name="pedals",
    client_name="pedals",
    virtual=True
)

midiOutputPort = mido.open_output(
    name="pedals",
    client_name="pedals",
    virtual=True
)

table = {
    b'0': 56,
    b'1': 57,
    b'2': 58,
    b'3': 59,
    b'4': 60,
    b'5': 61,
    b'6': 62,
    b'7': 63,
}

def userInputTask(flag, const):
    while (flag[0]):
        configs = getConfigs()
#        print("print \033c")
        print("print")
        for c in configs:
            print("print %2i: %s"%(c["index"], c["filename"]))
        print("print")
        print("print *** %s ***"%(const["CONFIG_FILENAME"]))
        print("print")
        userInput = input("print=Enter \"quit\" or the number of a configuration.:\n")
        print(userInput)
        if userInput == "quit":
            flag[0] = 0
        else:
            try:
                number = int(userInput)
                if not 1 <= number <= len(configs):
                    print("print The input must be between 1 and %i"%(len(configs)))
                else:
                    for c in configs:
                        if c["index"] == number:
                            updateConst(const, c["filename"])
                            print("config %s"%(c["filename"]))
            except:
                print("print Invalid input.")

def listeningTask(flag, const):
    sleepDuration = const["STANDBY_SLEEP_DURATION_IN_SECONDS"]
    standbyCounter = 0
    signalNotes = []
    while (flag[0]):
        if "RUN" in const.keys():
            somethingHappened = False
            now = time.time()
            if (len(signalNotes) > 0):
                if now > signalNotes[0]["time"] + 1.0:
                    midiOutputPort.send(
                        mido.Message(
                            "note_off",
                            channel=const["CTRL_CHANNEL"] - 1,
                            note=signalNotes[0]["note"],
                            velocity=0,
                        )
                    )
                    del signalNotes[0]
            if (arduino.inWaiting() > 0):
                somethingHappened = True
                arduinoValue = arduino.read();
                if arduinoValue not in [b'\r', b'\n']:
                    midicode = table[arduinoValue]
                    midiOutputPort.send(
                        mido.Message(
                            "note_on",
                            channel=const["CTRL_CHANNEL"] - 1,
                            note=midicode,
                            velocity=100,
                        )
                    )
                    signalNotes.append({"note": midicode, "time": time.time()})
            message = midiInputPort.poll()
            if message:
                somethingHappened = True
                if message.channel != const["CTRL_CHANNEL"] - 1:
                    midiOutputPort.send(message)
            if somethingHappened:
                standbyCounter = 0
                sleepDuration = const["ACTIVE_SLEEP_DURATION_IN_SECONDS"]
            else:
                standbyCounter += 1
            if standbyCounter > const["NUMBER_OF_LOOPS_UNTIL_STANDBY"]:
                sleepDuration = const["STANDBY_SLEEP_DURATION_IN_SECONDS"]
            time.sleep(sleepDuration)   

if const["CONSOLE_IO"]:
    inputThread = threading.Thread(target=userInputTask, args=(flag, const))
if arduino:
    listeningThread = threading.Thread(target=listeningTask, args=(flag, const))
if const["CONSOLE_IO"]:
    inputThread.start()
if arduino:
    listeningThread.start()
if const["CONSOLE_IO"]:
    inputThread.join()
if arduino:
    listeningThread.join()

midiInputPort.close()
midiOutputPort.close()
