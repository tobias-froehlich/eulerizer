import serial
import time
import threading
import mido
from const import *

arduino = serial.Serial(
    "/dev/ttyUSB0",
    9600
)

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



def userInputTask(flag):
    while (flag[0]):
        userInput = input("Enter \"quit\":\n")
        if userInput == "quit":
            flag[0] = 0

def listeningTask(flag):
    sleepDuration = STANDBY_SLEEP_DURATION_IN_SECONDS
    numberOfLoopsUntilStandby = STANDBY_AFTER_SECONDS // ACTIVE_SLEEP_DURATION_IN_SECONDS + 1
    standbyCounter = 0
    signalNotes = []
    while (flag[0]):
        somethingHappened = False
        now = time.time()
        if (len(signalNotes) > 0):
            if now > signalNotes[0]["time"] + 1.0:
                midiOutputPort.send(
                    mido.Message(
                        "note_off",
                        channel=CTRL_CHANNEL - 1,
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
                        channel=CTRL_CHANNEL - 1,
                        note=midicode,
                        velocity=100,
                    )
                )
                signalNotes.append({"note": midicode, "time": time.time()})
        message = midiInputPort.poll()
        if message:
            somethingHappened = True
            if message.channel != CTRL_CHANNEL - 1:
                midiOutputPort.send(message)
        if somethingHappened:
            standbyCounter = 0
            sleepDuration = ACTIVE_SLEEP_DURATION_IN_SECONDS
        else:
            standbyCounter += 1
        if standbyCounter > numberOfLoopsUntilStandby:
            sleepDuration = STANDBY_SLEEP_DURATION_IN_SECONDS
        time.sleep(sleepDuration)   

if CONSOLE_IO:
    inputThread = threading.Thread(target=userInputTask, args=(flag,))
listeningThread = threading.Thread(target=listeningTask, args=(flag,))
if CONSOLE_IO:
    inputThread.start()
listeningThread.start()
if CONSOLE_IO:
    inputThread.join()
listeningThread.join()

midiInputPort.close()
midiOutputPort.close()
