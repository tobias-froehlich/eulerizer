import numpy as np
from MidiConnection import MidiConnection
import Calculator
from Eulerizer import Eulerizer
import time
import threading
from const import updateConst

const = {} # never dereference!

updateConst(const, "standard")


sleepDuration = const["STANDBY_SLEEP_DURATION_IN_SECONDS"]
standbyCounter = 0
eulerizers = []
flag = [1]
factorTwo = const["FACTOR_TWO"]
factorThree = const["FACTOR_THREE"]
factorFive = const["FACTOR_FIVE"]
factorSeven = const["FACTOR_SEVEN"]
def userInputTask(flag, eulerizers, factorTwo, factorThree, factorFive):
    while flag[0]:
        userInput = input()
        if userInput != None:
            words = userInput.split()
        else:
            words = ["none"]

        if userInput == "quit":
            flag[0] = 0
        elif userInput == "off":
            for i in range(len(const["PARAMS"])):
                (eulis, bendings) = Calculator.Calculator()(const, const["PARAMS"][i]["BENDING"], True, factorTwo, factorThree, factorFive, factorSeven)
                eulerizers[i].setBendings(bendings)
        elif userInput == "on":
            for i in range(len(const["PARAMS"])):
                (eulis, bendings) = Calculator.Calculator()(const, const["PARAMS"][i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                eulerizers[i].setBendings(bendings)
        elif words[0] == "print":
            print("print=%s"%(" ".join(words[1:])))
        elif words[0] == "set":
            if words[1] == "FACTOR_TWO":
                for i in range(len(const["PARAMS"])):
                    factorTwo = float(words[2])
                    (eulis, bendings) = Calculator.Calculator()(const, const["PARAMS"][i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                    eulerizers[i].setBendings(bendings)
            elif words[1] == "FACTOR_THREE":
                for i in range(len(const["PARAMS"])):
                    factorThree = float(words[2])
                    (eulis, bendings) = Calculator.Calculator()(const, const["PARAMS"][i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                    eulerizers[i].setBendings(bendings)
            elif words[1] == "FACTOR_FIVE":
                for i in range(len(const["PARAMS"])):
                    factorFive = float(words[2])
                    (eulis, bendings) = Calculator.Calculator()(const, const["PARAMS"][i]["BENDING"], False, factorTwo, factorThree, factorFive, factorSeven)
                    eulerizers[i].setBendings(bendings)
        elif words[0] == "config":
            updateConst(const, words[1])
            eulerizers.clear()
            for param in const["PARAMS"]:
                (eulis, bendings) = Calculator.Calculator()(
                    const,
                    param["BENDING"],
                    const["NO_BENDING"],
                    const["FACTOR_TWO"],
                    const["FACTOR_THREE"],
                    const["FACTOR_FIVE"],
                    const["FACTOR_SEVEN"]
                )
                eulerizers.append(Eulerizer(midi_connection, eulis, bendings, param, const["EULER_NET"], const["NO_BENDING"], const["CONSOLE_IO"], const["OCTAVES_SHARE_CHANNEL"]))
            print("print=%s"%(const))
            print("config=%s"%(words[1]))

if const["CONSOLE_IO"]:
    userInputThread = threading.Thread(target=userInputTask, args=(flag, eulerizers, factorTwo, factorThree, factorFive))
    userInputThread.start()

midi_connection = MidiConnection()
for param in const["PARAMS"]:
    (eulis, bendings) = Calculator.Calculator()(
        const,
        param["BENDING"],
        const["NO_BENDING"],
        const["FACTOR_TWO"],
        const["FACTOR_THREE"],
        const["FACTOR_FIVE"],
        const["FACTOR_SEVEN"]
    )
    eulerizers.append(Eulerizer(midi_connection, eulis, bendings, param, const["EULER_NET"], const["NO_BENDING"], const["CONSOLE_IO"], const["OCTAVES_SHARE_CHANNEL"]))
while flag[0]:
    message = midi_connection.get_message()
    if "RUN" in const.keys():
        if message:
            if message.type == "stop":
                midi_connection.send_stop_signal();
                for eulerizer in eulerizers:
                    eulerizer.reset()
            if message.type == "note_on" or \
               message.type == "note_off" or \
               message.type == "control_change":
                 if message.channel != const["CTRL_CHANNEL"] - 1:
                     for eulerizer in eulerizers:
                         eulerizer.loop(message)
                 else:
                     if message.type == "note_on":
                         region = message.note - 56
                         if 0 <= region < 8:
                             for eulerizer in eulerizers:
                                 eulerizer.setRegion(region)
                             if const["CONSOLE_IO"]:
                                 print("region=%i"%(region), flush=True)
            standbyCounter = 0
            sleepDuration = const["ACTIVE_SLEEP_DURATION_IN_SECONDS"]
        else:
            standbyCounter += 1
        if standbyCounter > const["NUMBER_OF_LOOPS_UNTIL_STANDBY"]:
            sleepDuration = const["STANDBY_SLEEP_DURATION_IN_SECONDS"]
        time.sleep(sleepDuration)

if const["CONSOLE_IO"]:
    print("quit", flush=True)
    userInputThread.join() 
