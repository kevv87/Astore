# E: Numero variable de listas y el numero de indice que se quiere comparar
# S: Numero de letras de la palabra mas grande del indice de todas las listas
# R: Todas los elementos deben ser listas del mismo tamanno.
def bigger_word(*args):  # Para que funcione bien, primero se dan las listas y de ultimo el indice.
    if bigger_word_verifier(args[:len(args)-1], 0, len(args[0])):
        return bigger_word_aux(args[:len(args)-1], args[len(args)-1], -1, 0)
    else:
        return 'Error'

# E: Una lista
# S: True si todos los elementos de la lista son listas y tienen el mismo tamanno, False de lo contrario
# R: lista valida
def bigger_word_verifier(lista, cont, largo_necesario):
    if cont == len(lista):
        return True
    if isinstance(lista[cont], list) and len(lista[cont]) == largo_necesario:
        return bigger_word_verifier(lista, cont+1, largo_necesario)
    else:
        return False


def bigger_word_aux(lista, indice, mayor_len, cont):
    if cont == len(lista):
        return mayor_len
    elif len(lista[cont][indice]) >= mayor_len:
        mayor_len = len(lista[cont][indice])
        return bigger_word_aux(lista, indice, mayor_len, cont+1)
    else:
        return bigger_word_aux(lista, indice, mayor_len, cont+1)

