


class Jatekos:
    def __init__(self, nev, egyenleg=1000):
        self.nev = nev
        self.kartyak = []
        self.egyenleg = egyenleg

    def kez_ertek(self):
        osszeg = sum(kartya.ertekeles() for kartya in self.kartyak)
        aszok_szama = sum(1 for kartya in self.kartyak if kartya.ertek == 14)

        # Két ász esetén automatikusan 21
        if aszok_szama == 2 and len(self.kartyak) == 2:
            return 21

        # Ász értékének csökkentése 11-ről 1-re, ha szükséges
        while osszeg > 21 and aszok_szama:
            osszeg -= 10
            aszok_szama -= 1
        return osszeg


    def kartyat_hozzaad(self, kartya):
        self.kartyak.append(kartya)

    def tet(self, osszeg):
        if 0 < osszeg <= self.egyenleg:
            self.egyenleg -= osszeg
            return osszeg
        return 0

    def nyer(self, osszeg):
        self.egyenleg += osszeg
        return osszeg
