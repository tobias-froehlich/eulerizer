import numpy as np
import serial
import mido
import time
import Calculator
import const

#arduino = serial.Serial(
#    "/dev/ttyUSB0",
#    9600
#)


class Saite:

    def __init__(self, port_out, channel):
        self.__port_out = port_out
        self.__channel = channel
        self.__euli = (0, 0)
        self.__midi = 0
        self.__bending = 0.
        self.__pressed = False
        self.__playing = False

    def is_playing(self):
        return self.__playing

    def start_note(self, euli, midi, bending):
        self.__euli = euli
        self.__midi = midi
        self.__bending = bending
        self.__pressed = True
        self.__playing = True
        self.__port_out.send(
            mido.Message(
                "pitchwheel",
                channel=self.__channel,
                pitch=round(bending * 8191)
            )
        )
        self.__port_out.send(
            mido.Message(
                "note_on",
                channel=self.__channel,
                note=self.__midi
            )
        )
#        print("starting note on channel", self.__channel)
        print("note_on=%i,%i"%(self.__euli[0], self.__euli[1]), flush=True)

    def release_key(self, midi):
        if midi == self.__midi:
            if self.__pressed:
                self.__pressed = False
                return True
        return False

    def release_pedal(self):
        if not self.__pressed:
            if self.__playing:
                self.__playing = False
                self.__port_out.send(
                    mido.Message(
                        "note_off",
                        channel=self.__channel,
                        note=self.__midi
                    )
                )
                print("note_off=%i,%i"%(self.__euli[0], self.__euli[1]), flush=True)
#                print("stopping note on channel", self.__channel)

class Eulerizer:

    def __init__(self):
        (self.__eulis, self.__bendings) \
            = Calculator.Calculator()()
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
        for channel in const.CHANNELS:
            self.__saiten.append(
                Saite(self.__port_out, channel)
            )
            self.__priorities.append(100)

#        print("inizialized")

    def loop(self):
        message = self.__port_in.poll()
        if message:
            typ = message.type
            if typ == "note_on":
                midi = message.note
                index = self.__priorities.index(
                    max(self.__priorities)
                )
                saite = self.__saiten[index]
                if not saite.is_playing():
                    saite.start_note(
                        self.__eulis
                            [self.__region]
                            [midi],
                        midi,
                        self.__bendings
                            [self.__region]
                            [midi] 
                    )
                    self.__priorities[index] = 0
#                    for i in range(len(const.CHANNELS)):
#                        if not self.__saiten[i].is_playing():
#                            self.__priorities[i] += 1
#                print(self.__priorities)
            elif typ == "note_off":
                midi = message.note
                for i in range(len(const.CHANNELS)):
                    if self.__saiten[i].release_key(midi):
                        self.__priorities[i] = 0
                for i in range(len(const.CHANNELS)):
                    if not self.__saiten[i].is_playing():
                        self.__priorities[i] += 1
#                print(self.__priorities)

            if not self.__pedal_pressed:
                for saite in self.__saiten:
                    saite.release_pedal()
                        
                
                
#        if (arduino.inWaiting() > 0):
#            arduino_value = arduino.read()
#            if (arduino_value == b'3'):
#                print("region=3", flush=True)
#            if (arduino_value == b'4'):
#                print("region=4", flush=True)
#            if (arduino_value == b'5'):
#                print("region=5", flush=True)
        time.sleep(0.01)
        

        

if __name__ == "__main__":
    eulerizer = Eulerizer()
    while True:
        eulerizer.loop()
        time.sleep(0.001)
