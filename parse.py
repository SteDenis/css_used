import os
from tkinter import filedialog
import tkinter as tk
from tkinter.ttk import Frame, Button, Style, Progressbar
import threading
cwd = os.getcwd()
import tkinter.simpledialog

class City:
    def __init__(self, name):
        self.name = name
        self.how = ''
        self.why = ''
        self.store = ''
        self.locality = ''
        self.airport = ''
        self.station = ''
        self.place = ''
        self.event = ''
        self.park = ''
        self.museum = ''
        self.street = ''

class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("City Maker")
        self.root.geometry("830x730")
        #self.root.resizable(False, False)
        self.style = Style()
        self.style.theme_use("classic")
        self.city = None
        self.data = None
        self.file = None
        self.line = ''
        self.result = None
        self.step = 0
        frame = tk.Frame(self.root, width=830, height=720)
        frame.pack(fill=tk.X, side=tk.TOP, pady=10)

        frame_top = tk.Frame(frame, height=250)
        frame_top.grid(row=0, column=0)

        self.btn_file = Button(frame_top, width="13", text="Browse File Text", command=self.browse_file)
        self.btn_file.grid(row=0, column=0)

        self.btn_city = Button(frame_top, width="13", text="City Name", command=self.getText)
        self.btn_city.grid(row=0, column=1)

        self.btn_start = Button(frame_top, width="13", text="Start", command=self.start)
        self.btn_start.grid(row=0, column=2)

        frame_top2 = tk.Frame(frame, height=400)
        frame_top2.grid(row=1, column=0)

        self.txt = tk.Text(frame_top2, borderwidth=3, relief="sunken", width=100, height=10)
        self.txt.config(font=("consolas", 9), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        frame_top3 = tk.Frame(frame, height=400)
        frame_top3.grid(row=2, column=0)

        self.btn_app = Button(frame_top3, width="13", text="Ajouter", command=self.append)
        self.btn_app.grid(row=0, column=0)

        self.btn_ign = Button(frame_top3, width="13", text="Ignorer", command=self.append)
        self.btn_ign.grid(row=0, column=1)

        self.btn_nxt = Button(frame_top3, width="13", text="Etape suivante", command=self.append)
        self.btn_nxt.grid(row=0, column=2)

    def browse_file(self):
        file = filedialog.askopenfilename(initialdir = cwd, title = "Select text file")
        if file:
            self.file = file
            lines = []
            with open (self.file, 'rt') as file:
                for line in file:
                    lines.append(line)
            self.data = [ elem for elem in lines if elem != '\n']

    def append(self):
        self.city.how = self.city.how + self.line
        self.result = 1

    def start(self):
        def real_traitement():
            for self.line in self.data:
                self.result = None
                self.txt.config(state=tk.NORMAL)
                self.txt.delete('1.0', tk.END)
                self.txt.insert(tk.END, self.line)
                while self.result is None:
                    pass
        threading.Thread(target=real_traitement).start()

    def getText(self):
        city = tkinter.simpledialog.askstring("City Name", "Nom de la ville")
        self.city = City(city)

if __name__ == "__main__":
    inter = Interface()
inter.root.mainloop()


#name = input("Enter city name : ")
#ville = City(name)
#sep = ''
#for line in list1:
#    print(line)
#    if step == 0:
#        res = input("Ajouter cette ligne a HOW to ?")
#        if res == "0":
#            ville.how = ville.how + line
#        elif res == "2":
#            continue
#        elif res == "3":
#            print (ville.how)
#            break
#{ "country" : "IT" , "name" : "Rome" , "i18n" : { "es" : { "name" : "Roma" , "slug" : "roma" , "atName" : "en Roma" , "articleName" : "Roma"} , "it" : { "name" : "Roma" , "slug" : "roma" , "atName" : "a Roma" , "articleName" : "Roma"} , "de" : { "name" : "Roma" , "slug" : "roma" , "atName" : "in Roma" , "articleName" : "Roma"} , "en" : { "slug" : "rome" , "atName" : "in Rome" , "articleName" : "Rome" , "name" : "Rome"} , "fr" : { "slug" : "rome" , "atName" : "à Rome" , "articleName" : "Rome" , "name" : "Rome"} , "pt" : { "slug" : "rome" , "atName" : "em Rome" , "articleName" : "Rome" , "name" : "Rome"} , "zh" : { "slug" : "rome" , "atName" : "in Rome" , "articleName" : "Rome" , "name" : "Rome"}} , "latitude" : 41.90278349999999 , "longitude" : 12.496365500000024 , "type" : "locality" , "poiIndexes" : [ "566-128" , "729-129" , "777-544"] , "customLanding" : true , "reference" : "2898-46" , "creationDate" : 1564652624038 , "iatas" : [ "ROM" , "FCO" , "CIA"] , "lastUpdateDate" : 1565114590236 ,
#  "landing" : { "fr" :
#  { "how" : "<p>a</p>" ,
#  "why" : "" ,
#  "store" : "" ,
#  "typeIntros" :
#       { "locality" : "" , "airport" : "" , "station" : "" , "place" : "" , "event" : "" , "park" : "" , "museum" : "" , "street" : ""}}}}