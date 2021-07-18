import numpy as np
import serial
import mido
import time
from Calculator import Calculator
from Saite import Saite
from ChannelManager import ChannelManager
import const

#arduino = serial.Serial(
#    "/dev/ttyUSB0",
#    9600
#)


class Eulerizer:

    def __init__(self):
        (self.__eulis, self.__bendings) \
            = Calculator()()
        self.__port_in = mido.open_input(
            name="eulerizer",
            client_name="eulerizer",
            virtual=True
        )
        self.__port_out = mido.open_output(
            name="eulerizer",
            client_name="eulerizer",
            virtual=True
        )
        self.__region = 4
        self.__pedal_pressed = False
        self.__saiten = []
        self.__priorities = []
        self.__channel_manager = ChannelManager()
        for s in range(const.NUMBER_OF_SAITEN):
            self.__saiten.append(
                Saite(
                    self.__port_out,
                    self.__channel_manager
                )
            )
            self.__priorities.append(100)


    def __play_test(self):
        for i in range(len(self.__saiten)):
            saite1 = self.__saiten[i]
            saite2 = self.__saiten[(i+1) % len(self.__saiten)]
            saite1.start_note((0, 0), 57, 0, 100)
            saite2.start_note((0, 0), 57-const.BENDING, 1, 100)
            time.sleep(0.25)
            saite1.release_key(57)
            saite1.release_pedal()
            saite2.release_key(57-const.BENDING)
            saite2.release_pedal()
            time.sleep(0.25)

    def __handle_control_change(self, message):
        if message.control == 64:
           if message.value > 50:
               self.__pedal_pressed = True
           else:
               self.__pedal_pressed = False

    def __handle_note_on(self, message):
        midi = message.note
        if midi == 108:
            self.__play_test()
        index = self.__priorities.index(
            max(self.__priorities)
        )
        saite = self.__saiten[index]
        print(self.__priorities)
        euli = self.__eulis[self.__region][midi]
        bending = self.__bendings[self.__region][midi]
        if not saite.is_playing():
            print("Start saite ", index)
            saite.start_note(
                euli,
                midi,
                bending,
                message.velocity
            )
            self.__priorities[index] = 0

    def __handle_note_off(self, message):
        midi = message.note
        for s in range(const.NUMBER_OF_SAITEN):
            if self.__saiten[s].release_key(midi):
                self.__priorities[s] = 0
        for s in range(const.NUMBER_OF_SAITEN):
            if not self.__saiten[s].is_playing():
                self.__priorities[s] += 1
 
    def loop(self):
        message = self.__port_in.poll()
        if message:
            typ = message.type
            if typ == "note_on":
                if message.velocity == 0:
                    typ = "note_off"
            if typ == "control_change":
                self.__handle_control_change(message)
            if typ == "note_on":
                self.__handle_note_on(message)
            elif typ == "note_off":
                self.__handle_note_off(message)
                
            if not self.__pedal_pressed:
                for saite in self.__saiten:
                    saite.release_pedal()
                                                       
#        if (arduino.inWaiting() > 0):
#            arduino_value = arduino.read()
#            if (arduino_value == b'2'):
#                print("region=2", flush=True)
#                self.__region = 2
#            if (arduino_value == b'3'):
#                print("region=3", flush=True)
#                self.__region = 3
#            if (arduino_value == b'4'):
#                print("region=4", flush=True)
#                self.__region = 4
#            if (arduino_value == b'5'):
#                print("region=5", flush=True)
#                self.__region = 5
#            if (arduino_value == b'6'):
#                print("region=6", flush=True)
#                self.__region = 6
#        time.sleep(0.01)
        

        

if __name__ == "__main__":
    eulerizer = Eulerizer()
    while True:
        eulerizer.loop()
        time.sleep(0.001)
