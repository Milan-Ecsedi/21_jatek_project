from random import shuffle
import Kartya

class Pakli:
    def __init__(self):
        self.kartyak = [Kartya.Kartya(ertek, szin) for ertek in range(1, 8) for szin in range(4)]
        shuffle(self.kartyak)

    def huz(self):
        return self.kartyak.pop() if self.kartyak else None
