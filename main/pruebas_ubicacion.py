from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from random import randint

root = Tk()

canvas = Canvas(root)
canvas.pack()

juego1_load_banner = Image.open('../apps/juegos/yume_nikki/icon.jpg')
juego1_banner = ImageTk.PhotoImage(juego1_load_banner)
juego1_banner_label = Label(canvas, image=juego1_banner)
juego1_banner_label.pack()
juego1_banner_label.place(x=0,y=0)

root.mainloop()