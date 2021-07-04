import numpy as np
import serial
import mido
import time
import Calculator
import const

arduino = serial.Serial(
    "/dev/ttyUSB0",
    9600
)


class Saite:

    def __init__(self, port_out, euli, bending):
        self.__port_out = port_out
        self.__euli = euli
        self.__bending = bending

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


    def loop(self):
        midis = self.__port_in.poll()
        if midis:
            print(midis)
        if (arduino.inWaiting() > 0):
            arduino_value = arduino.read()
            if (arduino_value == b'3'):
                print("region=3", flush=True)
            if (arduino_value == b'4'):
                print("region=4", flush=True)
            if (arduino_value == b'5'):
                print("region=5", flush=True)
        time.sleep(0.01)
        

        

if __name__ == "__main__":
    eulerizer = Eulerizer()
    while True:
        eulerizer.loop()
        time.sleep(0.001)
