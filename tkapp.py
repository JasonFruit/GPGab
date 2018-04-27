#!/usr/bin/env python3
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self,
                                    text='Quit',
                                    command=self.quit)
        self.quitButton.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.buttButton = tk.Button(self,
                                    text='Butt',
                                    command=self.quit)
        self.buttButton.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.footButton = tk.Button(self,
                                    text='Foot',
                                    command=self.quit)
        self.footButton.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.pianoButton = tk.Button(self,
                                     text='Piano',
                                     command=self.quit)
        self.pianoButton.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.rowconfigure(0, minsize=120)
        self.rowconfigure(1, minsize=120)
        self.columnconfigure(0, minsize=160)
        self.columnconfigure(1, minsize=160)
        
app = Application()
app.master.minsize(320, 240)
app.master.title('Full-size Thing') 
app.mainloop()                         
