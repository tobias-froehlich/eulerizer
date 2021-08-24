import numpy as np
import const


class Calculator:

    def __call__(self, bending):
        self.__midis = []
        self.__freqs = []
        for j in range(const.EULER_ROWS):
            self.__midis.append([])
            self.__freqs.append([])
            for i in range(const.EULER_COLS):
                self.__midis[-1].append(
                    const.INIT_MIDI
                  + (i - const.INIT_POS[0]) * 7
                  + (j - const.INIT_POS[1]) * 4
                )
                self.__freqs[-1].append(
                    const.INIT_FREQ
                  * (3/2)**(i - const.INIT_POS[0])
                  * (5/4)**(j - const.INIT_POS[1])
                )
        for j in range(const.EULER_ROWS):
            for i in range(const.EULER_COLS):
                midi = self.__midis[j][i]
                freq = self.__freqs[j][i]
                oct = midi // 12
                self.__midis[j][i] = midi % 12
                self.__freqs[j][i] = freq / 2**(oct)

        self.__intonations = []
        self.__eulis = []
        for i in range(const.EULER_COLS - 3):
            midis = []
            freqs = []
            eulis = []
            for j in range(3):
                for i1 in range(4):
                    midis.append(
                        self.__midis[j][i+i1]
                    )
                    freqs.append(
                        self.__freqs[j][i+i1]
                    )
                    eulis.append((i+i1, j))
            self.__intonations.append([])
            self.__eulis.append([])
            for note in range(128):
                self.__intonations[-1].append(
                    freqs[midis.index(note%12)]
                  * 2 ** (note // 12)
                )
                self.__eulis[-1].append(
                    eulis[midis.index(note%12)]
                )

        self.__bendings = []
        self.__equal_freqs = []
        for note in range(128):
            self.__equal_freqs.append(
                440.0
              * 2**((note - 57)/12)
            )
        for i in range(const.EULER_COLS - 3):
            self.__bendings.append([])
            for note in range(128):
                self.__bendings[-1].append(
                    np.log2(
                        self.__intonations[i][note]
                      / self.__equal_freqs[note]
                    )*12 / bending
                )

#        for i in range(len(self.__bendings)):
#            print(self.__eulis[i])
#            print(self.__bendings[i])

        return (self.__eulis, self.__bendings)
 
        


