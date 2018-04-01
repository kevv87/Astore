from manejo_txt import *

class usersTable():
    def __init__(self):
        self.file = 'pruebas.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

    def is_in(self, ele, row, column):
        if row == len(self.list)-1:
            if column == len(self.list[0])-1:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row]
                else:
                    return False
            else:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)
        else:
            if column == len(self.list[0]):
                return self.is_in(ele, row+1, 0)
            else:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)

    def get_list(self):
        return self.list[1:]

    def add(self, lista):
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            print(self.list + [lista])
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
        else:
            print('Faltan columnas')


users = usersTable()

users.add(['Kevin', 'asdsd', 'asdasd', 'None', 'None', 'si'])

