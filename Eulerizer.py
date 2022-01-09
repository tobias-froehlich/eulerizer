import numpy as np
import serial
from MidiConnection import MidiConnection
import Calculator
import time
from const import *

arduino = serial.Serial(
    "/dev/ttyUSB0",
    9600
)


class Eulerizer:

    def __init__(self):
        (self.__eulis, self.__bendings) = \
            Calculator.Calculator()()
        self.__midi_connection = MidiConnection()
        self.__region = 4
        self.__pedal_pressed = False
        self.__pressed = np.zeros(
            (len(CHANNELS), 128),
            dtype="int32"
        )
        self.__sounding = np.zeros(
            (len(CHANNELS), 128),
            dtype="int32"
        )
        self.__priority = np.zeros(
            len(CHANNELS),
            dtype="int32"
        ) + 100
        self.__euli = [None]*len(CHANNELS)

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
                        print(
                            "note_off=%i,%i"%euli,
                            flush=True
                        )
                self.__priority += (self.__priority >= 10)
                       
                
                
        if (arduino.inWaiting() > 0):
            arduino_value = arduino.read()
            if (arduino_value == b'0'):
                print("region=0", flush=True)
                self.__region = 0
            if (arduino_value == b'1'):
                print("region=1", flush=True)
                self.__region = 1
            if (arduino_value == b'2'):
                print("region=2", flush=True)
                self.__region = 2
            if (arduino_value == b'3'):
                print("region=3", flush=True)
                self.__region = 3
            if (arduino_value == b'4'):
                print("region=4", flush=True)
                self.__region = 4
            if (arduino_value == b'5'):
                print("region=5", flush=True)
                self.__region = 5
            if (arduino_value == b'6'):
                print("region=6", flush=True)
                self.__region = 6
            if (arduino_value == b'7'):
                print("region=7", flush=True)
                self.__region = 7
        time.sleep(0.01)
        

        

if __name__ == "__main__":
    eulerizer = Eulerizer()
    while True:
        eulerizer.loop()
        time.sleep(0.001)
