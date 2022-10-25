import numpy as np
from MidiConnection import MidiConnection
import Calculator
from Eulerizer import Eulerizer
import time
import threading
from const import *
        

sleepDuration = STANDBY_SLEEP_DURATION_IN_SECONDS
numberOfLoopsUntilStandby = STANDBY_AFTER_SECONDS // ACTIVE_SLEEP_DURATION_IN_SECONDS + 1
standbyCounter = 0
eulerizers = []
flag = [1]
factorTwo = FACTOR_TWO
factorThree = FACTOR_THREE
factorFive = FACTOR_FIVE
factorSeven = FACTOR_SEVEN
def userInputTask(flag, eulerizers, factorTwo, factorThree, factorFive):
    while flag[0]:
        userInput = input()
        words = userInput.split()
        if userInput == "quit":
            flag[0] = 0
        elif userInput == "off":
            for i in range(len(PARAMS)):
                (eulis, bendings) = Calculator.Calculator()(PARAMS[i]["BENDING"], True, factorTwo, factorThree, factorFive, factorSeven)
                eulerizers[i].setBendings(bendings)
        elif userInput == "on":
            for i in range(len(PARAMS)):
                (eulis, bendings) = Calculator.Calculator()(PARAMS[i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                eulerizers[i].setBendings(bendings)
        elif words[0] == "set":
            if words[1] == "FACTOR_TWO":
                for i in range(len(PARAMS)):
                    factorTwo = float(words[2])
                    (eulis, bendings) = Calculator.Calculator()(PARAMS[i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                    eulerizers[i].setBendings(bendings)
            elif words[1] == "FACTOR_THREE":
                for i in range(len(PARAMS)):
                    factorThree = float(words[2])
                    (eulis, bendings) = Calculator.Calculator()(PARAMS[i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                    eulerizers[i].setBendings(bendings)
            elif words[1] == "FACTOR_FIVE":
                for i in range(len(PARAMS)):
                    factorFive = float(words[2])
                    (eulis, bendings) = Calculator.Calculator()(PARAMS[i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                    eulerizers[i].setBendings(bendings)

if CONSOLE_IO:
    userInputThread = threading.Thread(target=userInputTask, args=(flag, eulerizers, factorTwo, factorThree, factorFive))
    userInputThread.start()

midi_connection = MidiConnection()
for param in PARAMS:
    (eulis, bendings) = Calculator.Calculator()(param["BENDING"], NO_BENDING, FACTOR_TWO, FACTOR_THREE, FACTOR_FIVE, FACTOR_SEVEN)
    eulerizers.append(Eulerizer(midi_connection, eulis, bendings, param))
while flag[0]:
    message = midi_connection.get_message()
    if message:
        if message.type == "stop":
            midi_connection.send_stop_signal();
            for eulerizer in eulerizers:
                eulerizer.reset()
        if message.type == "note_on" or \
           message.type == "note_off" or \
           message.type == "control_change":
             if message.channel != CTRL_CHANNEL - 1:
                 for eulerizer in eulerizers:
                     eulerizer.loop(message)
             else:
                 if message.type == "note_on":
                     region = message.note - 56
                     if 0 <= region < 8:
                         for eulerizer in eulerizers:
                             eulerizer.setRegion(region)
                         if CONSOLE_IO:
                             print("region=%i"%(region), flush=True)
        standbyCounter = 0
        sleepDuration = ACTIVE_SLEEP_DURATION_IN_SECONDS
    else:
        standbyCounter += 1
    if standbyCounter > numberOfLoopsUntilStandby:
        sleepDuration = STANDBY_SLEEP_DURATION_IN_SECONDS
    time.sleep(sleepDuration)

if CONSOLE_IO:
    print("quit", flush=True)
    userInputThread.join() 
