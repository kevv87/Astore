import sys
sys.setrecursionlimit(10000) # Cambiando el limite de recursividad porque las listas de apps se pueden alargar mucho
from tkinter import filedialog as fd

def create_db(contenido, file):
    create_db_aux(contenido, 0, 0, [], file)


def suma_list(lista, cont):
    if len(lista)-1 == cont:
        return lista[cont]
    else:
        return  lista[cont] + suma_list(lista, cont+1)

def create_db_aux(contenido, cont_row, cont_column, list_column_width, file):
    if cont_row == 0:
        if cont_column == len(contenido[0]):
            file.write('\n')
            file.write('-'*((suma_list(list_column_width, 0))-2))
            file.write('\n')
            return create_db_aux(contenido, cont_row+1, 0, list_column_width, file)
        else:
            list_column_width = list_column_width + [(max_len_column(contenido, cont_column))+2]
            file.write(contenido[0][cont_column]+'  '+' '*(list_column_width[cont_column]-(len(contenido[cont_row]
                                                                                               [cont_column])+2)))
            return create_db_aux(contenido, cont_row, cont_column+1, list_column_width, file)
    else:
        if cont_row == len(contenido):
            if cont_column ==len(contenido[0]):
                return
            else:
                return create_db_aux(contenido, cont_row, cont_column+1, list_column_width, file)
        elif cont_column == len(contenido[0]):
            file.write('\n')
            return create_db_aux(contenido, cont_row+1, 0, list_column_width, file)
        else:
            file.write(str(contenido[cont_row][cont_column])+'  '+' '*(list_column_width[cont_column]-(len(contenido[cont_row]
                                                                                               [cont_column])+2)))
            return create_db_aux(contenido, cont_row, cont_column+1, list_column_width, file)


def max_len_column(lista, column):
    return max_len_column_aux(lista, 0, '', column)


def max_len_column_aux(lista, cont, max, column):
    if len(lista) == cont:
        return len(max)
    elif len(lista[cont][column]) > len(max):
        return max_len_column_aux(lista, cont+1, lista[cont][column], column)
    else:
        return max_len_column_aux(lista, cont+1, max, column)



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


def normalize_list_table_aux2(lista, cont):
    if cont == len(lista):
        return []
    elif lista[cont] == '' or lista[cont] == ' ':
        return [] + normalize_list_table_aux2(lista, cont+1)
    elif lista[cont] == '\n' or lista[cont] == ' \n':
        return [] + normalize_list_table_aux2(lista, cont + 1)
    elif lista[cont].startswith(' '):
        if lista[cont].endswith('\n'):
            return [lista[cont][1:len(lista[cont])-1]] + normalize_list_table_aux2(lista, cont+1)
        else:
            return [lista[cont][1:]] + normalize_list_table_aux2(lista, cont+1)
    elif lista[cont].endswith('\n'):
        return [lista[cont][:len(lista[cont])-1]] + normalize_list_table_aux2(lista, cont+1)
    else:
        return [lista[cont]] + normalize_list_table_aux2(lista, cont+1)


def normalize_list_table_aux3(list, cont):
    if len(list) == cont:
        return []
    else:
        return [normalize_list_table_aux2(list[cont], 0)] + normalize_list_table_aux3(list, cont+1)


def find_all(lista, ele, column, cont):
    if len(lista) == cont:
        return []
    elif lista[cont][column] == ele:
        return [lista[cont]] + find_all(lista, ele, column, cont+1)
    else:
        return find_all(lista, ele, column, cont+1)

def is_in(lista, ele, contcolumn, controw):
    if len(lista) == controw:
        return False, False
    elif len(lista[controw]) == contcolumn:
        return is_in(lista, ele, 0, controw+1)
    elif lista[controw][contcolumn].lower().replace(' ', '') == ele.lower().replace(' ', ''):
        return lista[controw], int(controw)
    else:
        return is_in(lista, ele, contcolumn+1, controw)


def lista_isin(lista, ele, cont):
    if len(lista) == cont:
        return False
    elif lista[cont].lstrip().replace(' ','').lower() == ele.lstrip().replace(' ','').lower():
        return lista[cont], cont
    else:
        return lista_isin(lista, ele, cont+1)