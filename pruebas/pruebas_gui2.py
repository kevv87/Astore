from tkinter import *
from PIL import ImageTk, Image



class listaApps:
    def __init__(self, root):
        self.canvas = Canvas(root, borderwidth=0, bg='red')
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.img_path = '../images/icons/back.png'
        self.img_load = Image.open(self.img_path)
        self.img = ImageTk.PhotoImage(self.img_load)

        self.populate()
    def populate(self, *args):
        for row in range(100):
            Label(self.frame, image=self.img).grid(row=row, column=0)
            t="this is the second column for row %s" %row
            Label(self.frame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))






root=Tk()

prueba = listaApps(root)

root.mainloop()