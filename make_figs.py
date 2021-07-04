import matplotlib.pyplot as plt
import const

(w, h) = const.LETTER_SIZE
w /= 60
h /= 60
print(w, h)
for state in ["small", "big"]:
    for name in const.NOTE_NAMES + ["o"]:
        fig = plt.figure(figsize=(w, h), dpi=60)
        fig.add_subplot(111)
        plt.axis("off")
        #plt.plot([1, 2, 3], [1, 2, 3])
        printname = name
        if len(name) == 2:
            if name[1] == "b":
                printname = name[0] + "\N{MUSIC FLAT SIGN}"
            if name[1] == "#":
                printname = name[0] + "\N{MUSIC SHARP SIGN}"
        if state == "small":
            size=50
            name += "_small"
        else:
            size=70
            name += "_big"
        plt.text(0, 0, printname, size=size, horizontalalignment="center", verticalalignment="center", color="black", fontfamily="serif", style="italic")
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.savefig("figs/%s.png"%(name), transparent=True)
        plt.close()
