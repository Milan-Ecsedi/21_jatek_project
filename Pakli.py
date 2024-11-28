from random import shuffle
import Kartya

class Pakli:
    def __init__(self):
        self.kartyak = [Kartya.Kartya(szin, ertek) for szin in range(4) for ertek in range(7, 15)]
        shuffle(self.kartyak)

    def huz(self):
        return self.kartyak.pop() if self.kartyak else None
