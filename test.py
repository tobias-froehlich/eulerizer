import time
time.sleep(1)
for i in list(range(8)) + [2]:
    print("region=%i"%(i), flush=True)
    time.sleep(1)
print("note_on=4,0", flush=True)
time.sleep(1)
print("note_on=4,1", flush=True)
time.sleep(1)
print("note_off=4,0", flush=True)
time.sleep(1)
print("note_off=4,1", flush=True)
time.sleep(1)
print("EOF", flush=True)
