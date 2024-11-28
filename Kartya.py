import os

SZINEK = ["Piros", "Tök", "Zöld", "Makk"]
ERTEKEK = [None, None, None, None, None, None, None, "7", "8", "9", "10", "Alsó", "Felső", "Király", "Ász"]

class Kartya:
    def __init__(self, ertek, szin):
        self.ertek = ertek
        self.szin = szin
        self.kep_ut = f"kartyakepek/{SZINEK[szin]}_{ERTEKEK[ertek]}.png"
        if not os.path.exists(self.kep_ut):  # Ellenőrizzük, hogy létezik-e a kép
            self.kep_ut = "kartyakepek/blank.png"  # Ha nem tudna valami okból megtaalálni a képet

    def __str__(self):
        return f"{ERTEKEK[self.ertek]} {SZINEK[self.szin]}"

    def ertekeles(self):
        if self.ertek == 14:  # Ász
            return 11
        elif self.ertek == 13:  # Király
            return 4
        elif self.ertek == 12:  # Felső
            return 3
        elif self.ertek == 11:  # Alsó
            return 2
        elif 7 <= self.ertek <= 10:  # 7, 8, 9, 10 értéke azonos a számukkal
            return self.ertek
        return 0
