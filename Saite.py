import numpy as np
import serial
import mido
import time
import const


class Saite:

    def __init__(self, port_out, channel_manager):
        self.__port_out = port_out
        self.__channel_manager = channel_manager
        self.__channel = 0
        self.__euli = (0, 0)
        self.__midi = 0
        self.__bending = 0.
        self.__pressed = False
        self.__playing = False

    def is_playing(self):
        return self.__playing

    def start_note(self, euli, midi, bending, velocity):
        self.__channel = self.__channel_manager \
                .get_channel(euli)
        print("on channel ", self.__channel)
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
                note=self.__midi,
                velocity=velocity
            )
        )
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
                self.__channel_manager.free(
                    self.__channel
                )
                print("note_off=%i,%i"%(self.__euli[0], self.__euli[1]), flush=True)


