#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkf
from random import choice

key_defs = [["1!", "2@", "3#", "4$", "5%", "6^", "7&", "8*", "9(", "0)"],
            ["qQ", "wW", "eE", "rR", "tT", "yY", "uU", "iI", "oO", "pP"],
            ["aA", "sS", "dD", "fF", "gG", "hH", "jJ", "kK", "lL", "'\""],
            ["zZ", "xX", "cC", "vV", "bB", "nN", "mM", ",<", ".>", "/?"]]
            
font_name = "Linux Libertine Mono O"
font_size = 8

class KeyButton(tk.Button):
    def __init__(self, key_def, master=None):
        self.narrow = tkf.Font(family=font_name, size=font_size)
        tk.Button.__init__(self,
                           master,
                           text=key_def[0],
                           font=self.narrow,
                           command=self.send_key,
                           borderwidth=0,
                           highlightthickness=0)
        self.key_def = key_def

    def shift(self):
        self["text"] = self.key_def[1]

    def unshift(self):
        self["text"] = self.key_def[0]

    def send_key(self):
        self.master.handle_key(self["text"])

class Keyboard(tk.Frame):
    def __init__(self, keyhandler, master=None):
        self.narrow = tkf.Font(family=font_name, size=font_size)
        tk.Frame.__init__(self, master)
        self.keyhandler = keyhandler
        self.grid()
        self.add_keys()
        self.shifted = False

    def handle_key(self, char):
        self.keyhandler(char)

        if self.shifted:
            self.shift()

    def add_keys(self):
        self.keys = []
        
        for row in range(len(key_defs)):
            for col in range(len(key_defs[row])):
                keybutton = KeyButton(key_defs[row][col], self)
                keybutton.grid(row=row,
                               column=col,
                               ipadx=0,
                               padx=0,
                               sticky=tk.N + tk.S + tk.E + tk.W)
                self.keys.append(keybutton)

        row = len(key_defs)

        self.shift_key = tk.Button(text="Shift",
                                   command=self.shift,
                                   master=self,
                                   font=self.narrow)
        self.shift_key.grid(row=row,
                            column=0,
                            columnspan=3,
                            sticky=tk.N + tk.S + tk.E + tk.W)

        self.space_key = KeyButton("  ",
                                   master=self)
        self.space_key.grid(row=row,
                            column=3,
                            columnspan=4,
                            sticky=tk.N + tk.S + tk.E + tk.W)

        self.symbol_key = tk.Button(text="Symbol",
                                    command=self.symbol,
                                    master=self,
                                    font=self.narrow,
                                    padx=0,
                                    bd=0)
        self.symbol_key.grid(row=row,
                             column=7,
                             columnspan=3,
                             sticky=tk.N + tk.S + tk.E + tk.W)

        for col in range(10):
            self.columnconfigure(col, pad=0)

    def shift(self):
        self.shifted = not self.shifted
        
        for key in self.keys:
            if self.shifted:
                key.shift()
            else:
                key.unshift()

    def symbol(self):
        pass
                

class DemoApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.lbl = tk.Label(self)
        self.lbl.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.keyboard = Keyboard(keyhandler=self.handle_key, master=self)
        self.keyboard.grid(row=1, column=0)

        self.chars = []

    def handle_key(self, key):
        self.chars.append(key)
        self.lbl["text"] = "".join(self.chars)
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(master=root)

    app.master.minsize(320, 240)
    app.master.maxsize(320, 240)
    app.master.title('Full-size Thing') 
    app.mainloop()

    root.quit()

    print("".join(app.chars))
