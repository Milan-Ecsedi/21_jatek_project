import ctypes
import tkinter as tk
from random import shuffle
import os
from PIL import Image, ImageTk #pip install pillow
import pygame #pip install pygame (A játék hangjához)
import Pakli
import Jatekos

# Magyar kártya színek és értékek
SZINEK = ["Piros", "Tök", "Zöld", "Makk"]
ERTEKEK = ["7", "8", "9", "10", "Alsó", "Felső", "Király", "Ász"]

#Kartya class különítve Kartya fileba 

#Pakli class különítve Pakli fileba 

#Jatekos class különítve Jatekos fileba 

class FeketeJatek:
    def __init__(self, root):
        self.root = root
        self.root.title("Huszonegyes")
        #myappid = u'mycompany.myproduct.subproduct.version'
        #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        # KI KELL PRÓBÁLNI, TASKBAR IKON MEGJELENÍTÉSE
        #img = tk.PhotoImage(file='./icon.png')
        #icon = Image.open(img)
        #icon = ImageTk.PhotoImage(icon)
        #root.iconphoto(True, icon)
        #root.iconphoto(False, img)
        #root.iconbitmap(r"./icon.ico")
        self.root.configure(bg='#2E2E2E')
        self.pakli = Pakli.Pakli()
        self.jatekos = Jatekos.Jatekos("Játékos")
        self.oszto = Jatekos.Jatekos("Osztó")
        self.current_tet = 0
        self.canvas = tk.Canvas(root, width=720, height=450, bg="#1F1F1F")
        self.canvas.pack(padx=20, pady=20)
        root.attributes("-fullscreen", True)
        root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
        root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
        

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

        self.canvas.create_text(550, 50, text="Osztó", fill="white", font=("Arial", 16, 'bold'), anchor=tk.S)
        self.canvas.create_text(550, 80, text=f"Érték: {self.oszto.kez_ertek() if self.current_tet > 0 else '???'}", fill="white", font=("Arial", 14), anchor=tk.S)

        self.canvas.create_text(100, 50, text="Játékos", fill="white", font=("Arial", 16, 'bold'), anchor=tk.S)
        self.canvas.create_text(100, 80, text=f"Érték: {self.jatekos.kez_ertek() if self.current_tet > 0 else '???'}", fill="white", font=("Arial", 14), anchor=tk.S)


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



    def huzHang(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./sounds/pickingCard.mp3")
        pygame.mixer.music.play()

    def kartyaMutatHang(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./sounds/flipingCard.mp3")
        pygame.mixer.music.play()

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
            self.kartyaMutatHang()
            # Tét összegének frissítése
            self.tet_ossz.config(text=f"Jelenlegi tét: {self.current_tet} Ft")
        except ValueError as e:
            self.canvas.create_text(350, 350, text="Hiba! Érvénytelen tét.", fill="red", font=("Arial", 18, 'bold'))

    def jatekos_huz(self):
        self.jatekos.kartyat_hozzaad(self.pakli.huz())
        self.frissit_ablak()
        self.huzHang()
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
        self.canvas.create_text(350, 400, text=f"Egyenleg: {self.jatekos.egyenleg} Ft", fill="white", font=("Arial", 18, 'bold'))
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
            self.pakli = Pakli.Pakli()
            self.current_tet = 0
            self.huz_gomb.config(state=tk.DISABLED)
            self.megall_gomb.config(state=tk.DISABLED)
            self.restart_gomb.config(state=tk.DISABLED)
            self.tet_gomb.config(state=tk.NORMAL)  # Tét gomb újra engedélyezése
            self.canvas.delete("all")
            self.kezdeti_osztas()
            self.canvas.create_text(100, 50, text="Játékos", fill="white", font=("Arial", 16, 'bold'), anchor=tk.S)
            self.canvas.create_text(100, 80, text=f"Érték: {self.jatekos.kez_ertek() if self.current_tet > 0 else '???'}", fill="white", font=("Arial", 14), anchor=tk.S)
            self.canvas.create_text(550, 50, text="Osztó", fill="white", font=("Arial", 16, 'bold'), anchor=tk.S)
            self.canvas.create_text(550, 80, text=f"Érték: {self.oszto.kez_ertek() if self.current_tet > 0 else '???'}", fill="white", font=("Arial", 14), anchor=tk.S)
            self.canvas.create_text(350, 400, text=f"Egyenleg: {self.jatekos.egyenleg} Ft", fill="white", font=("Arial", 18, 'bold'))
        else:
            self.canvas.create_text(350, 370, text="Játék vége! Nincs több pénzed.", fill="red", font=("Arial", 18, 'bold'))

    def jatek_inditas(self):
        self.kezdeti_osztas()
        self.canvas.create_text(350, 400, text=f"Egyenleg: {self.jatekos.egyenleg} Ft", fill="white", font=("Arial", 18, 'bold'))

# Fő ablak
root = tk.Tk()
jatek = FeketeJatek(root)
jatek.jatek_inditas()
root.mainloop()
tk.Tk
