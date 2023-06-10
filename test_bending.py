import sys
import time
from MidiConnection import MidiConnection

if len(sys.argv) != 3:
    print("Give two arguments: The channel and the expected bending.")
    sys.exit()

try:
    channel = int(sys.argv[1])
    bending = int(sys.argv[2])
except:
    print("Invalid arguments.")
    sys.exit()

print("Testing channel %i with bending %i."%(channel, bending))

#output = mido.open_output(
#    name="output",
#    client_name="bending test",
#    virtual=True,
#)

midi = MidiConnection()

input("Press enter to start.")

for i in range(2):
    midi.start_note(60, 100, 0, channel)
    time.sleep(0.5)
    midi.stop_note(60, channel)

    midi.start_note(60 + bending, 100, -1, channel)
    time.sleep(0.5)
    midi.stop_note(60 + bending, channel)
