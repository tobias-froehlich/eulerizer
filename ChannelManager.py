import const

class ChannelManager:
    def __init__(self):
        self.__channels = []
        self.__eulis = []
        self.__occupations = []
        self.__priorities = []
        for channel in const.CHANNELS:
            self.__channels.append(channel)
            self.__eulis.append(None)
            self.__occupations.append(0)
            self.__priorities.append(100)


    def get_channel(self, euli):
        if euli in self.__eulis:
            index = self.__eulis.index(euli)
        else:
            index = self.__priorities.index(
                max(self.__priorities)
            )
            self.__eulis[index] = euli
        channel = self.__channels[index]
        self.__occupations[index] += 1
        self.__priorities[index] = 0
        return channel

    def free(self, channel):
        index = self.__channels.index(channel)
        self.__occupations[index] -= 1
        if (self.__occupations[index] == 0):
            self.__eulis[index] = None
        for i in range(len(self.__priorities)):
            if self.__occupations[i] == 0:
                self.__priorities[i] += 1

