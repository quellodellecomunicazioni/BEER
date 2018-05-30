import tkinter as tk
from tkinter import font  as tkfont
import tkinter.scrolledtext as tkst
import webbrowser
import os
import winsound


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18,
                                      weight="bold", slant="italic")
        self.title("BEER")
        self.iconbitmap('ico_beer.ico')

        menu = tk.Menu(self)
        self.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label='About Me', command=self.about_me)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, AddPage, ListPage, SearchPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=1, column=1, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def about_me(self):
        webbrowser.open_new(r"https://github.com/quellodellecomunicazioni")
    def client_exit(self):
        exit()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        label = tk.Label(self, text="Benvenuto Davide!",
                         font=controller.title_font)
        label.grid(row=0, columnspan=4)

        plus = tk.PhotoImage(file='piu.png')
        button1 = tk.Button(self, image=plus, compound=tk.TOP, text="NUOVA",
                            command=lambda: controller.show_frame("AddPage"))
        button1.image = plus
        button1['border']='0'
        button1.grid(row=1, column=1)

        lista = tk.PhotoImage(file='lista.png')
        button2 = tk.Button(self, image=lista, compound=tk.TOP, text="ELENCO",
                            command=lambda: controller.show_frame("ListPage"))
        button2.image = lista
        button2['border']='0'
        button2.grid(row=2, columnspan=3)

        cerca = tk.PhotoImage(file='find.png')
        button3 = tk.Button(self, image=cerca, compound=tk.TOP, text="CERCA",
                            command=lambda: controller.show_frame("SearchPage"))
        button3.image = cerca
        button3['border']='0'
        button3.grid(row=1, column=2)

class AddPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        label = tk.Label(self, text="Aggiungi qui!",
                         font=controller.title_font)
        label.grid(row=0, columnspan=3)

        label = tk.Label(self, text="MARCA")
        label.grid(row=1)
        e = tk.Entry(self)
        e.grid(row=1,column=1)

        label1 = tk.Label(self, text="TIPO")
        label1.grid(row=2)
        e1 = tk.Entry(self)
        e1.grid(row=2,column=1)

        label2 = tk.Label(self, text="PAESE")
        label2.grid(row=3)
        e2 = tk.Entry(self)
        e2.grid(row=3,column=1)

        submit = tk.PhotoImage(file="sub.png")
        button1 = tk.Button(self, image=submit,
                           command=lambda: self.save(e,e1,e2))
        button1['border']='0'
        button1.image = submit
        button1.grid(row=4,column=1, sticky="e")

        home = tk.PhotoImage(file="home.png")
        button = tk.Button(self, image=home,
                           command=lambda: controller.show_frame("StartPage"))
        button['border']='0'
        button.image = home
        button.grid(row=4)

    def save(self, brand, type, country):
        with open("log.txt", "a") as f:
            f.write(brand.get() + ", " + type.get() + ", " + country.get()+"/")

class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        label = tk.Label(self, text="Cosa cerchi?", font=controller.title_font)
        label.grid(row=0,columnspan=3)

        e5 = tk.Entry(self)
        e5.grid(row=1,column=0)
        look = tk.PhotoImage(file="look.png")
        button1 = tk.Button(self, image=look, command=lambda: self.research(e5))
        button1['border']='0'
        button1.image = look
        button1.grid(row=1,column=1)

        editArea= tkst.ScrolledText(master=self, wrap=tk.WORD, width=33,
                                    height=10)
        editArea.grid(row=2,columnspan=2)

        home = tk.PhotoImage(file="home.png")
        button = tk.Button(self, image=home,
                           command=lambda: controller.show_frame("StartPage"))
        button['border']='0'
        button.image = home
        button.grid(row=3,column=0)

    def research(self, ent):
        pattern = ent.get()

        editArea= tkst.ScrolledText(master=self, wrap=tk.WORD, width=33,
                                    height=10)
        editArea.grid(row=2,columnspan=2)

        with open("log.txt", "r") as f:
            cont = f.read()
            splitted = cont.split("/")
            for beer in splitted:
                if pattern in beer:
                    test = beer
                    editArea.insert(tk.INSERT, test + "\n")
        editArea.config(state=tk.DISABLED)

class ListPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(2, weight=2)
        label = tk.Label(self, text="Tutto quello che hai!",font=controller.title_font)
        label.grid(row=0,columnspan=3)

        editArea= tkst.ScrolledText(master=self, wrap=tk.WORD, width=33,
                                    height=10)
        editArea.grid(row=1)
        with open("log.txt", "r") as f:
            text = f.read()
            splitted = text.split("/")
            for beers in splitted:
                editArea.insert(tk.INSERT, beers + "\n")
        editArea.config(state=tk.DISABLED)
        home = tk.PhotoImage(file="home.png")
        button = tk.Button(self, image=home,
                           command=lambda: controller.show_frame("StartPage"))
        button['border']='0'
        button.image = home
        button.grid(row=2, column=0)

if __name__ == "__main__":
    #winsound.PlaySound("song.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
    app = SampleApp()
    app.mainloop()
