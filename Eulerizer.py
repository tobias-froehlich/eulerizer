import numpy as np
import serial
from MidiConnection import MidiConnection
import Calculator
import time
from const import *


class Eulerizer:

    def __init__(self, midi_connection, eulis,
        bendings, param):
        (self.__eulis, self.__bendings) = \
            (eulis, bendings)
        self.__in_channel = param["IN_CHANNEL"]
        self.__channels = param["CHANNELS"]
        self.__bending = param["BENDING"]
        self.__midi_connection = midi_connection
        self.__region = 4
        self.reset()

    def reset(self):
        self.__pedal_pressed = False
        self.__pressed = np.zeros(
            (len(self.__channels), 128),
            dtype="int32"
        )
        self.__sounding = np.zeros(
            (len(self.__channels), 128),
            dtype="int32"
        )
        self.__priority = np.zeros(
            len(self.__channels),
            dtype="int32"
        ) + 100
        self.__euli = [None]*len(self.__channels)

<<<<<<< HEAD
    def loop(self):
        message = \
            self.__midi_connection.get_message()
        if message:
            typ = message.type
            if typ == "note_on":
                if message.velocity == 0:
                    typ = "note_off"
            if typ == "control_change":
                if message.control == 66:
                    if message.value > 50:
                        self.__pedal_pressed = True
                    else:
                        self.__pedal_pressed = False
            if typ == "note_on":
                midi = message.note
                velocity = message.velocity
                euli = self.__eulis \
                    [self.__region][midi]
                bending = self.__bendings \
                    [self.__region][midi]
                if euli in self.__euli and OCTAVES_SHARE_CHANNEL:
                    j = self.__euli.index(euli)
                    self.__midi_connection \
                        .start_note(
                            midi,
                            velocity,
                            bending,
                            CHANNELS[j]
                        )
                    self.__pressed[j, midi] = 1
                    self.__sounding[j, midi] = 1
                else:
                    j = self.__priority.argmax()
                    self.__euli[j] = euli
                    self.__midi_connection \
                        .start_note(
                            midi,
                            velocity,
                            bending,
                            CHANNELS[j]
                        )
                    self.__priority[j] = 0
                    self.__pressed[j, midi] = 1
                    self.__sounding[j, midi] = 1
                    print(
                        "note_on=%i,%i"%euli,
                        flush=True
                    )
            elif typ == "note_off":
                midi = message.note
                self.__pressed[:, midi] = 0

            if not self.__pedal_pressed:
                sounding_but_not_pressed = \
                    self.__sounding - self.__pressed
                jis = np.argwhere(
                    sounding_but_not_pressed
                )
                for ji in jis:
                    j = ji[0]
                    i = ji[1]
                    self.__sounding[j, i] = 0
                    self.__midi_connection \
                        .stop_note(
                            i,
                            CHANNELS[j]
                        )
                    euli = self.__euli[j]
                    if self.__sounding[j].sum() == 0:
                        self.__priority[j] = 10
                        self.__euli[j] = None
=======
    def loop(self, message):
        typ = message.type
        if typ in ["note_on", "note_off", "control_change"]:
            if message.channel == self.__in_channel:                
                if typ == "note_on":
                    if message.velocity == 0:
                        typ = "note_off"
                if typ == "control_change":
                    if message.control == 64:
                        if message.value > 50:
                            self.__pedal_pressed = True
                        else:
                            self.__pedal_pressed = False
                if typ == "note_on":
                    midi = message.note
                    velocity = message.velocity
                    euli = self.__eulis \
                        [self.__region][midi]
                    bending = self.__bendings \
                        [self.__region][midi]
                    if euli in self.__euli:
                        j = self.__euli.index(euli)
                        self.__midi_connection \
                            .start_note(
                                midi,
                                velocity,
                                bending,
                                self.__channels[j]
                            )
                        self.__pressed[j, midi] = 1
                        self.__sounding[j, midi] = 1
                    else:
    #                    print(self.__priority)
                        j = self.__priority.argmax()
                        self.__euli[j] = euli
                        self.__midi_connection \
                            .start_note(
                                midi,
                                velocity,
                                bending,
                                self.__channels[j]
                            )
                        self.__priority[j] = 0
                        self.__pressed[j, midi] = 1
                        self.__sounding[j, midi] = 1
    #                print(self.__priority)
>>>>>>> oldversion
                        print(
                            "note_on=%i,%i"%euli,
                            flush=True
                        )
                elif typ == "note_off":
                    midi = message.note
                    self.__pressed[:, midi] = 0
    
                if not self.__pedal_pressed:
                    sounding_but_not_pressed = \
                        self.__sounding - self.__pressed
                    jis = np.argwhere(
                        sounding_but_not_pressed
                    )
                    for ji in jis:
                        j = ji[0]
                        i = ji[1]
                        self.__sounding[j, i] = 0
                        self.__midi_connection \
                            .stop_note(
                                i,
                                self.__channels[j]
                            )
                        euli = self.__euli[j]
                        if self.__sounding[j].sum() == 0:
                            self.__priority[j] = 10
                            self.__euli[j] = None
                            print(
                                "note_off=%i,%i"%euli,
                                flush=True
                            )
                    self.__priority += (self.__priority >= 10)
                       
        time.sleep(0.001)
                
    def setRegion(self, region):
        self.__region = region

        

if __name__ == "__main__":
    midi_connection = MidiConnection()
    eulerizers = []
    for param in PARAMS:
        (eulis, bendings) = Calculator.Calculator()(param["BENDING"])
        eulerizers.append(Eulerizer(midi_connection, eulis, bendings, param))
    while True:
        message = midi_connection.get_message()
        if message:
            if message.type == "stop":
                midi_connection.send_stop_signal();
                for eulerizer in eulerizers:
                    eulerizer.reset()
                print("reset=true", flush=True)
            if message.type == "note_on":
                if message.channel == CTRL_CHANNEL:
                    region = message.note - 56
                    for eulerizer in eulerizers:
                        eulerizer.setRegion(region)
                    print("region=%i"%(region), flush=True)
            if message.type == "note_on" or \
               message.type == "note_off":
                 if message.channel != CTRL_CHANNEL:
                     for eulerizer in eulerizers:
                         eulerizer.loop(message)
            time.sleep(0.001)
