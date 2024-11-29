import os

SZINEK = ["Piros", "Tök", "Zöld", "Makk"]
ERTEKEK = ["7", "8", "9", "10", "Alsó", "Felső", "Király", "Ász"]

class Kartya:
    def __init__(self, ertek, szin):
        self.ertek = ertek
        self.szin = szin
        self.kep_ut = f"kartyakepek/{SZINEK[szin]}_{ERTEKEK[ertek]}.png"
        if not os.path.exists(self.kep_ut):  # Ellenőrizzük, hogy létezik-e a kép
            self.kep_ut = "kartyakepek/blank.png"  # Ha nem tudna valami okból találni képet

    def __str__(self):
        return f"{SZINEK[self.szin]} {ERTEKEK[self.ertek]}"

    def ertekeles(self):
        if self.ertek == 8:  # Ász
            return 11
        elif self.ertek == 7:  # Király
            return 4
        elif self.ertek == 6:  # Felső
            return 3
        elif self.ertek == 5:  # Alsó
            return 2
        elif 1 <= self.ertek <= 4:  # 7, 8, 9, 10 értéke azonos a számukkal
            return self.ertek + 6 #MERT a tömb indexet kapja meg értéknek ezért hozzá kell adnunk 6-ot hogy a kártyák eredeti értéke legyen
        return 0
