import numpy as np
from MidiConnection import MidiConnection
import Calculator
import time
import threading



class Eulerizer:

    def __init__(self, midi_connection, eulis,
        bendings, param, eulerNet, noBending, consoleIo, octavesShareChannel):
        (self.__eulis, self.__bendings) = \
            (eulis, bendings)

        if eulerNet in ["STANDARD", "MEANTONE"]:
            self.__note_on_format_str = "note_on=%i,%i"
            self.__note_off_format_str = "note_off=%i,%i"
        elif eulerNet == "STANDARD7":
            self.__note_on_format_str = "note_on=%i,%i,%i"
            self.__note_off_format_str = "note_off=%i,%i,%i"

        self.__noBending = noBending
        self.__consoleIo = consoleIo
        self.__octavesShareChannel = octavesShareChannel
        self.__in_channel = param["IN_CHANNEL"] - 1
        self.__channels = [c - 1 for c in param["CHANNELS"]]
        self.__bending = param["BENDING"]
        self.__legato = param["LEGATO"]
        if "MIDI_RANGE" in param.keys():
            self.__midiRange = param["MIDI_RANGE"]
        else:
            self.__midiRange = [0, 127]
        if "TRANSPOSE" in param.keys():
            self.__transpose = param["TRANSPOSE"]
        else:
            self.__transpose = 0
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
        ) + 1000
        self.__euli = [None]*len(self.__channels)


    def setBendings(self, bending):
        self.__bendings = bending

    def loop(self, message):
        typ = message.type
        if typ in ["note_on", "note_off", "control_change"]:
            if message.channel == self.__in_channel:                
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
                    if (self.__midiRange[0] <= midi <= self.__midiRange[1]):
                        midi += self.__transpose
                        velocity = message.velocity
                        euli = self.__eulis \
                            [self.__region][midi]
                        bending = self.__bendings \
                            [self.__region][midi]
                        if euli in self.__euli and self.__octavesShareChannel:
                            j = self.__euli.index(euli)
                            self.__midi_connection \
                                .start_note(
                                    midi,
                                    velocity,
                                    bending,
                                    self.__channels[j]
                                )
                            self.__pressed[j, midi] = 1
                            self.__sounding[j, midi] += 1
                        elif self.__legato and self.__sounding.sum() > 0:
                            velocity = message.velocity
                            euli = self.__eulis \
                                [self.__region][midi]
                            j = np.where(self.__sounding == 1)[0][0]
                            self.__midi_connection \
                                .start_note(
                                    midi,
                                    velocity,
                                    bending,
                                    self.__channels[j]
                                )
                            self.__pressed[j, midi] = 1
                            self.__sounding[j, midi] += 1
                        else:
                            j = self.__priority.argmax()
                            if self.__priority[j] < 100:
                                print("print=%s"%("Caution! Notes have to be stopped because you do not have enough channels!"))
                                soundingMidis = np.argwhere(self.__sounding[j] > 0)
                                for m in soundingMidis[:, 0]:
                                    for n in range(self.__sounding[j, m]):
                                        self.__midi_connection \
                                            .stop_note(
                                                m,
                                                self.__channels[j]
                                            )
                                    self.__sounding[j, m] = 0
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
                            self.__sounding[j, midi] += 1
                            if self.__consoleIo:
                                print(
                                    self.__note_on_format_str%euli,
                                    flush=True
                                )
                elif typ == "note_off":
                    midi = message.note
                    if (self.__midiRange[0] <= midi <= self.__midiRange[1]):
                        midi += self.__transpose
                        self.__pressed[:, midi] = 0
    
                if not self.__pedal_pressed:
                    sounding_but_not_pressed = \
                        np.logical_and(self.__sounding > 0, self.__pressed == 0)
                    jis = np.argwhere(
                        sounding_but_not_pressed
                    )
                    for ji in jis:
                        j = ji[0]
                        i = ji[1]
                        for n in range(self.__sounding[j, i]):
                            self.__midi_connection \
                                .stop_note(
                                    i,
                                    self.__channels[j]
                                )
                        self.__sounding[j, i] = 0
                        euli = self.__euli[j]
                        if self.__sounding[j].sum() == 0:
                            self.__priority[j] = 100
                            self.__euli[j] = None
                            if self.__consoleIo:
                                print(
                                    self.__note_off_format_str%euli,
                                    flush=True
                                )
                self.__priority += 1
    def setRegion(self, region):
        self.__region = region

        
