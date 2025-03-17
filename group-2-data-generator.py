import random


class DataGenerator:
    def __init__(self, range=(0, 1)):
        self.__miltiplier = range[1] - range[0]
        self.__shift = range[0]

    def __generate(self):
        return random.random()

    @property
    def value(self):
        return self.__generate() * self.__miltiplier + self.__shift
