import serial
import time

arduino = serial.Serial(
    "dev/tty1",
    9600
)
