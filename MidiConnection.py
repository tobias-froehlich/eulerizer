import numpy as np
import mido
#import Calculator
from const import *

class MidiConnection:
    
    def __init__(self):
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

    def get_message(self):
        return self.__port_in.poll()

    def start_note(self, midi,
            velocity, bending, channel):
        self.__port_out.send(
            mido.Message(
                "pitchwheel",
                channel=channel,
                pitch=round(bending * 8191)
            )
        )
        self.__port_out.send(
            mido.Message(
                "note_on",
                channel=channel,
                note=midi,
                velocity=velocity
            )
        )

    def stop_note(self, midi, channel):
        self.__port_out.send(
            mido.Message(
                "note_off",
                channel=channel,
                note=midi
            )
        )

