import tkinter as tk
from random import shuffle
import os
from PIL import Image, ImageTk


# Magyar kártya színek és értékek
SZINEK = ["Piros", "Tök", "Zöld", "Makk"]
ERTEKEK = [None, None, None, None, None, None, None, "7", "8", "9", "10", "Alsó", "Felső", "Király", "Ász"]

class Kartya:
    def __init__(self, ertek, szin):
        self.ertek = ertek
        self.szin = szin
        self.kep_ut = f"kartyakepek/{SZINEK[szin]}_{ERTEKEK[ertek]}.png"
        if not os.path.exists(self.kep_ut):  # Ellenőrizzük, hogy létezik-e a kép
            self.kep_ut = "kartyakepek/blank.png"  # Alapértelmezett kép

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

class Pakli:
    def __init__(self):
        self.kartyak = [Kartya(ertek, szin) for ertek in range(7, 15) for szin in range(4)]
        shuffle(self.kartyak)

    def huz(self):
        return self.kartyak.pop() if self.kartyak else None


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

class FeketeJatek:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.configure(bg='#2E2E2E')
        self.pakli = Pakli()
        self.jatekos = Jatekos("Játékos")
        self.oszto = Jatekos("Osztó")
        self.current_tet = 0
        self.canvas = tk.Canvas(root, width=720, height=450, bg="#1F1F1F")
        self.canvas.pack(padx=20, pady=20)

        self.button_style = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#4CAF50',
            'fg': 'white',
            'width': 12,
            'height': 2,
            'relief': 'raised',
            'bd': 0,
            'highlightthickness': 0,
            'activebackground': '#45a049',
            'activeforeground': 'white'
        }

        self.huz_gomb = tk.Button(root, text="Húzni", command=self.jatekos_huz, **self.button_style)
        self.huz_gomb.pack(side=tk.LEFT, padx=20)
        self.huz_gomb.config(state=tk.DISABLED)  # Alapból letiltjuk

        self.megall_gomb = tk.Button(root, text="Megállni", command=self.jatekos_megall, **self.button_style)
        self.megall_gomb.pack(side=tk.LEFT, padx=20)
        self.megall_gomb.config(state=tk.DISABLED)

        self.restart_gomb = tk.Button(root, text="Újraindítás", command=self.restart, **self.button_style)
        self.restart_gomb.pack(side=tk.BOTTOM, pady=20)
        self.restart_gomb.config(state=tk.DISABLED)

        self.tet_keres = tk.Label(root, text="Tét: ", font=('Arial', 12, 'bold'), fg='white', bg='#2E2E2E')
        self.tet_keres.pack(pady=10)

        self.tet_berak = tk.Entry(root, font=('Arial', 12), width=15)
        self.tet_berak.pack(pady=10)

        self.tet_gomb = tk.Button(root, text="Tét felhelyezése", command=self.tet_beallit, **self.button_style) #itt vagyunk
        self.tet_gomb.pack(pady=10)
        self.tet_ossz = tk.Label(root, text="Jelenlegi tét: 0 Ft", font=('Arial', 12, 'bold'), fg='white', bg='#2E2E2E')
        self.tet_ossz.pack(pady=10)

    def kezdeti_osztas(self):
        for _ in range(2):
            self.jatekos.kartyat_hozzaad(self.pakli.huz())
            self.oszto.kartyat_hozzaad(self.pakli.huz())

    def tet_beallit(self):
        try:
            tet = int(self.tet_berak.get())
            if tet <= 0 or tet > self.jatekos.egyenleg:
                raise ValueError("Érvénytelen tét")
            self.current_tet = self.jatekos.tet(tet)
            self.tet_gomb.config(state=tk.DISABLED)  # Tét gomb letiltása a tét megadása után
            self.huz_gomb.config(state=tk.NORMAL)  # Húzás gomb engedélyezése
            self.megall_gomb.config(state=tk.NORMAL)
            self.frissit_ablak()
            # Tét összegének frissítése
            self.tet_ossz.config(text=f"Jelenlegi tét: {self.current_tet} Ft")
        except ValueError as e:
            self.canvas.create_text(350, 350, text="Hiba! Érvénytelen tét.", fill="red", font=("Arial", 18, 'bold'))

    def jatekos_huz(self):
        self.jatekos.kartyat_hozzaad(self.pakli.huz())
        self.frissit_ablak()
        if self.jatekos.kez_ertek() >= 21:
            self.jatek_vege()

    def jatekos_megall(self):
        self.oszto_kore()
        self.jatek_vege()

    def oszto_kore(self):
        while self.oszto.kez_ertek() < 15:
            self.oszto.kartyat_hozzaad(self.pakli.huz())
        self.frissit_ablak()

    def jatek_vege(self):
        self.huz_gomb.config(state=tk.DISABLED)
        self.megall_gomb.config(state=tk.DISABLED)
        self.restart_gomb.config(state=tk.NORMAL)
        self.frissit_ablak()
        eredmeny = self.eredmeny_meghatarozasa()
        self.canvas.create_text(350, 350, text=eredmeny, fill="yellow", font=("Arial", 18, 'bold'))
        
        if self.jatekos.egyenleg <= 0:
            self.canvas.create_text(350, 370, text="Játék vége! Nincs több pénzed.", fill="red", font=("Arial", 18, 'bold'))
            self.restart_gomb.config(state=tk.DISABLED)  # Újraindítás letiltása, ha nincs több egyenleg

    def eredmeny_meghatarozasa(self):
        jatekos_osszeg = self.jatekos.kez_ertek()
        oszto_osszeg = self.oszto.kez_ertek()
        
        if jatekos_osszeg > 21:
            return "Az osztó nyert! (Túllépted a 21-et)"
        elif oszto_osszeg > 21 or jatekos_osszeg > oszto_osszeg:
            self.jatekos.nyer(self.current_tet * 2)
            return "Játékos nyert!"
        elif jatekos_osszeg < oszto_osszeg:
            return "Az osztó nyert!"
        else:
            self.jatekos.nyer(self.current_tet)
            return "Döntetlen!"

    def frissit_ablak(self):

        self.canvas.delete("all")
        self.canvas.create_text(550, 50, text="Osztó", fill="white", font=("Arial", 16, 'bold'), anchor=tk.S)
        self.canvas.create_text(550, 80, text=f"Érték: {self.oszto.kez_ertek() if self.current_tet > 0 else '???'}", fill="white", font=("Arial", 14), anchor=tk.S)

        self.canvas.create_text(100, 50, text="Játékos", fill="white", font=("Arial", 16, 'bold'), anchor=tk.S)
        self.canvas.create_text(100, 80, text=f"Érték: {self.jatekos.kez_ertek() if self.current_tet > 0 else '???'}", fill="white", font=("Arial", 14), anchor=tk.S)

        # További megjelenítési logika, képek stb.



        y_offset = 150
        self.kartyakepek= []
        for kartya in self.jatekos.kartyak:
            original_image = Image.open(kartya.kep_ut)
            resized_image = original_image.resize((50, 75))  # Átméretezés
            kartya_kep = ImageTk.PhotoImage(resized_image)
            self.kartyakepek.append(kartya_kep)
            # Kép és szöveg elhelyezése egymás mellett
            self.canvas.create_image(80, y_offset, image=kartya_kep, anchor=tk.W)
            self.canvas.create_text(150, y_offset, text=str(kartya), fill="white", font=("Arial", 14), anchor=tk.W)
            y_offset += 80  # Sor eltolása

        y_offset = 150
        for kartya in self.oszto.kartyak:
        # Kép betöltése és átméretezése
            original_image = Image.open(kartya.kep_ut)
            resized_image = original_image.resize((50, 75))  # Átméretezés
            kartya_kep = ImageTk.PhotoImage(resized_image)
            self.kartyakepek.append(kartya_kep)

        # Kép és szöveg elhelyezése egymás mellett
            self.canvas.create_image(530, y_offset, image=kartya_kep, anchor=tk.W)
            self.canvas.create_text(600, y_offset, text=str(kartya), fill="white", font=("Arial", 14), anchor=tk.W)
            y_offset += 80  # Sor eltolása

        self.canvas.create_text(350, 400, text=f"Egyenleg: {self.jatekos.egyenleg} Ft", fill="white", font=("Arial", 18, 'bold'))

    def restart(self):
        if self.jatekos.egyenleg > 0:
            self.jatekos.kartyak = []
            self.oszto.kartyak = []
            self.pakli = Pakli()
            self.current_tet = 0
            self.huz_gomb.config(state=tk.NORMAL)
            self.megall_gomb.config(state=tk.NORMAL)
            self.restart_gomb.config(state=tk.DISABLED)
            self.tet_gomb.config(state=tk.NORMAL)  # Tét gomb újra engedélyezése
            self.kezdeti_osztas()
            self.frissit_ablak()
        else:
            self.canvas.create_text(350, 370, text="Játék vége! Nincs több pénzed.", fill="red", font=("Arial", 18, 'bold'))

    def jatek_inditas(self):
        self.kezdeti_osztas()
        self.frissit_ablak()

# Fő ablak
root = tk.Tk()
jatek = FeketeJatek(root)
jatek.jatek_inditas()
root.mainloop()
tk.tk