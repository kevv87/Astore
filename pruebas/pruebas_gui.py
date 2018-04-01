from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from random import randint
bg_color = '#bbb8c1'


class manageWinVendedores:
    def __init__(self, root):
        self.canvas = Canvas(root, borderwidth=0, bg=bg_color)
        self.frame = Frame(self.canvas, background=bg_color)
        self.vsby = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.vsbx = Scrollbar(root, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsby.set)
        self.canvas.configure(xscrollcommand=self.vsbx.set)

        self.vsby.pack(side="right", fill="y")
        self.vsbx.pack(side='bottom',fill='x')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.lista_apps = [[],[]]

        # Dimensiones
        self.sc_width = root.winfo_screenwidth()
        self.sc_height = root.winfo_screenheight()
        self.width = self.sc_width * 60 / 100
        self.height = self.sc_height * 50 / 100
        root.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 25 / 100, self.sc_height * 15 / 100))
        self.buttons=[]


        self.table()

        self.frame.update()
        #self.load_plus = Image.open('../images/icons/plus.png').resize((self.frame.winfo_width(), 100), Image.ANTIALIAS)
        #self.plus_img = ImageTk.PhotoImage(self.load_plus)
        #self.plus = Label(self.frame, image=self.plus_img)
        #self.plus.grid(row=2, column=0, columnspan=3)


    def table(self, *args):
        self.headers = ['ID', 'Nombre', 'Correo', 'Pagina Web']
        Label(self.frame, text=self.headers[0], bg=bg_color).grid(row=0, column=0)
        Label(self.frame, text=self.headers[1], bg=bg_color).grid(row=0, column=1)
        Label(self.frame, text=self.headers[2], bg=bg_color).grid(row=0, column=2)
        Label(self.frame, text=self.headers[3], bg=bg_color).grid(row=0, column=3)
        self.__table_aux([['1', 'Google', 'support@gmail.com', 'www.google.com'], ['2', 'Microsoft', 'support@outlook.com', 'www.example.com '], ['2', 'Joel Kant', 'joelk@coolmail.com', 'none'], ['3', 'Theodore Brown', 'tbrown@coolmail.com', 'none'], ['4', 'Rafael Gondor', 'rafag@notcoolmail.com', 'none']]
, 0, 0)

    def __table_aux(self, info, controw, contcolumn):
        if controw == len(info):
            return
        elif contcolumn == len(info[0]):
            load_erase_img = Image.open('../images/icons/red_cross.png').resize((10,10), Image.ANTIALIAS)
            erase_img = ImageTk.PhotoImage(load_erase_img)
            self.buttons = self.buttons + ['eraseme']
            self.buttons[controw] = Label(self.frame, image=erase_img, bg=bg_color)
            self.buttons[controw].grid(row=controw+1, column=contcolumn)
            self.buttons[controw].image = erase_img
            self.buttons[controw].bind('<Button-1>', lambda event: self.erase(controw))
            return self.__table_aux(info, controw + 1, 0)
        else:
            Label(self.frame, text=info[controw][contcolumn], bg=bg_color).grid(row=controw+1, column=contcolumn, sticky=W)
            self.__table_aux(info, controw, contcolumn+1)


    def onFrameConfigure(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def erase(self, row):
        print('c')


root=Tk()
prueba = listaApps(root)
mainloop()