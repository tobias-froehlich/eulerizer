import numpy as np
import const


class Calculator:

    def __call__(self, bending, noBending, factorTwo, factorThree, factorFive, factorSeven):
        if const.USE_SEVEN:
            return self.__calculate_with_7(bending, noBending, factorTwo, factorThree, factorFive, factorSeven)
        else:
            return self.__calculate_without_7(bending, noBending, factorTwo, factorThree, factorFive)

    def __calculate_without_7(self, bending, noBending, factorTwo, factorThree, factorFive):
        self.__midis = []
        self.__freqs = []
        self.__bending = bending
        self.__noBending = noBending
        for j in range(const.EULER_ROWS):
            self.__midis.append([])
            self.__freqs.append([])
            for i in range(const.EULER_PEDALS + 3):
                self.__midis[-1].append(
                    const.INIT_MIDI
                  + (i - const.INIT_POS[0]) * 7
                  + (j - const.INIT_POS[1]) * 4
                )
                self.__freqs[-1].append(
                    const.INIT_FREQ
                  * (factorThree/factorTwo)**(i - const.INIT_POS[0])
                  * (factorFive/factorTwo**2)**(j - const.INIT_POS[1])
                )
        for j in range(const.EULER_ROWS):
            for i in range(const.EULER_PEDALS + 3):
                midi = self.__midis[j][i]
                freq = self.__freqs[j][i]
                oct = midi // 12
                self.__midis[j][i] = midi % 12
                self.__freqs[j][i] = freq / factorTwo**(oct)

        self.__intonations = []
        self.__eulis = []

        assert const.REGION_MODE in ["HORIZONTAL", "MEANTONE"], "The REGION_MODE %s does not exist."%(const.REGION_MODE)
        if const.REGION_MODE == "HORIZONTAL":
            self.__make_intonations_without_7_horizontal(factorTwo, factorThree, factorFive)
        elif const.REGION_MODE == "MEANTONE":
            self.__make_intonations_without_7_meantone(factorTwo, factorThree, factorFive)

        self.__bendings = []
        self.__equal_freqs = []
        for note in range(128):
            self.__equal_freqs.append(
                440.0
              * 2.0**((note - 57)/12)
            )
        for i in range(const.EULER_PEDALS):
            self.__bendings.append([])
            for note in range(128):
                self.__bendings[-1].append(
                    np.log2(
                        self.__intonations[i][note]
                      / self.__equal_freqs[note]
                    )*12 / self.__bending * (self.__noBending == False)
                )


        return (self.__eulis, self.__bendings)

    def __make_intonations_without_7_horizontal(self, factorTwo, factorThree, factorFive):
        for i in range(const.EULER_PEDALS):
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
                  * factorTwo ** (note // 12)
                )
                self.__eulis[-1].append(
                    eulis[midis.index(note%12)]
                )

    def __make_intonations_without_7_meantone(self, factorTwo, factorThree, factorFive):
        for i in range(const.EULER_PEDALS):
            midis = []
            freqs = []
            eulis = []
            for j in range(1, 4):
                for i1 in range(4):
                    if i + i1 > 7:
                        j_corrected = j - 1
                    elif i + i1 < 4:
                        j_corrected = j + 1
                    else:
                        j_corrected = j
                    midis.append(
                        self.__midis[j_corrected][i+i1]
                    )
                    freqs.append(
                        self.__freqs[j_corrected][i+i1]
                    )
                    eulis.append((i+i1, j_corrected))
            self.__intonations.append([])
            self.__eulis.append([])
            for note in range(128):
                self.__intonations[-1].append(
                    freqs[midis.index(note%12)]
                  * factorTwo ** (note // 12)
                )
                self.__eulis[-1].append(
                    eulis[midis.index(note%12)]
                )



 
    def __calculate_with_7(self, bending, noBending, factorTwo, factorThree, factorFive, factorSeven):
        self.__midis = []
        self.__freqs = []
        self.__bending = bending
        self.__noBending = noBending
        for k in range(const.EULER_LAYERS):
            self.__midis.append([])
            self.__freqs.append([])
            for j in range(const.EULER_ROWS):
                self.__midis[-1].append([])
                self.__freqs[-1].append([])
                for i in range(const.EULER_PEDALS + 1):
                    self.__midis[-1][-1].append(
                        const.INIT_MIDI
                      + (i - const.INIT_POS[0]) * 7
                      + (j - const.INIT_POS[1]) * 4
                      + (k - const.INIT_POS[2]) * 10
                    )
                    self.__freqs[-1][-1].append(
                        const.INIT_FREQ
                      * (factorThree/factorTwo)**(i - const.INIT_POS[0])
                      * (factorFive/factorTwo**2)**(j - const.INIT_POS[1])
                      * (factorSeven/factorTwo**2)**(k - const.INIT_POS[2])
                    )
        for k in range(const.EULER_LAYERS):
            for j in range(const.EULER_ROWS):
                for i in range(const.EULER_PEDALS + 1):
                    midi = self.__midis[k][j][i]
                    freq = self.__freqs[k][j][i]
                    oct = midi // 12
                    self.__midis[k][j][i] = midi % 12
                    self.__freqs[k][j][i] = freq / factorTwo**(oct)


        self.__intonations = []
        self.__eulis = []
        for i in range(const.EULER_PEDALS):
            midis = []
            freqs = []
            eulis = []
            for k in range(2):
                for j in range(3):
                    for i1 in range(2):
                        midis.append(
                            self.__midis[k][j][i+i1]
                        )
                        freqs.append(
                            self.__freqs[k][j][i+i1]
                        )
                        eulis.append((i+i1, j, k))
            self.__intonations.append([])
            self.__eulis.append([])
            for note in range(128):
                self.__intonations[-1].append(
                    freqs[midis.index(note%12)]
                  * factorTwo ** (note // 12)
                )
                self.__eulis[-1].append(
                    eulis[midis.index(note%12)]
                )

        self.__bendings = []
        self.__equal_freqs = []
        for note in range(128):
            self.__equal_freqs.append(
                440.0
              * 2.0**((note - 57)/12)
            )
        for i in range(const.EULER_PEDALS):
            self.__bendings.append([])
            for note in range(128):
                self.__bendings[-1].append(
                    np.log2(
                        self.__intonations[i][note]
                      / self.__equal_freqs[note]
                    )*12 / self.__bending * (self.__noBending == False)
                )


        return (self.__eulis, self.__bendings)
        


