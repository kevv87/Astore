from tkinter import *

def normalize_list_table(list, cont):
    list_filter1 = normalize_list_table_aux1(list, 0)
    list_filter2 = normalize_list_table_aux3(list_filter1, 0)
    cleaned_list = list_filter2[:1] + list_filter2[2:]
    return cleaned_list


def normalize_list_table_aux1(list, cont):
    if cont == len(list):
        return list
    else:
        list[cont] = str(list[cont]).split('  ')
        return normalize_list_table_aux1(list, cont+1)


def normalize_list_table_aux2(list, cont):
    if cont == len(list):
        return []
    elif list[cont] == '':
        return [] + normalize_list_table_aux2(list, cont+1)
    elif list[cont] == '\n' or list[cont] == ' \n':
        return [] + normalize_list_table_aux2(list, cont + 1)
    else:
        return [list[cont]] + normalize_list_table_aux2(list, cont+1)


def normalize_list_table_aux3(list, cont):
    if len(list) == cont:
        return []
    else:
        return [normalize_list_table_aux2(list[cont], 0)] + normalize_list_table_aux3(list, cont+1)

class appTable:
    def __init__(self):
        self.file = '../apps/apps.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()
        self.musica = self.list_categoria('Musica', 0)
        self.juegos = self.list_categoria('Juegos', 0)
        self.herramientas = self.list_categoria('Herramientas', 0)
        self.redes = self.list_categoria('Redes', 0)


    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

    def get_list(self):
        return self.list[1:]

    def get_headers(self):
        return self.list[:1]

    def get_musica(self):
        return self.musica

    def get_juegos(self):
        return self.juegos

    def get_herramientas(self):
        return self.herramientas

    def get_redes(self):
        return self.redes

    def list_categoria(self, categ, row):
        column_categoria = 3
        if row == len(self.list):
            return []
        elif self.list[row][column_categoria].lstrip() == categ:
            return [self.list[row]] + self.list_categoria(categ, row+1)
        else:
            return [] + self.list_categoria(categ, row+1)

def start_search(*args):
    ele = trymebitch.entry.get()
    print(search_nombre_by_letter(apps.get_list(), ele, 0))

class prueba:
    def __init__(self):
        self.root = Tk()
        self.entry = Entry(self.root)
        self.entry.pack()
        self.entry.bind('<KeyRelease>', start_search)


def search_nombre_by_letter(lista, ele, cont):
    if ele != '' and ele != ' ':
        if len(lista) == cont:
            return []
        elif lista[cont][2].lower().replace(' ', '').startswith(ele):
            return [lista[cont]] + search_nombre_by_letter(lista, ele, cont+1)
        else:
            return search_nombre_by_letter(lista, ele, cont+1)
    else:
        return []

mainloop()
