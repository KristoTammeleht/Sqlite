import sqlite3
from tkinter import *
import ttkbootstrap as ttkbs
import tkinter as tk
from tkinter import ttk
lehekylg = 1 

def loe_andmed(lehekylg, otsing):
    conn = sqlite3.connect('autod.db')
    c = conn.cursor()
    if otsing:
        c.execute("SELECT * FROM autod WHERE first_name LIKE ? LIMIT ?, 20", (f'%{otsing}%', (lehekylg - 1) * 20,))
    else:
        c.execute("SELECT * FROM autod LIMIT ?, 20", ((lehekylg - 1) * 20,))
    andmed = c.fetchall()
    conn.close()
    return andmed

def kuvada_andmed():
    otsing = otsingu_sisestus.get()
    andmed = loe_andmed(lehekylg, otsing)
    loend.delete(0, END)
    for rida in andmed:
        loend.insert(END, rida)
    uuenda_sisestuste_arvu()

def lehekylge_edasi():
    global lehekylg
    lehekylg += 1
    kuvada_andmed()
    sisestus.delete(0, END)
    sisestus.insert(0, lehekylg)
    uuenda_sisestuste_arvu()

def lehekylge_tagasi():
    global lehekylg
    lehekylg -= 1
    if lehekylg < 1:
        lehekylg = 1
    kuvada_andmed()
    sisestus.delete(0, END)
    sisestus.insert(0, lehekylg)
    uuenda_sisestuste_arvu()

def kustuta_rida():
    id = kustutus_sisestus.get()
    conn = sqlite3.connect('autod.db')
    c = conn.cursor()
    c.execute("DELETE FROM autod WHERE id=?", (id,))
    conn.commit()
    conn.close()
    kuvada_andmed()
    uuenda_sisestuste_arvu()

def lisa_andmed():
    conn = sqlite3.connect('autod.db')
    c = conn.cursor()
    c.execute("INSERT INTO autod (first_name,last_name,email,car_make,car_year,car_price) VALUES (?, ?, ?, ?, ?, ?)",
              (eesnimi_sisestus.get(), perenimi_sisestus.get(), email_sisestus.get(), automark_sisestus.get(), aasta_sisestus.get(), hind_sisestus.get()))
    conn.commit()
    conn.close()
    uuenda_sisestuste_arvu()

def uuenda_sisestuste_arvu():
    conn = sqlite3.connect('autod.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM autod")
    result = c.fetchone()
    sisestuste_arv_silt.config(text="Sisestuste arv: " + str(result[0]))


aken = Tk()
aken.title('OW mu silmad valutavad  4')

style = ttk.Style()
style.theme_use('clam')

paned = ttkbs.Panedwindow(aken, orient=VERTICAL)
paned.pack(fill=BOTH, expand=1)

andmete_konteiner = ttkbs.Frame(paned, relief=SOLID, borderwidth=2)
paned.add(andmete_konteiner, weight=1)

loend = Listbox(aken, height=10, width=70)
loend.pack(side=LEFT, fill=Y)

otsingu_nupp = Button(aken, text="Otsi", command=kuvada_andmed)
otsingu_nupp.pack(side=LEFT)

otsingu_silt = Label(aken, text="Otsi nime järgi:")
otsingu_silt.pack(side=LEFT)

otsingu_sisestus = Entry(aken, width=20)
otsingu_sisestus.pack(side=LEFT)



kerimine = Scrollbar(aken)
kerimine.pack(side=RIGHT, fill=Y)
loend.configure(yscrollcommand=kerimine.set)
kerimine.configure(command=loend.yview)



#kustuta
kustutus_silt = Label(aken, text="Kustutamise ID:")
kustutus_silt.pack()

sisestus_kont = Frame(aken)
sisestus_kont.pack()

kustutus_sisestus = Entry(sisestus_kont, width=20)
kustutus_sisestus.pack(side=LEFT)

kustuta_nupp = Button(sisestus_kont, text="Kustuta", command=kustuta_rida)
kustuta_nupp.pack(side=LEFT)


#lisamine
eesnimi_silt = Label(aken, text="Eesnimi:")
eesnimi_silt.pack()

eesnimi_sisestus = Entry(aken, width=20)
eesnimi_sisestus.pack()

perenimi_silt = Label(aken, text="Perenimi:")
perenimi_silt.pack()

perenimi_sisestus = Entry(aken, width=20)
perenimi_sisestus.pack()

email_silt = Label(aken, text="Email:")
email_silt.pack()

email_sisestus = Entry(aken, width=20)
email_sisestus.pack()

automark_silt = Label(aken, text="Auto mark:")
automark_silt.pack()

automark_sisestus = Entry(aken, width=20)
automark_sisestus.pack()

aasta_silt = Label(aken, text="Auto aasta:")
aasta_silt.pack()

aasta_sisestus = Entry(aken, width=20)
aasta_sisestus.pack()

hind_silt = Label(aken, text="Auto hind:")
hind_silt.pack()

hind_sisestus = Entry(aken, width=20)
hind_sisestus.pack()

lisa_nupp = Button(aken, text="Lisa andmed", command=lisa_andmed)
lisa_nupp.pack()





# nupud lehekülje muutmiseks
tagasi_nupp = Button(aken, text="-", command=lehekylge_tagasi)
tagasi_nupp.pack(side=LEFT)

sisestus = Entry(aken, width=5)
sisestus.insert(0, lehekylg)
sisestus.pack(side=LEFT)

edasi_nupp = Button(aken, text="+", command=lehekylge_edasi)
edasi_nupp.pack(side=LEFT)


sisestuste_arv_silt = Label(aken, text="Sisestuste arv: 0")
sisestuste_arv_silt.pack()

nupp = Button(aken, text="Kuva andmed", command=kuvada_andmed)
nupp.pack()

aken.mainloop()