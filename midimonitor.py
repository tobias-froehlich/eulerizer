import mido

port_in = mido.open_input(
    name="monitor",
    client_name="monitor",
    virtual=True
)

while True:
    message = port_in.poll()
    if message:
        print(message)
